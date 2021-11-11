#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

try:
    import yaml
    from configparser import ConfigParser
    from configparser import NoSectionError
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

    def read_csv_file(self, file: str) -> list:
        data = []
        with open(file, encoding='utf8', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')
            for line in reader:
                data.append(line)
            return data

    def read_yaml_config(self, file: str, section: str) -> dict:
        with open(file, 'r') as yaml_stream:
            fd = yaml.full_load(yaml_stream)
            if section in fd:
                settings = fd[section]
                return settings
            else:
                logging.error(f"Section {section} not find in the file {file}")
                sys.exit(2)

    def read_ini_config(self, file: str, section: str) -> dict:
        try:
            configuration = {}
            parser = ConfigParser()
            parser.read(file)
            if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                    configuration[param[0]] = param[1]
                return configuration
        except NoSectionError as err:
            logging.error(f"The file {self.file} hasn't section {section}")
            sys.exit(2)


if __name__ == '__main__':
    print(f"You are ran content from '{__file__}' data_utils library")
    
