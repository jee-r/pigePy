#!/usr/bin/env python
# encoding: utf-8

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

        #self.scheduler = BackgroundScheduler(daemon=False)
        self.scheduler = BlockingScheduler(daemon=False, timezone=timezone)
        #self.scheduler.add_listener(self.listener, EVENT_ALL)

    def start(self):
        """Start Scheduler"""

        print('Scheduler Start')
        self.scheduler.start()
        self.scheduler.print_jobs()

    def stop(self, myjobid):
        """Stop the scheduler"""

        self.scheduler.remove_job(myjobid)
        self.scheduler.print_jobs()
        print('Scheduler Stoped')

    def status(self):
        """Print jobs"""

        self.scheduler.print_jobs()

    def listener(self, event):
        """print all scheduler's events, usefull for debug"""

        print(event)

    def addRecorderJob(self, job_interval_args, args, replace_value=True):
        """ """
        def recorderLoop():
            """recorder loop that timeout after interval value"""

            from recorder import Recorder

            recorder_now_time = datetime.now()
            print(recorder_now_time)
            recorder_delta = timedelta(**job_interval_args)
            print(recorder_delta)
            recorder_next_time = recorder_now_time + timedelta(**job_interval_args)

            print("recorder now : " + str(recorder_now_time))
            print("recorder next : " + str(recorder_next_time))

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
