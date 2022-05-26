"""
SQL Related operations
"""
import datetime
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
from string_literals import SQLConstants
from common_utils import ValidationMethods

validation_object = ValidationMethods()

class SQLUtilityMethods():
    """
    Methods for SQL Utility operations
    """
    __slots__ = ()

    def convert_datetime_to_string(self, records):
        """
        Convert all the datetime values to string
        :param records: Records fetched from DB/Request payload
        :return: Records with updated values
        """
        if isinstance(records, list):
            for item in records:
                item = self.convert_dict_datetime_to_string(item)
        elif isinstance(records, dict):
            records = self.convert_dict_datetime_to_string(records)
        return records

    @staticmethod
    def convert_dict_datetime_to_string(records):
        """
        Convert all the datetime values to string in a record of dictionary type
        :param records: Records fetched from DB/Request payload
        :return: Records with updated values
        """
        for key, value in records.items():
            if isinstance(records[key], datetime.datetime):
                records[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        return records

class SQLMethods(SQLUtilityMethods, SQLConstants):
    """
    Methods for SQL operations
    """
    __slots__ = ()

    @staticmethod
    def mysql_connector():
        """
        Creates MySQL Connector
        :return: MySQL Connector object
        """
        host = "localhost"
        user = "root3"
        password = "Rabi@1991"
        db_name = "sakila"
        auto_commit_flag = True
        cursor_type = "dict"

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
            return True, connection
        except pymysql.err.OperationalError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                validation_type="db_connect",
                status_code=500
            )
            return response

    def execute_query(self, connection, query):
        """
        Execute SQL query
        :param connection: MySQL Connector
        :param query: SQL Query
        :return: Fetched details
        """
        with connection.cursor() as cursor:
            print(f'Querying SQL : {query}')
            cursor.execute(query=query)

            sql_fetch = cursor.fetchall()
            result = self.convert_datetime_to_string(sql_fetch)
            return result

    def row_counter(self, connection, table):
        """
        Count number of rows in a table
        :param connection: MySQL Connector
        :param table: Table Name
        :return: Row Count of table
        """
        with connection.cursor() as cursor:
            query = self.TABLE_ROW_COUNTER.format(table)
            print(f'Querying SQL : {query}')
            cursor.execute(query=query)

            sql_fetch = cursor.fetchone()
            return sql_fetch.get("count")
