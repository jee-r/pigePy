#!/usr/bin/env python
# encoding: utf-8

from recorder import Recorder

def main():
    # Config
    stream = "https://radioquetsch.out.airtime.pro/radioquetsch_a"
    basePath = "/tmp/pige"
    directoryFormat = "%Y_%m_%d-%Hh%Mm"
    filenameFormat = "%Ss"
    segmentDuration = 60
    retention = 90
    retentionBy = "minutes"

    recorder = Recorder(stream, segmentDuration)

    recorder.rec(stream, segmentDuration, basePath, directoryFormat, filenameFormat)

if __name__ == "__main__":
    main()
