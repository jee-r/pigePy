#!/usr/bin/env python
# encoding: utf-8

import sys
from datetime import datetime, timedelta
from pathlib import Path
from ast import literal_eval

class FileManager:
    """Manage files"""
    def __init__(self, basePath, directoryFormat, directoryDelta):

        self.basePath = Path(basePath)
        self.directoryFormat = directoryFormat
        self.directoryDelta = directoryDelta

    def createDir(self):
        now = datetime.now()
        delta = now + timedelta(**self.directoryDelta)
        today_dir = now.strftime(self.directoryFormat)
        delta_dir = delta.strftime(self.directoryFormat)
        today_full_path = str(self.basePath) + "/" + str(today_dir)
        delta_full_path = str(self.basePath) + "/" + str(delta_dir)

        try:
            if not Path(today_full_path).is_dir():
                Path(today_full_path).mkdir(parents=True, exist_ok=True)
                print(f"create directory : {today_full_path}")

            if not Path(delta_full_path).is_dir():
                Path(delta_full_path).mkdir(parents=True, exist_ok=True)
                print(f"create directory : {delta_full_path}")

        except Exception as ex:
            print(f"Create directory failed : {ex}")
