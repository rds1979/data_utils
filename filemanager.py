#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

try:
    import yaml
except ImportError as err:
    sys.stderr.write(f"Error {err} occured in module {__name__} file: {__file__}")
    sys.exit(1)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', \
                    datefmt='%Y-%m-%d %H:%M:%S', filemode='w', level=logging.INFO)


class FileManager:
    '''Description FileManager class'''
    def read_text_file(self, file: str) -> list:
        lines = []
        with open(file, 'r') as fd:
            for line in fd:
                line = line.replace("\n","")
                lines.append(line)
        return lines

    def read_yaml_config(self, file: str, section: str) -> dict:
        with open(file, 'r') as yaml_stream:
            fd = yaml.full_load(yaml_stream)
            if section in fd:
                settings = fd[section]
                return settings
            else:
                logging.error(f"Section {section} not find in the file {file}")
                sys.exit(2)
