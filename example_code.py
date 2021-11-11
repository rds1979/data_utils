#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from data_utils.filemanager import FileManager
from data_utils.s3client import S3Client
from data_utils.sqlclient import SQLClient

def processing(yaml_config: str, ini_config: str) -> None:
    today = datetime.today().strftime('%Y-%m-%d')
    fm = FileManager()

    postgres_settings = fm.read_yaml_config(yaml_config, 'postgres')
    postgres_client = SQLClient(postgres_settings)
    query = f"SELECT * FROM cbrf.currency WHERE valute_load ='{today}';"
    currency = postgres_client.execute_one(query, True)
    postgres_client.close_connection()
    print(currency)

    greenplum_settings = fm.read_ini_config(ini_config, 'greenplum')
    greenplum_client = SQLClient(greenplum_settings)
    query = f"INSERT INTO cbrf.currency VALUES(%s, %s, %s, %s, %s, %s, %s)"
    greenplum_client.insert_batch(query, currency)
    greenplum_client.close_connection()

    s3settings = fm.read_yaml_config(yaml_config, 's3')
    s3cli = S3Client(s3settings)
    s3files, bucket = s3cli.get_info_from_s3('zip')
    print(bucket)

if __name__ == '__main__':
    yaml_config, ini_config = 'config.yaml', 'config.ini'
    processing(yaml_config, ini_config)

