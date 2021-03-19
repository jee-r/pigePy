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
        #timeDeltaArg = {self.retentionBy: self.interval}
        directory_day = datetime.now() + timedelta(**self.directoryDelta)
        delta_dir = directory_day.strftime(self.directoryFormat)
        Path(str(self.basePath) + "/" + str(delta_dir)).mkdir(parents=True, exist_ok=True)
        print(f"create directory : {str(self.basePath)}/{str(delta_dir)}")
