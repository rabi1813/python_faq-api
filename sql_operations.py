import datetime
import os
import json
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
from string_literals import SQL_CONSTANTS

class SQL_UTILITY_METHODS():
    __slots__ = ()

    def convert_datetime_to_string(self, records):
        if isinstance(records, list):
            for item in records:
                item = self.convert_dict_datetime_to_string(item)
        elif isinstance(records, dict):
            records = self.convert_dict_datetime_to_string(records)
        return records

    def convert_dict_datetime_to_string(self, records):
        for key, value in records.items():
            if isinstance(records[key], datetime.datetime):
                records[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        return records

class SQL_METHODS(SQL_UTILITY_METHODS, SQL_CONSTANTS):
    __slots__ = ()

    def mysql_connector(self):
        host = "localhost"
        user = "root"
        password = "Rabi@1991"
        db_name = "sakila"
        auto_commit_flag = True
        cursor_type = "dict"

        print()
        if cursor_type == "dict":
            cursor_class = pymysql.cursors.DictCursor
        else:
            cursor_class = pymysql.cursors.Cursor

        try:
            connection = pymysql.connect(host=host,
                                         user=user,
                                         password=password,
                                         db=db_name,
                                         charset='utf8mb4',
                                         cursorclass=cursor_class,
                                         client_flag=CLIENT.MULTI_STATEMENTS,
                                         autocommit=auto_commit_flag)
            print("Connected to db")
            return connection
        except Exception as e:
            print(str(e))
            exit(1)

    def execute_query(self, query, record_start=None, record_end=None):
        connection = self.mysql_connector()
        with connection.cursor() as cursor:
            print("Querying SQL : {0}".format(query))
            cursor.execute(query=query)

            sql_fetch = cursor.fetchall()
            result = self.convert_datetime_to_string(sql_fetch)
            return result

    def row_counter(self, connection, table):
        with connection.cursor() as cursor:
            query = self.TABLE_ROW_COUNTER.format(table)
            print("Querying SQL : {0}".format(query))
            cursor.execute(query=query)

            sql_fetch = cursor.fetchone()
            return sql_fetch.get("count")
