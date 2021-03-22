#!/usr/bin/env python
# encoding: utf-8

import requests


class Healthcheck:
    """Healthcheck system"""

    def __init__(self, healthcheck_url):

        self.healthcheck_url = healthcheck_url
        self.req = requests.Session()

    def ping(self, check_name, msg):
        url = self.healthcheck_url
        post_data = {"msg": msg}

        try:
            response = self.req.post(url, data = post_data, timeout=10)
        except requests.RequestException as except_error_msg:
            print(f"Ping failed : {except_error_msg}")

        return response

    def fail(self, check_name, msg):
        url = self.healthcheck_url + "/fail"
        post_data = {"msg": msg}

        try:
            response = self.req.post(url, data = post_data, timeout=10)
        except requests.RequestException as except_error_msg:
            print(f"Ping failed : {except_error_msg}")

        return response

    def getCheckList(self):

        url = self.healthcheck_host + "/api/v1/checks/"
        headers={'X-Api-Key': self.apikey}
        response = self.req.get(url, headers=headers, timeout=10)
        jsonData = response.json()

        for item in jsonData["checks"]:
            self.healthcheck_urls[item["name"]] = item["ping_url"]


if __name__ == "__main__":
    main()
