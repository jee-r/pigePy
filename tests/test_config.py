#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")
from pathlib import Path
from pigepy.config import Config
import unittest


class TestArgs(unittest.TestCase):

    def setUp(self):
        self.stream = "http://localhost:30000"
        self.config = Config()

    def test_verify_dir(self):
        self.assertEqual(Path("/tmp"), self.config.verify_dir("/tmp"))
        with self.assertRaises(Exception): self.config.verify_dir(50)
        with self.assertRaises(Exception): self.config.verify_dir("ThisAString")
        with self.assertRaises(Exception): self.config.verify_dir("/this/path/dont/exist")

    def test_check_duration_(self):
        self.assertEqual(50, self.config.check_duration(50))
        with self.assertRaises(Exception): self.config.check_duration("aString")

    def test_interval_duration(self):
        self.assertEqual({'days': 5}, self.config.interval_validation("{'days': 5}"))
        with self.assertRaises(Exception): self.config.interval_validation(50)
        with self.assertRaises(Exception): self.config.interval_validation("{'years': 5}")
        with self.assertRaises(Exception): self.config.interval_validation({})
        with self.assertRaises(Exception): self.config.interval_validation("thisIsAString")
        with self.assertRaises(Exception): self.config.interval_validation("/this/path/dont/exist")

    def test_check_chunkSize(self):
        self.assertEqual(50, self.config.check_chunkSize(50))
        with self.assertRaises(Exception): self.config.check_chunkSize("aString")
    
    def test_check_prune_value(self):
        self.assertEqual(50, self.config.check_prune_value(50))
        with self.assertRaises(Exception): self.config.check_prune_value("aString")
    
    def test_check_cron_syntax(self):
        self.assertEqual("0 0 * * *", self.config.check_cron_syntax("0 0 * * *"))
        with self.assertRaises(Exception): self.config.check_cron_syntax(50)
        with self.assertRaises(Exception): self.config.check_cron_syntax("{'years': 5}")
        with self.assertRaises(Exception): self.config.check_cron_syntax({})
        with self.assertRaises(Exception): self.config.check_cron_syntax("thisIsAString")
        with self.assertRaises(Exception): self.config.check_cron_syntax("/this/path/dont/exist")

if __name__ == '__main__':
    unittest.main()
