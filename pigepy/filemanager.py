#!/usr/bin/env python
# encoding: utf-8

import logging
import sys
import os
import shutil
import re
from datetime import datetime, timedelta
from pathlib import Path
from ast import literal_eval


class FileManager:
    """Manage files"""

    def __init__(self, basePath, directoryFormat):

        logging.debug('FileManager: Initializing...')
        
        self.basePath = Path(basePath)
        self.directoryFormat = directoryFormat
        # self.directoryDelta = directoryDelta
        
        logging.debug('FileManager: Initialized')

    def createDir(self, directoryDelta):
        now = datetime.now()
        delta = now + timedelta(**directoryDelta)
        today_dir = now.strftime(self.directoryFormat)
        delta_dir = delta.strftime(self.directoryFormat)
        today_full_path = str(self.basePath) + "/" + str(today_dir)
        delta_full_path = str(self.basePath) + "/" + str(delta_dir)

        try:
            if not Path(today_full_path).is_dir():
                Path(today_full_path).mkdir(parents=True, exist_ok=True)
                logging.info("create directory : %s", today_full_path)

            if not Path(delta_full_path).is_dir():
                Path(delta_full_path).mkdir(parents=True, exist_ok=True)
                logging.info("create directory : %s", delta_full_path)

        except Exception as ex:
            logging.exception("Create directory failed : %s", ex)


    def prune_old_files(self, directoryFormat, fileFormat, noSubDir, retention):
        retention_days = retention.get("days", 0)  # Get the value of "days" or use 0 if it's not set
        retention_hours = retention.get("hours", 0)  # Get the value of "hours" or use 0 if it's not set
        retention_minutes = retention.get("minutes", 0)  # Get the value of "minutes" or use 0 if it's not set

        cutoff_date = datetime.now() - timedelta(days=retention_days, hours=retention_hours, minutes=retention_minutes)

        logging.info(f"Pruning files older than: {cutoff_date}")
        
        files_to_remove = []

        if noSubDir:
            for file in Path(self.basePath).iterdir():
                if file.is_file():
                    try: 
                        file_date_str = Path(file).name.split('.')[0]
                        file_date = datetime.strptime(file_date_str, fileFormat)

                        if file_date < cutoff_date:
                            logging.info(f"remove file: {file} is older than {cutoff_date}")
                            files_to_remove.append(file)
                            # os.remove(file)
                            
                    except ValueError:
                        logging.error(f"Invalid date format for file: {file}")
                        continue
            for file in files_to_remove:
                os.remove(file)
            
        if not noSubDir:
            full_date_format = directoryFormat + "/" + fileFormat
            datetime.strptime
            for file in Path(self.basePath).rglob('*'):
                if file.is_file():
                    relative_path = Path(file).relative_to(self.basePath)
                    dated_file = Path(relative_path).with_suffix('')
                    print("daed :", dated_file)
                    try:
                        file_date = datetime.strptime(str(dated_file), full_date_format)
                        if file_date < cutoff_date:
                            logging.info(f"file: {file} is older than {cutoff_date}")
                            files_to_remove.append(file)
                            # os.remove(file)

                        continue
                    except ValueError:
                        logging.error(f"Invalid date format for file: {file}")
                        continue
        
            for file in files_to_remove:
                os.remove(file)
                parent_dir = file.parent
                if parent_dir.exists() and parent_dir.is_dir() and not any(parent_dir.iterdir()):
                    logging.info(f"Removing parent directory: {parent_dir} as it is empty")
                    parent_dir.rmdir()