#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from data_utils.filemanager import FileManager
from data_utils.s3client import S3Client
from data_utils.sqlclient import SQLClient

def processing(config: str) -> None:
    today = datetime.today().strftime('%Y-%m-%d')
    fm = FileManager()

    dbsettings = fm.read_yaml_config(config, 'postgres')
    cli = SQLClient(dbsettings)
    query = f"SELECT * FROM cbrf.currency WHERE valute_load ='{today}';"
    res = cli.execute_one(query, True)
    cli.close_connection()
    print(res)

    s3settings = fm.read_yaml_config(config, 's3')
    s3cli = S3Client(s3settings)
    s3files = s3cli.get_info_from_s3('zip')
    print(s3files)


if __name__ == '__main__':
    config = 'config.yaml'
    processing(config)
