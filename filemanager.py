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
        self.interval = 1
        self.retentionBy = "minutes"
#        self.fileFormat = fileFormat
#        self.segmentDuration = segmentDuration
#
#        self.interval = segmentDuration
#        self.retentionBy = retentionBy
#        self.retention = retention

        #print(list(self.retention.items())[0][0])
        #print(self.retention["1"])

    def createOneDir(self):
        print("create directory")
        timeDeltaArg = {self.retentionBy: self.interval}
        directory_day = datetime.now() + timedelta(**timeDeltaArg)
        delta_dir = directory_day.strftime(self.directoryFormat)
        Path(str(self.basePath) + "/" + str(delta_dir)).mkdir(parents=True, exist_ok=True)

    def createDir(self):
        for dirInterval in range(self.interval):
            timeDeltaArg = {self.retentionBy: dirInterval}
            directory_day = datetime.now() + timedelta(**timeDeltaArg)
            delta_dir = directory_day.strftime(self.directoryFormat)
            Path(str(self.basePath) + "/" + str(delta_dir)).mkdir(parents=True, exist_ok=True)

    def createDirInPast(self):
        now = datetime.now()
        for days in range(90):
            directory_day = datetime.now() - timedelta(minutes=days)
            delta_dir = directory_day.strftime("%Y/%m/%d/%H/%M")
            Path("/tmp/pige/" + delta_dir).mkdir(parents=True, exist_ok=True)

    def deleteDir(self):
        print("dir to delete")

        directoriesToKeep = []

        for dirInterval in range(self.interval):
            timeDeltaArg = {self.retentionBy: dirInterval}
            deltaDir = datetime.now() - timedelta(**timeDeltaArg)
            print(deltaDir)

            directoryToKeepByMinute = str(self.basePath) + "/" + str(deltaDir.strftime("%Y/%m/%d/%H/%M"))
            directoryToKeepByHour = str(self.basePath) + "/" + str(deltaDir.strftime("%Y/%m/%d/%H"))
            directoryToKeepByDay = str(self.basePath) + "/" + str(deltaDir.strftime("%Y/%m/%d"))
            directoryToKeepByMonth = str(self.basePath) + "/" + str(deltaDir.strftime("%Y/%m"))
            directoryToKeepByYear = str(self.basePath) + "/" + str(deltaDir.strftime("%Y"))

            if str(directoryToKeepByMinute) not in directoriesToKeep:
                directoriesToKeep.append(directoryToKeepByMinute)

            if str(directoryToKeepByHour) not in directoriesToKeep:
                directoriesToKeep.append(directoryToKeepByHour)

            if str(directoryToKeepByMonth) not in directoriesToKeep:
                directoriesToKeep.append(directoryToKeepByMonth)

            if str(directoryToKeepByYear) not in directoriesToKeep:
                directoriesToKeep.append(directoryToKeepByYear)

            directoriesToKeep.append(directoryToKeepByDay)

        print(directoriesToKeep)


        for dir in self.basePath.rglob("*"):
            if str(dir) in directoriesToKeep:
                print("keep this dir :" + str(dir))
#            else:
#                print("delete : " + str(dir))

