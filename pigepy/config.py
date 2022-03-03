#!/usr/bin/env python
# encoding: utf-8

#import logging
import configparser, argparse
from pathlib import Path
from ast import literal_eval


class Config:
    """
    Load configuration from command lines arguments
    Note: logging line are commented because Config is loaded before Root handler is called, if someone know a workaround please submit a  pull request
    """
    def __init__(self):

        self.parser = argparse.ArgumentParser(description='PigePy is a script for recording audio stream')
        self.streamUrl = self.parser.add_argument('--stream', '-s', dest="stream", required=True, help='specify a stream url')
        self.basePath = self.parser.add_argument('--base-path', '-b', dest="basePath", required=True, type=self.verify_dir, help='Base destination directory absolute path.')
        self.dirFormat = self.parser.add_argument('--directory-format', '-df', dest="directoryFormat", default='%Y/%m/%d', help='sub directories structure in strftime format (default: "%%Y/%%m/%%d")')
        self.fileFormat = self.parser.add_argument('--file-format', '-ff', dest="filenameFormat", default="%Hh-%Mm-%Ss", help='filename format can contain strftime format (default: "%%Hh-%%Mm-%%Ss")')
        self.interval = self.parser.add_argument('--interval', '-i', dest="interval", default={"minutes": 60}, type=self.interval_validation, help='Audio files length kwargs format (default: {"minutes": 60})')
        self.alignToHour = self.parser.add_argument('--align', dest="align", action='store_true', help='automatcally align next record to hour hh:00')
        self.createdir_delta = self.parser.add_argument('--directory-delta', '-dd', dest="directoryDelta", default={"days": 1}, type=self.interval_validation, help='directory creating delta, kwargs format (default: {"days": 1})')
        self.schedulerTimezone = self.parser.add_argument('--timezone', '-tz', dest="schedulerTimezone", default="utc", help='APScheduler timezone  (default: utc)')
        self.chunkSize = self.parser.add_argument('--chunk-size', '-cz', dest="chunkSize", default=1024, type=self.check_chunkSize, help='How much data in octet will be stored in memory before it\'s write in the file. Must an integer multiple of 1024 eg 1024*512 = 0.5Mo (default: 1024 = 1Mo)')
        self.healthcheck_url = self.parser.add_argument('--healthcheck-url', dest="healthcheckUrl", default=False, help='Provide a healthcheck url to enable healthcheck monitoring (see https://healthchecks.io/ for more infos default: False)')
        self.healthcheck_interval = self.parser.add_argument('--heathcheck-interval', dest="healthcheckInterval", default={"minutes": 10}, type=self.interval_validation, help='healthcheck interval (aka ping interval) kwargs format (default: {"minutes": 10})')
        self.logLevel = self.parser.add_argument('--log-level', dest="logLevel", default="INFO", help='Set loggin output level (possible values DEBUG,INFO,WARNING,CRITICAL default: INFO)')

    def verify_dir(self, dirPath):
        
        directory = Path(dirPath)
        if directory.exists() and directory.is_dir():
            # logging.info('Directory %s exist', dirPath)
            print(f"ok directory : {dirPath} exist")
            return directory
        else:
            logging.error("Directory %s don't exist or is not readable", dirPath)
            print(f"Error directory : {dirPath} don't exist")
            raise argparse.ArgumentTypeError(f"readable_dir:{dirPath} is not a valid path")

    def check_duration(self, value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(
                'Duration in minutes must be a positive integer.')
            # logging.exception('Duration in minutes must be a positive integer.')
        if value < 1:
            raise argparse.ArgumentTypeError(
                'Duration in minutes must be a positive integer.')
            # logging.exception('Duration in minutes must be a positive integer.')
        else:
            return value

    def interval_validation(self, value):
        accepted_key = ["days", "hours", "minutes", "seconds"]
        for key, val in literal_eval(value).items():
            if key  in accepted_key:
                pass
            else:
                raise argparse.ArgumentTypeError(f"{key} is not available")
                # logging.exception("%s is not available", key)
            try:
                val = int(val)
            except ValueError:
                raise argparse.ArgumentTypeError('Duration in minutes must be a positive integer.')
                # logging.exception('Duration in minutes must be a positive integer.')
            if val < 1:
                raise argparse.ArgumentTypeError('Duration in minutes must be a positive integer.')
                # logging.exception('Duration in minutes must be a positive integer.')
        return literal_eval(value)

    def check_chunkSize(self, value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(
                'Chunk size must be a positive integer.')
            # logging.exception('Chunk size must be a positive integer.')
        if value < 1:
            raise argparse.ArgumentTypeError(
                'Chunk size must be a positive integer.')
            # logging.exception('Chunk size must be a positive integer.')
        else:
            return value
