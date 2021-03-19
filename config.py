#!/usr/bin/env python
# encoding: utf-8

import configparser, argparse
from pathlib import Path
from ast import literal_eval

class Config:

    def __init__(self):

        self.parser = argparse.ArgumentParser(description='PigePy is a script for recording audio stream')
        #self.configFile = self.parser.add_argument('--config-file', required=False, help='specify a config file')
        self.streamUrl = self.parser.add_argument('--stream', '-s', dest="stream", required=True, help='specify a stream url')
        self.basePath = self.parser.add_argument('--base-path', '-b', dest="basePath", required=True, type=self.verify_dir, help='Base destination directory absolute path.')
        self.dirFormat = self.parser.add_argument('--directory-format', '-df', dest="directoryFormat", default='%Y/%m/%d', help='sub directories structure in strftime format (default: "%%Y/%%m/%%d")')
        self.fileFormat = self.parser.add_argument('--file-format', '-ff', dest="filenameFormat", default="%Hh-%Mm-%Ss", help='filename format can contain strftime format (default: "%%Hh-%%Mm-%%Ss")')
        self.interval = self.parser.add_argument('--interval', '-i', dest="interval", default={"minutes": 60}, type=self.interval_validation, help='Audio files length kwargs format (default: {"minutes": 60})')
        #self.retentionBy = self.parser.add_argument('--retention-by', '-rb', required=True, default="days", help='retention by  (default=days)')
        #self.retention = self.parser.add_argument('--retention', '-r', required=True, default=90, help='Duration of how many time files should be keeped (default=90)')
        #self.retentionType = self.parser.add_argument('--retention-type', '-rt', required=True, default="days", help='retention type minutes/hours/days default=days')

        #self.args = self.parser.parse_args()

       # verifyBasePath = self.verify_dir(self.args.base_path)

    def verify_dir(self, dirPath):
        directory = Path(dirPath)
        if directory.exists() and directory.is_dir():
            print(f"ok directory : {dirPath} exist")
            return directory
        else:
            print(f"Error directory : {dirPath} don't exist")
            raise argparse.ArgumentTypeError(f"readable_dir:{dirPath} is not a valid path")

    def check_duration(self, value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(
                'Duration in minutes must be a positive integer.')

        if value < 1:
            raise argparse.ArgumentTypeError(
                'Duration in minutes must be a positive integer.')
        else:
            return value

    def interval_validation(self, value):
        print(value)
        accepted_key = ["days", "hours", "minutes", "seconds"]
        for key, val in literal_eval(value).items():
            print(key, val)
            if key  in accepted_key:
                pass
            else:
                raise argparse.ArgumentTypeError(f"{key} is not available")

            try:
                val = int(val)
            except ValueError:
                raise argparse.ArgumentTypeError('Duration in minutes must be a positive integer.')

            if val < 1:
                raise argparse.ArgumentTypeError('Duration in minutes must be a positive integer.')

        return literal_eval(value)