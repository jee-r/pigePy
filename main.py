#!/usr/bin/env python
# encoding: utf-8

from recorder import Recorder

def main():

    # Config
    stream = "https://radioquetsch.out.airtime.pro/radioquetsch_a"
    basePath = "/tmp/pige"
    directoryFormat = "%Y/%m/%d/%H/%M"
    filenameFormat = "%H_%M_%S"
    segmentDuration = 60
    retention = 90
    retentionBy = "minutes"

    recorder = Recorder(stream, segmentDuration)

    recorder.rec(args.stream, args.segment_duration, args.base_path, args.directory_format, args.file_format)

if __name__ == "__main__":
    main()
