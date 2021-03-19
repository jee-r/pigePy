#!/usr/bin/env python
# encoding: utf-8

from scheduler import Scheduler
from recorder import Recorder
from filemanager import FileManager
from config import Config

def main():
    """Get args from config.py"""
    config = Config()
    args = config.parser.parse_args()

    """Scheduler"""
    scheduler = Scheduler(args.schedulerTimezone)

    recorder = Recorder(args.stream, args.basePath, args.interval, args.directoryFormat, args.filenameFormat)

    scheduler.scheduler.add_job(lambda: recorder.writeFile(), id="recorder_writeFile_init", max_instances=2)
    scheduler.scheduler.add_job(lambda: recorder.writeFile(), 'interval', **args.interval, max_instances=2, replace_existing=True, id="recorder_writeFile")

    filemanager = FileManager(args.basePath, args.directoryFormat, args.directoryDelta)

    scheduler.scheduler.add_job(lambda: filemanager.createDir(), replace_existing=True, id="create_dir_init")
    scheduler.scheduler.add_job(lambda: filemanager.createDir(), 'interval', **args.interval, replace_existing=True, id="create_dir")

    """DEBUG: print threads each interval"""
    #scheduler.scheduler.add_job(lambda: recorder.threadStatus(), id="threadStatus_init", max_instances=2)
    #scheduler.scheduler.add_job(lambda: recorder.threadStatus(), 'interval', **args.interval, max_instances=2, replace_existing=True, id="threadStatus")

    scheduler.scheduler.start()
    scheduler.scheduler.print_jobs()

if __name__ == "__main__":
    main()
