#!/usr/bin/env python
# encoding: utf-8

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.events import EVENT_ALL
from datetime import datetime, timedelta

class Scheduler:
    """
    Scheduler is running as a blocking process
    """

    def __init__(self, timezone):

        logging.info("Scheduler: Initializing...")
        #self.scheduler = BackgroundScheduler(daemon=False)
        self.scheduler = BlockingScheduler(daemon=False, timezone=timezone)
        #self.scheduler.add_listener(self.listener, EVENT_ALL)
        logging.info("Scheduler: Initialized")

    def start(self):
        """Start Scheduler"""

        logging.info("Scheduler: Started")
        self.scheduler.start()
        self.scheduler.print_jobs()

    def stop(self, myjobid):
        """Stop the scheduler"""

        self.scheduler.remove_job(myjobid)
        self.scheduler.print_jobs()
        logging.info("Scheduler: Stopped")

    def status(self):
        """Print jobs"""

        self.scheduler.print_jobs()

    def listener(self, event):
        """print all scheduler's events, usefull for debug"""
    
        logging.debug("Scheduler: %s", event)

    def alignJob(self, job_interval_args):
        """
        Align job after init to the next hour
        TODO: create dynamic align system like minute, quarter, range of hours etc 
        """
        now = datetime.now()
        now_plus_one_hour = now + timedelta(hours = 1)
        alignto = now_plus_one_hour.replace(second=0, microsecond=0, minute=0) 

        logging.info("Align job value:  %s", alignto)
        
        return alignto
        
    def addRecorderJob(self, job_interval_args, args, replace_value=True):

        def recorderLoop():
            """recorder loop that timeout after interval value"""

            from recorder import Recorder

            recorder_now_time = datetime.now()
            logger.info("Scheduler: %s", recorder_now_time)
            # print(recorder_now_time)
            recorder_delta = timedelta(**job_interval_args)
            logger.info("Scheduler: %s", recorder_delta)
            print(recorder_delta)
            recorder_next_time = recorder_now_time + timedelta(**job_interval_args)

            logging.debug("Scheduler: recorder now : %s", recorder_now_time)
            logging.debug("Scheduler: recorder next : %s", recorde_next_time)

            # print("recorder now : " + str(recorder_now_time))
            # print("recorder next : " + str(recorder_next_time))

            recorder = Recorder(args.stream, args.segmentDuration, args.basePath, args.directoryFormat, args.filenameFormat, name='Recorder')

            self.scheduler.add_job(lambda: recorder.start(), replace_existing=replace_value, id="recorder_start")
            self.scheduler.add_job(lambda: recorder.join(), run_date=recorder_next_time, replace_existing=replace_value, id="recorder_join")
            self.scheduler.add_job(lambda: recorder.reset_job(), run_date=recorder_next_time, replace_existing=replace_value, id='recorder_reset')


        self.scheduler.add_job(lambda: recorderLoop(), replace_existing=True, id="recorder_loop")
        self.scheduler.add_job(lambda: recorderLoop(), 'interval', **job_interval_args, replace_existing=True, id="recorder_loop")

    def addFileManagerJob(self, job_interval_args, args, replace_value=True):

        from filemanager import FileManager

        fileManager_dirFormat = "%Y/%m/%d"
        filemanager = FileManager(args.basePath, fileManager_dirFormat)

        self.scheduler.add_job(lambda: filemanager.createOneDir(), replace_existing=replace_value, id="create_dir")
        self.scheduler.add_job(lambda: filemanager.createOneDir(), 'interval', **job_interval_args, replace_existing=replace_value, id="create_dir")
