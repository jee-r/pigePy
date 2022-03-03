#!/usr/bin/env python
# encoding: utf-8

import logging
import sys
#sys.path.append("..")
import unittest
import warnings
from pigepy.scheduler import Scheduler

class Test(unittest.TestCase):

    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        self.interval = {"seconds": 10}
        # self.interval = {"minutes": 60}
        self.timezone = "utc"
        self.scheduler = Scheduler

    def test_scheduler_alignJob(self):

       print(self.scheduler.alignJob(self, self.interval))
        

