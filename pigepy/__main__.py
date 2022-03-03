#!/usr/bin/env python
# encoding: utf-8

import logging
from scheduler import Scheduler
from recorder import Recorder
from filemanager import FileManager
from config import Config
# from logger import Logger


def main():

    """Get args from config.py"""
    config = Config()
    args = config.parser.parse_args()

    """Set Logger"""
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=getattr(logging, args.logLevel.upper()))
    logging.info('Logging init')

    """Scheduler"""
    scheduler = Scheduler(args.schedulerTimezone)

    if args.logLevel.upper() != 'DEBUG':
        logging.getLogger('apscheduler').setLevel(logging.ERROR)
    else:
        logging.getLogger('apscheduler').setLevel(logging.ERROR)

    recorder = Recorder(args.stream, args.basePath, args.interval, args.directoryFormat, args.filenameFormat, args.chunkSize)
    
    scheduler.scheduler.add_job(lambda: recorder.writeFile(), id="recorder_writeFile_init", max_instances=2)
    if args.align:
        start_date = scheduler.alignJob(args.interval)
        scheduler.scheduler.add_job(lambda: recorder.writeFile(), 'interval', **args.interval, start_date=start_date, id="recorder_writeFile", max_instances=2)
    else:
        scheduler.scheduler.add_job(lambda: recorder.writeFile(), 'interval', **args.interval, id="recorder_writeFile", max_instances=2)

    filemanager = FileManager(args.basePath, args.directoryFormat, args.directoryDelta)

    scheduler.scheduler.add_job(lambda: filemanager.createDir(), replace_existing=True, id="create_dir_init")
    scheduler.scheduler.add_job(lambda: filemanager.createDir(), 'interval', **args.interval, replace_existing=True, id="create_dir")

    if args.healthcheckUrl:
        from healthcheck import Healthcheck
        healthcheck = Healthcheck(args.healthcheckUrl)

        scheduler.scheduler.add_job(lambda: healthcheck.ping("main", "ping"), replace_existing=True, id="Healthcheck_main_init")
        scheduler.scheduler.add_job(lambda: healthcheck.ping("main", "ping"), 'interval', **args.healthcheckInterval, replace_existing=True, id="Healthcheck_main")

    """DEBUG: print threads each interval"""
    #scheduler.scheduler.add_job(lambda: recorder.threadStatus(), id="threadStatus_init", max_instances=2)
    #scheduler.scheduler.add_job(lambda: recorder.threadStatus(), 'interval', **args.interval, max_instances=2, replace_existing=True, id="threadStatus")

    scheduler.scheduler.start()
    scheduler.scheduler.print_jobs()
    
    logging.info('Good bye')

if __name__ == "__main__":
    main()
