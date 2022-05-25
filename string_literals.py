

class CONSTANTS():
    __slots__ = ()
    ALLOWED_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
    MANDATORY_HEADERS = ["content-type"]
    JSON_CONTENT_TYPE = "application/json"
    GET_METHOD = "GET"
    NON_GET_METHODS = ["POST", "PUT", "PATCH", "DELETE"]


class SQL_CONSTANTS():
    __slots__ = ()
    GET_LIST_WHERE_CONDITION = " where {0} between {1} and {2};"
    SELECT_ACTOR = "select * from actor"
    TABLE_ROW_COUNTER = "select count(*) as count from {0};"


class ERROR_MESSAGE:
    __slots__ = ()
    GENERAL_MESSAGE = "Error Occured"
    INVALID_METHOD = "Invalid Request Method"
    INVALID_CONTENT_TYPE = "Invalid Content-type"
    INVALID_HEADER = "Mandatory header missing : {0}"
    INVALID_PAYLOAD = "Internal Server Error"
    INVALID_RECORDS_VALUE = "Value of query param: '{0}' must be integer"
    ERROR_MESSAGE_TEMPLATE = message = {
        "error_message": ""
    }


