#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='data_utils',
    version='1.1.0',
    description='Data_utils package',
    author='Dmitriy Redkin',
    author_email='expert.info79@gmail.com',
    packages=['data_utils'],
    install_requires=['boto3', 'botocore', 'PyYaml', 'psycopg2']
)
