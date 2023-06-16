#!/usr/bin/env python
# encoding: utf-8

import logging
import sys
import shutil
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
                # print(f"create directory : {today_full_path}")
                logging.info("create directory : %s", today_full_path)

            if not Path(delta_full_path).is_dir():
                Path(delta_full_path).mkdir(parents=True, exist_ok=True)
                # print(f"create directory : {delta_full_path}")
                logging.info("create directory : %s", delta_full_path)

        except Exception as ex:
            # print(f"Create directory failed : {ex}")
            logging.exception("Create directory failed : %s", ex)

    def pruneOldDirectories(self, days=90):
        cutoff_date = datetime.now() - timedelta(days=days)
        for directory in self.basePath.iterdir():
            if directory.is_dir():
                try:
                    directory_date = datetime.strptime(directory.name, self.directoryFormat).date()
                    if directory_date < cutoff_date.date():
                        shutil.rmtree(directory)
                        logging.info("Removed directory: %s", directory)
                except Exception as ex:
                    logging.exception("Failed to remove directory: %s", directory)
