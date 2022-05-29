"""
File to store all constant values
"""
import os


class Constants:
    """
    General Constants
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """

    ALLOWED_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
    MANDATORY_HEADERS = ["content-type"]
    JSON_CONTENT_TYPE = "application/json"
    GET_METHOD = "GET"
    NON_GET_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(FILE_DIR, "config", "config.yaml")


class SQLConstants:
    """
    SQL related constants
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """
    GET_LIST_WHERE_CONDITION = " where {0} between {1} and {2};"
    GET_LIST_ID_BASED = " where {0} = '{1}';"
    SELECT_QUERY = "select * from {0}"
    TABLE_ROW_COUNTER = "select count(*) as count from {0};"
    PRE_DELETE = "select count(*) as count from {0} where {1} = '{2}';"

    INSERT_MASTER_QUERY = "Insert into master (master_id, type, query, answer) values " \
                          "(%(master_id)s, %(type)s, %(query)s, %(answer)s);"
    DELETE_MASTER_QUERY = "Delete from master where master_id = (%(master_id)s;"
    MASTER_PREFIX = "MTR"
    MASTER_TABLE = "master"
    MASTER_SEQ_TABLE = "master_seq"
    MASTER_ID_ZERO_COUNT = 9


class ErrorMessages:
    """
    Error Messages
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """
    GENERAL_ERROR_MESSAGE = "Error Occurred"
    DB_CONNECTION_FAIL = "Failed to connect DB"
    ID_GENERATION_FAILURE = "Unique ID Generation Failed"
    PRE_DELETE_CHECK = "ID: {0} doesn't exist"
    INVALID_METHOD = "Invalid Request Method"
    INVALID_CONTENT_TYPE = "Invalid Content-type"
    INVALID_HEADER = "Mandatory header missing : {0}"
    INVALID_PAYLOAD = "Internal Server Error"
    INVALID_RECORDS_VALUE = "Value of query param: '{0}' must be integer"
    ERROR_MESSAGE_TEMPLATE = message = {}
