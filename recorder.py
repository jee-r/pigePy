#!/usr/bin/env python
# encoding: utf-8

from subprocess import Popen, PIPE
from datetime import datetime

class Recorder:
    """Record live stream"""

    def __init__(self, streamUrl, segmentDuration):
        self.stream = streamUrl
        self.segmentDuration = segmentDuration

        print(self.segmentDuration)

    def rec(self, stream, interval, basePath, dirFormat, fileFormat):
        now = datetime.now()
        dest = str(basePath) + "/" +str(dirFormat) + "/" + str(fileFormat) + ".mp3"

        try:
            record = Popen(['ffmpeg', '-i', stream, '-codec:a', 'libmp3lame', '-qscale:a', '3', '-f', 'segment', '-strftime', '1', '-segment_time', str(interval), '-segment_list', 'list.csv', '-segment_list_flags', 'cache', dest], stdout=PIPE, bufsize=1)
            record.wait()
        except KeyboardInterrupt:
            record.terminate()


