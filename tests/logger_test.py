#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")
from pigepy.logger import Logger
import unittest


class TestLogger(unittest.TestCase):

    def setUp(self):
        self.logger_name = "Unit_Test_Logger_Name"
        self.logger_level = "INFO"
        self.logger_instance = Logger(self.logger_name, self.logger_level)
        self.logger = self.logger_instance.logger

    def test_logger_is_instance_of_module(self):
        self.assertIsInstance(self.logger_instance, Logger)

    def test_logger_name(self):
        self.assertEqual(self.logger_name, self.logger.name)

    def test_print_debug(self):
        self.logger.debug('DEBUG test message')
        self.logger.info('INFO test message')
        self.logger.critical('CRITICAL test message')

    def test_logger_level_is_correctly_set(self):
        levels = {
           10: "DEBUG",
           20: "INFO",
           30: "WARNING",
           40: "ERROR",
           50: "CRITICAL"
        }

        level = self.logger.level

        if level is None:
            levelname = levels[20]
        else:
            levelname = levels[int(level)]

        self.assertEqual(self.logger_level, levelname)


#    def test_check_duration_(self):
#        self.assertEqual(50, self.config.check_duration(50))
#        with self.assertRaises(Exception): self.config.check_duration("aString")
#
#    def test_interval_duration(self):
#        self.assertEqual({'days': 5}, self.config.interval_validation("{'days': 5}"))
#        with self.assertRaises(Exception): self.config.interval_validation(50)
#        with self.assertRaises(Exception): self.config.interval_validation("{'years': 5}")
#        with self.assertRaises(Exception): self.config.interval_validation({})
#        with self.assertRaises(Exception): self.config.interval_validation("thisIsAString")
#        with self.assertRaises(Exception): self.config.interval_validation("/this/path/dont/exist")
#
#    def test_check_chunkSize(self):
#        self.assertEqual(50, self.config.check_chunkSize(50))
#        with self.assertRaises(Exception): self.config.check_chunkSize("aString")

if __name__ == '__main__':
    unittest.main()
