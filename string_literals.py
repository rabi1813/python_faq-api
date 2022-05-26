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
    SELECT_ACTOR = "select * from actor"
    TABLE_ROW_COUNTER = "select count(*) as count from {0};"


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
    INVALID_METHOD = "Invalid Request Method"
    INVALID_CONTENT_TYPE = "Invalid Content-type"
    INVALID_HEADER = "Mandatory header missing : {0}"
    INVALID_PAYLOAD = "Internal Server Error"
    INVALID_RECORDS_VALUE = "Value of query param: '{0}' must be integer"
    ERROR_MESSAGE_TEMPLATE = message = {
        "error_message": ""
    }
