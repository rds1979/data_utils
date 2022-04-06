#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', \
                    datefmt='%Y-%m-%d %H:%M:%S', filemode='w', level=logging.INFO)

try:
    from clickhouse_driver import Client
except ImportError as err:
    logging.error(f"Error {err} occured in module {__name__} file: {__file__}")
    sys.exit(1)

class ClickClient:
    '''Description SQLClient class'''
    def __init__(self, settings: dict) -> None:
        self.host = settings['host']
        self.user = settings['user']
        self.pswd = settings['password']
        self.base = settings['database']

        self.auth = (('user', self.user),
                     ('password', self.pswd),
                     ('database', self.base))

        self.client = Client(host = self.host,
                             user = self.user,
                             password = self.pswd,
                             database = self.base)

    def client_native_select(self, query: str) -> list:
        result = self.client.execute(query)
        return result

    def external_tools_select(self, query: str) -> list:
        result = requests.post(self.host, data=query, params=self.auth, timeout=800)
        return result


if __name__ == '__main__':
    print(f"You are ran content from '{__file__}' data_utils library")
