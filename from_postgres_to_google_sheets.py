#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', \
                    datefmt='%Y-%m-%d %H:%M:%S', filemode='w', level=logging.INFO)

try:
    import yaml, psycopg2, httplib2, pandas as pd
    import gspread, gspread_dataframe as gd
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError as err:
    logging.error(f"Error {err} occured in module '{__name__}', file '{__file__}'")
    sys.exit(2)

CREDENTIALS_FILE = 'storeez--data-0000001-699b8a426ee9.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE)
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']


class FileManager:
    '''Description FileManager class'''
    def read_text_file(self, file: str) -> list:
        lines = []
        with open(file, 'r') as fd:
            for line in fd:
                line = line.replace("\n", "")
                if "'" in line:
                    line = line.replace("'", ' ')
                lines.append(line)
        return lines

    def read_yaml_file(self, file: str, section: str) -> dict:
        with open(file, 'r') as yaml_stream:
            fd = yaml.full_load(yaml_stream)
            if section in fd:
                settings = fd[section]
                return settings
            else:
                logging.error(f"Section '{section}' not find in the file '{file}'")
                sys.exit(2)


class SQLClient:
    '''Description SQLClient class'''
    def __init__(self, dbsettings: dict) -> None:
        self.settings = dbsettings
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

    def close_connection(self) -> None:
        if self.conn is not None:
            self.curs.close()
            self.conn.close()
            logging.info(f"Closed connect to database '{self.settings['database']}'on host '{self.settings['host']}'")


def transform_data(dataset: list):
    columns_names = ['Идентификатор', 'Место', 'Ряд', 'По горизонтали', 'По вертикали', 'По глубине',
                     'Тип места', 'Вместимость', 'Добавил', 'Добавлено', 'Изменил', 'Изменено',
                     'Блокиновано ВЫХ.', 'Блокировано ВХ.', 'Инвентаризация']
    df = pd.DataFrame(dataset, columns=columns_names)
    df['Добавлено'] = df['Добавлено'].dt.strftime('%d.%m.%Y/%H:%M')
    df['Изменено'] = df['Изменено'].dt.strftime('%Y/%m/%d')
    df['Инвентаризация'] = df['Инвентаризация'].dt.strftime('%d.%m.%Y')
    return df


def populate_existing_sheet(export_data: list, spread_sheetid: str):
    gs = gspread.authorize(creds)
    sheet = gs.open_by_key(spread_sheetid)
    wsht = sheet.get_worksheet(0)
    wsht.clear()
    gd.set_with_dataframe(wsht, export_data)


def processing(file: str, section: str, spread_sheetid: str) -> None:
    fm = FileManager()
    dbsettings = fm.read_yaml_file(file, section)
    cli = SQLClient(dbsettings)
    query = f'''SELECT id, name, sector_id, col, row, depth, place_type_id, capacity, created_by, created_at, updated_by,
            updated_at, is_blocked_for_out, is_blocked_for_in, last_inventorization_at FROM core.place'''
    dataset = cli.execute_one(query, True)
    cli.close_connection()
    export_data = transform_data(dataset)
    populate_existing_sheet(export_data, spread_sheetid)


if __name__ == '__main__':
    config, section = 'config.yaml', 'postgres_esb_prod'
    spread_sheetid = '14PnkMMudVNo8Ki0vLsY9_Ib4f0NIqItbVxdKQwZo2Ng'
    processing(config, section, spread_sheetid)

# https://docs.google.com/spreadsheets/d/14PnkMMudVNo8Ki0vLsY9_Ib4f0NIqItbVxdKQwZo2Ng/edit#gid=0
