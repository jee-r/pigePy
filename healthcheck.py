#!/usr/bin/env python
# encoding: utf-8

import requests

class Healthcheck:
    """Healthcheck system"""
    def __init__(self, apikey, host):

        self.apikey = apikey
        self.healthcheck_host = host

        self.req = requests.Session()

        self.getCheckList()

    def ping(self, check_name, msg):

        url = self.healthcheck_urls[check_name]
        post_data = {"msg": msg}

        try:
            response = self.req.post(url, data = post_data, timeout=10)
            print(response)
        except requests.RequestException as except_error_msg:
            print(f"Ping failed : {except_error_msg}")

    def fail(self, check_name, msg):

        url = self.healthcheck_urls[check_name] + "/fail"
        post_data = {"msg": msg}

        try:
            response = self.req.post(url, data = post_data, timeout=10)
            print(response)
        except requests.RequestException as except_error_msg:
            print(f"Ping failed : {except_error_msg}")

    def getCheckList(self):

        self.healthcheck_urls = {"main": "", "recorder": "", "filemanager": ""}

        url = self.healthcheck_host + "/api/v1/checks/"
        headers={'X-Api-Key': self.apikey}
        response = self.req.get(url, headers=headers, timeout=10)
        jsonData = response.json()

        for item in jsonData["checks"]:
            self.healthcheck_urls[item["name"]] = item["ping_url"]

def main():

    import sys

    healthcheck_apikey = sys.argv[1]
    healthcheck_host = sys.argv[2]

    #print(args.healthcheck_urls["main"])
    healthcheck = Healthcheck(healthcheck_apikey, healthcheck_host)
    healthcheck.getCheckList()
    healthcheck.ping('main', "ping main")
    healthcheck.fail('main', "failed main")

if __name__ == "__main__":

    main()


