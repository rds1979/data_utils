#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

try:
    import boto3, botocore
except ImportError as err:
    sys.stderr.write(f"Error {err} occured in module {__name__} file: {__file__}")
    sys.exit(1)

class S3Client:
    def __init__(self, settings: dict) -> None:
        self.settings = settings
        self.bucket_name = self.settings['bucket']
        self.resource = boto3.resource('s3',
        aws_access_key_id = self.settings['aws_access_key_id'],
        aws_secret_access_key = self.settings['aws_secret_access_key'])

    def get_info_from_s3(self, staging_dir: str) -> list:
        try:
            bucket = self.resource.Bucket(self.bucket_name)
            s3files = []
            for s3unit in bucket.objects.filter(Prefix=staging_dir):
                s3file = s3unit.key
                s3files.append(s3file)
                result = (s3files)
            return result
        except botocore.exceptions.ClientError as err:
            logging.err(f"{err} Module: '{__name__}'. File: '{__file__}'")
            sys.exit(2)
