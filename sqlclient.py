#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', \
                    datefmt='%Y-%m-%d %H:%M:%S', filemode='w', level=logging.INFO)

try:
    import psycopg2, psycopg2.extras as pcge
except ImportError as err:
    sys.stderr.write(f"Error {err} occured in module {__name__} file: {__file__}")
    sys.exit(1)
    

class SQLClient:
    '''Description SQLClient class'''
    def __init__(self,settings: dict) -> None:
        self.settings = settings
        try:
            self.conn = psycopg2.connect(**self.settings)
            self.curs = self.conn.cursor()
            logging.info(f"Established connect to database '{self.settings['database']}' on host '{self.settings['host']}'")
        except psycopg2.DatabaseError as err:
            logging.error(f"Couldn't establish connect to database '{self.settings['database']}' on host '{self.settings['host']}'")
            sys.exit(2)

    def execute_one(self, query: str, returning: bool) -> list:
        try:
            self.curs.execute(query)
            self.conn.commit()
            if returning:
                result = self.curs.fetchall()
                return result
        except psycopg2.DatabaseError as err:
            logging.error(f"Couldn't exequte query {query} because occured error '{err}'")
            sys.exit(2)

    def insert_batch(self, query_string: str, data: list) -> None:
        try:
            pcge.execute_batch(self.curs, query_string, data)
            self.conn.commit()
            logging.info("Batch insert rows successfully completed")
        except psycopg2.DatabaseError as err:
            logging.error(f"Couldn't exequte bulk insert because occured error '{err}'")
            sys.exit(2)

    def close_connection(self) -> None:
        if self.conn is not None:
            self.curs.close()
            self.conn.close()
            logging.info(f"Closed connect to database '{self.settings['database']}'on host '{self.settings['host']}'")
