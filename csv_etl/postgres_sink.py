import psycopg2
from psycopg2 import extras
from csv_etl.extractor import extract_col, column_exists, insert_data
import pandas as pd

class Postgres:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.engine = None
        self.connection_string = None
        self.cursor = None
        self.connected()

    def connected(self):
        self.connection_string = "host='{host}' dbname='{database}' user='{username}' password='{password}' port='{port}'".format(
            host= self.config['host'],
            database= self.config['database'],
            username= self.config['username'],
            password= self.config['password'],
            port= self.config['port']
        )
        self.connection= psycopg2.connect(self.connection_string)
        self.cursor= self.connection.cursor(cursor_factory=extras.DictCursor)

    def load(self, data):
        schema= self.config['schema']
        table= self.config['table']
        insert_data(self.cursor, schema, table, data)
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        return