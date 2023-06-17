#!/usr/bin/env python
# encoding: utf-8

import logging
import requests
from requests.adapters import HTTPAdapter, Retry
import threading
import io
import concurrent.futures
from time import sleep
from datetime import datetime

class Recorder():
    """Record live stream"""

    def __init__(self, stream, basePath, interval, directoryFormat, filenameFormat, chunkSize, noSubDir, name='Recorder',):
        
        self._stopevent = threading.Event()
        self.stream = stream
        self.basePath = basePath
        self.interval = interval
        self.directoryFormat = directoryFormat
        self.filenameFormat = filenameFormat
        self.chunkSize = chunkSize
        self.noSubDir = noSubDir

        self.req = requests.Session()
        self.retries = Retry(total=20,
                backoff_factor=0.05,
                status_forcelist=[404, 429, 500, 502, 503, 504]
                )

        self.retry = requests.adapters.HTTPAdapter(max_retries=self.retries)
        self.response = ""

        self.writeFile_thread = False
        self.writeFile_executor = False
        self.writeFile_job = True

        logging.info('Recorder init : %s', name)

    def _getStream(self, current_jobId, retry=False):
        """Listen the Stream"""
        if retry:
            logging.info('Retry to connect to %s', self.stream)

        self.connection_etablished = False

        while not self.connection_etablished and not self._stopevent.is_set():
            try:
                self.req.mount(self.stream, self.retry)
                self.streamData = self.req.get(self.stream, stream=True)
                self.streamData.raise_for_status()
                if not self.getStream_jobId == current_jobId:
                    # print(f"Connection closed : {current_jobId}")
                    logging.info("Connection closed : %s", current_jobId)
                    return response
                #print(f"Connection etablished : {current_jobId}")
                logging.info("Connection established : %s", current_jobId)
                self.connection_etablished = True
            except Exception as ex:
                # print(f"Connection failed with error: {ex}")
                logging.error("Connection failed with error: %s", ex)
                self.connection_etablished = False
                return self.getStream(retry=True)

    def getStream(self):
        now = datetime.now()
        self.getStream_jobId = "getStream_jobId_" + str(now.timestamp())

        getStream_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        getStream_executor.submit(self._getStream, self.getStream_jobId)

        return

    def _writeFile(self, dest, current_job_id, retry=False):
        """Write file"""
        threading.current_thread().name = "WriteFileThread"
        self.writeFile_thread_stopEvent = threading.Event()

        # print(f"waiting for connection...")
        logging.info("Waiting for connection...")

        while not self.connection_etablished:
            sleep(1)

        with open(dest, 'wb') as out_file:
            try:
                # print(f"Start writing new audio file in : {dest} job_id : {current_job_id}")
                logging.info("Start Writing new audio in : %s job_id %s", dest, current_job_id)
                for chunk in self.streamData.iter_content(chunk_size=1024*self.chunkSize):
                    out_file.write(chunk)
                    if self.writeFile_thread_stopEvent.is_set():
                        # print(f"Stop event called")
                        logging.info("Stopped event called")
                        out_file.close()
                        # print(f"Audio File writed in : {dest} jobid: {current_job_id}")
                        logging.info("Audio File written in : %s jobid: %s", dest, current_job_id) 
                        break
            except Exception as ex:
                # print(f"writeFile {current_job_id} failed with error: {ex}")
                logging.error("WriteFile %s failed with error: %s", current_job_id, ex)
                self._writeFile(dest, current_job_id, retry=True)

    def writeFile(self):
        now = datetime.now()
        directoryName = now.strftime(self.directoryFormat)
        fileName = now.strftime(self.filenameFormat)
        
        if not self.noSubDir:
            dest = str(self.basePath) + "/" + directoryName + "/" + fileName + ".mp3"
        else:
            dest = str(self.basePath) + "/" + fileName + ".mp3"
            
        self.writeFile_jobId = "writeFileJobId_" + str(now.timestamp())

        try:
            """Ensure that old WriteFile job are done"""
            for thread in threading.enumerate():
                if thread.name == "WriteFileThread":
                    self.writeFile_thread_stopEvent.set()
                    thread.join(timeout=None)
            if self.writeFile_executor:
                self.writeFile_executor_old = self.writeFile_executor
            else:
                self.writeFile_executor_old = False

            self.getStream()
        finally:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="WriteFile") as self.writeFile_executor:
                self.writeFile_worker = self.writeFile_executor.submit(self._writeFile, dest, self.writeFile_jobId)

            """Kill old futures object"""
            if self.writeFile_executor_old:
                self.writeFile_executor_old.shutdown(wait=False)
            return
    
    def stop(self):
        """Stop the Recorder gracefully"""
        self._stopevent.set()

    def is_stopped(self):
        """Check if the Recorder is stopped"""
        return self._stopevent.is_set()
    
    def threadStatus(self):
        """Print all threads for debug purpose"""
        # print(threading.active_count())
        logging.debug("%s", threading.active_count())

        for thread in threading.enumerate():
            # print(thread.name)
            logging.debug("%s", thread.name)