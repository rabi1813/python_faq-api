"""
SQL Related operations
"""
import datetime
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
from string_literals import SQLConstants, ErrorMessages
from common_utils import ValidationMethods
from security_operations import SecurityMethods

validation_object = ValidationMethods()
security_object = SecurityMethods()


class SQLUtilityMethods:
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


class SQLMethods(SQLUtilityMethods, SQLConstants, ErrorMessages):
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
        config_data = security_object.decrypted_config()

        if config_data.get("cursor_type") == "dict":
            cursor_class = pymysql.cursors.DictCursor
        else:
            cursor_class = pymysql.cursors.Cursor

        try:
            connection = pymysql.connect(host=config_data.get("host"),
                                         user=config_data.get("user"),
                                         password=config_data.get("password"),
                                         db=config_data.get("db_name"),
                                         charset='utf8mb4',
                                         cursorclass=cursor_class,
                                         client_flag=CLIENT.MULTI_STATEMENTS,
                                         autocommit=config_data.get("auto_commit_flag"))
            print("Connected to db")
            return True, connection
        except pymysql.err.OperationalError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                validation_type="db_connect",
                status_code=500
            )
            return response

    def execute_query(self, connection, query, payload=None):
        """
        Execute SQL query
        :param connection: MySQL Connector
        :param query: SQL Query
        :param payload: Query payload
        :return: Fetched details
        """
        try:
            with connection.cursor() as cursor:
                print(f'Querying SQL : {query}')
                payload = payload if payload else {}
                cursor.execute(query, payload)
                if "select" in query.lower():
                    sql_fetch = cursor.fetchall()
                    if not sql_fetch:
                        sql_fetch = self.generate_null_mapper(cursor)
                    result = self.convert_datetime_to_string(sql_fetch)
                    return True, result
                return True, ""
        except pymysql.err.OperationalError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                validation_type="id_generation",
                status_code=500
            )
            return response
        except pymysql.err.ProgrammingError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                validation_type="id_generation",
                status_code=500
            )
            return response

    def row_counter(self, connection, table):
        """
        Count number of rows in a table
        :param connection: MySQL Connector
        :param table: Table Name
        :return: Row Count of table
        """
        try:
            with connection.cursor() as cursor:
                query = self.TABLE_ROW_COUNTER.format(table)
                print(f'Querying SQL : {query}')
                cursor.execute(query=query)

                sql_fetch = cursor.fetchone()
                return True, sql_fetch.get("count")
        except pymysql.err.ProgrammingError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                status_code=500
            )
            return response

    def generate_id(self, connection, table_name):
        """
        Generate Unique ID
        :param connection: MySQL Connector
        :param table_name: Table Name
        :return: Generated Unique ID
        """
        generated_id = ""
        flag = False
        if table_name == self.MASTER_TABLE:
            print("Generating new Master ID")
            flag, generated_id = self.create_id(connection, self.MASTER_SEQ_TABLE, self.MASTER_PREFIX, self.MASTER_ID_ZERO_COUNT)
        return flag, generated_id

    @staticmethod
    def create_id(connection, seq_table, id_prefix, zero_fill_count):
        """
        Generate new sequence and create unique ID
        :param connection: MySQL Connector
        :param seq_table: Sequence Table Name
        :param id_prefix: Prefix of unique ID
        :param zero_fill_count: Zero Fill Count
        :return: Generated Unique ID
        """
        try:
            with connection.cursor as cursor:
                insert_qry = f"INSERT INTO {seq_table} VALUES (NULL);"
                print(f"Sequence table SQL : {insert_qry}")
                cursor.execute(insert_qry)

                fetch_qry = "select LAST_INSERT_ID() as id;"
                print(f"Last inserted ID Query: {fetch_qry}")
                cursor.execute(fetch_qry)
                for row in cursor:
                    row_num = row['id']

                id = id_prefix + (str(row_num).zfill(zero_fill_count))
                print(f"Generated ID : {id}")
                return True, id
        except pymysql.err.OperationalError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                validation_type="id_generation",
                status_code=500
            )
            return response
        except pymysql.err.ProgrammingError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                validation_type="id_generation",
                status_code=500
            )
            return response

    @staticmethod
    def generate_null_mapper(cursor):
        """
        Generate Null Mapper
        :param cursor: MySQl Cursor
        :return Null Mapper
        """
        null_mapper = [{item[0]: (0 if item[1] in range(6) else "") for item in cursor.description}]
        return null_mapper

    def pre_delete_check(self, connection, table_name, field_name, field_value):
        """
        Count number of rows in a table
        :param connection: MySQL Connector
        :param table_name: Table Name
        :param field_name: Where condition field name
        :param field_value: Where condition field value
        :return: Row Count of table
        """
        try:
            with connection.cursor() as cursor:
                query = self.PRE_DELETE.format(table_name, field_name, field_value)
                print(f'Pre-Delete Check Querying SQL : {query}')
                cursor.execute(query=query)
                sql_fetch = cursor.fetchone()
                count = sql_fetch.get("count")
                if count == 0:
                    message = self.PRE_DELETE_CHECK.format(field_value)
                    response = validation_object.generate_error_response(
                        validation_type="pre_delete_check",
                        message=message,
                        status_code=404
                    )
                    return response
                return True, ""
        except pymysql.err.ProgrammingError as exp:
            print(str(exp))
            response = validation_object.generate_error_response(
                status_code=500
            )
            return response
