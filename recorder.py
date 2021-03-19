#!/usr/bin/env python
# encoding: utf-8

import requests
import threading
import io
import concurrent.futures
from time import sleep
from datetime import datetime

class Recorder():
    """Record live stream"""


    def __init__(self, stream, basePath, interval, directoryFormat, filenameFormat, chunkSize, name='Recorder'):

        self._stopevent = threading.Event()

        self.stream = stream
        self.basePath = basePath
        self.interval = interval
        self.directoryFormat = directoryFormat
        self.filenameFormat = filenameFormat
        self.chunkSize = chunkSize

        self.req = requests.Session()
        self.response = ""

        self.writeFile_thread = False
        self.writeFile_executor = False
        self.writeFile_job = True


    def _getStream(self, current_jobId, retry=False):
        """Listen the Stream"""

        if retry:
            sleep(5)

        attempts = 5
        self.connection_etablished = False

        while not self.connection_etablished:
            try:
                self.streamData = self.req.get(self.stream, stream=True)
                self.streamData.raise_for_status()
                if not self.getStream_jobId == current_jobId:
                    print(f"Connection closed : {current_jobId}")
                    return response
                print(f"Connection etablished : {current_jobId}")
                self.connection_etablished = True
            except Exception as ex:
                print(f"Connection failed with error: {ex}")
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

        print(f"waiting for connection...")

        while not self.connection_etablished:
            sleep(1)

        with open(dest, 'wb') as out_file:
            try:
                print(f"Start writing new audio file in : {dest} job_id : {current_job_id}")
                for chunk in self.streamData.iter_content(chunk_size=1024*self.chunkSize):
                    out_file.write(chunk)
                    if self.writeFile_thread_stopEvent.is_set():
                        print(f"Stop event called")
                        out_file.close()
                        print(f"Audio File writed in : {dest} jobid: {current_job_id}")
                        break
            except Exception as ex:
                print(f"writeFile {current_job_id} failed with error: {ex}")
                self._writeFile(dest, current_job_id, retry=True)

    def writeFile(self):

        now = datetime.now()
        directoryName = now.strftime(self.directoryFormat)
        fileName = now.strftime(self.filenameFormat)
        dest = str(self.basePath) + "/" + directoryName + "/" + fileName + ".mp3"
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

    def threadStatus(self):
        """Print all threads for debug purpose"""
        print(threading.active_count())

        for thread in threading.enumerate():
            print(thread.name)
