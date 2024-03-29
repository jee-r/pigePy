#!/usr/bin/env python
# encoding: utf-8

import sys 
import os
#sys.path.append("..")
import unittest
import warnings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pigepy.healthcheck import Healthcheck


class TestHealthcheck(unittest.TestCase):


    def setUp(self):
        self.healthcheck = Healthcheck("https://hc-ping.com/eb095278-f28d-448d-87fb-7b75c171a6aa")

    def test_ping_healtcheck(self):
        """Test ping connection"""
        warnings.simplefilter('ignore', category=ResourceWarning)
        result = self.healthcheck.ping('main', "this is a test")

        self.assertEqual(200, result.status_code)
        self.assertEqual("OK (not found)", result.text)

    def test_fail_healthcheck(self):
        """Test fail connection"""
        warnings.simplefilter('ignore', category=ResourceWarning)
        result = self.healthcheck.fail('main', "this is a test")

        self.assertEqual(200, result.status_code)
        self.assertEqual("OK (not found)", result.text)


    def test_ping_healtcheck_with_fake_url(self):
        """Test ping connection with a fake url (404 handling)"""
        self.healthcheck.healthcheck_url = "https://hc-ping.com/this_url_dont_exist"
        warnings.simplefilter('ignore', category=ResourceWarning)
        result = self.healthcheck.ping('main', "this is a test")

        self.assertEqual(400, result.status_code)
        self.assertEqual("invalid url format", result.text)

    def test_fail_healthcheck_with_fake_url(self):
        """Test fail connection with a fake url (404 handling)"""
        self.healthcheck.healthcheck_url = "https://hc-ping.com/this_url_dont_exist"
        warnings.simplefilter('ignore', category=ResourceWarning)
        result = self.healthcheck.fail('main', "this is a test")

        self.assertEqual(400, result.status_code)
        self.assertEqual("invalid url format", result.text)


if __name__ == '__main__':
    unittest.main()
