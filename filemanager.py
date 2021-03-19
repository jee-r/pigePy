#!/usr/bin/env python
# encoding: utf-8

import sys
from datetime import datetime, timedelta
from pathlib import Path
from ast import literal_eval

class FileManager:
    """Manage files"""
    def __init__(self, basePath, directoryFormat):

        self.basePath = Path(basePath)
        self.directoryFormat = directoryFormat

    def createDir(self):
        timeDeltaArg = {self.retentionBy: self.interval}
        directory_day = datetime.now() + timedelta(**timeDeltaArg)
        delta_dir = directory_day.strftime(self.directoryFormat)
        Path(str(self.basePath) + "/" + str(delta_dir)).mkdir(parents=True, exist_ok=True)
        print("create directory : {str(self.basePath)}/{str(delta_dir)}")
