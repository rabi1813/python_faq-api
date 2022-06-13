"""
All route functions are written here
"""
import json

from string_literals import SQLConstants
from utils import UtilityMethods
from sql_operations import SQLMethods

utils_object = UtilityMethods()
sql_object = SQLMethods()


class GeneralOperations(SQLConstants):
    """
    Class which contains all the major functions of route
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    def table_operations(self, request_details, operation_type):
        """
        Function to perform table operations
        :param request_details: API Request Details
        :param operation_type: Operation Type
        :return: If True, returns Success response
                 If False, returns Error response
        """
        flag, connection = sql_object.mysql_connector()
        operation_details = utils_object.table_differentiator(operation_type)
        if flag is False:
            return connection
        method = request_details.get("method")
        if method == "POST":
            response = self.create_records(connection, request_details, operation_details)
        elif method == "GET":
            response = self.get_records_list(connection, request_details, operation_details)
        elif method == "DELETE":
            response = self.delete_records(connection, request_details, operation_details)
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response

    def create_records(self, connection, request_details, operation_details):
        """
        Create a new records
        :param connection: MySQL Connector
        :param request_details: API Request Details
        :param operation_details: Operation metadata
        :return: If True, returns Master list
                 If False, returns Error response
        """
        payload = json.loads(request_details.get("payload"))
        headers = request_details.get("headers")
        table_name = operation_details.get("table_name")
        field_name = operation_details.get("field_name")
        print(operation_details)
        flag, generated_id = sql_object.generate_id(connection, table_name)
        if flag is False:
            return generated_id
        payload[field_name] = generated_id
        print(payload)
        print(operation_details)
        print(self.INSERT_TABLE.format(**operation_details))
        flag, response = utils_object.execute_query(connection,
                                                    self.INSERT_TABLE.format(**operation_details),
                                                    payload)
        if flag is False:
            return response
        success_body = {
            "id": generated_id,
            "message": f"{operation_details.get('type')} ID: {generated_id} generated successfully."
        }
        response = utils_object.generate_success_response(status_code=200, message=success_body)
        return response

    def get_records_list(self, connection, request_details, operation_details):
        """
        Function to get Master records list
        :param connection: MySQL Connector
        :param request_details: API Request Details
        :param operation_details: Operation metadata
        :return: If True, returns Master list
                 If False, returns Error response
        """
        method = request_details.get("method")
        table_name = operation_details.get("table_name")
        field_name = operation_details.get("field_name")
        if method == "GET":
            flag, request_details = utils_object.param_null_value_generator(
                connection=connection,
                request_details=request_details,
                table_name=table_name)
            if flag is False:
                return request_details
            query_params = request_details.get("query_params")
            record_start = query_params.get("record_start")
            record_end = query_params.get("record_end")
            query = self.SELECT_QUERY.format(table_name) + \
                self.GET_LIST_WHERE_CONDITION.format(field_name, record_start, record_end)
            flag, data = utils_object.execute_query(connection, query)
            response = utils_object.generate_success_response(status_code=200, message=data)
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response

    def delete_records(self, connection, request_details, operation_details):
        """
        Create a Master records
        :param connection: MySQL Connector
        :param request_details: API Request Details
        :param operation_details: Operation metadata
        :return: If True, returns Master list
                 If False, returns Error response
        """
        payload = json.loads(request_details.get("payload"))
        headers = request_details.get("headers")

        table_name = operation_details.get("table_name")
        field_name = operation_details.get("field_name")
        operation_details["field_value"] = payload.get(field_name)
        field_value = payload.get(field_name)
        flag, response = utils_object.pre_delete_check(connection, table_name,
                                                       field_name, field_value)
        if flag is False:
            return response
        flag, response = utils_object.execute_query(connection,
                                                    self.DELETE_TABLE.format(**operation_details))
        if flag is False:
            return response
        success_body = {
            "id": field_value,
            "message": f"{operation_details.get('type')} ID: {field_value} deleted successfully."
        }
        response = utils_object.generate_success_response(status_code=200, message=success_body)
        return response

    def get_records_details(self, fetch_id, request_details, operation_type):
        """
        Function to get actor list
        :param fetch_id: ID value to fetch details from DB
        :param request_details: API Request Details
        :param operation_type: Operation Type
        :return: If True, returns Master ID Details
                 If False, returns Error response
        """
        flag, connection = sql_object.mysql_connector()
        operation_details = utils_object.table_differentiator(operation_type)
        if flag is False:
            return connection
        method = request_details.get("method")
        table_name = operation_details.get("table_name")
        field_name = operation_details.get("field_name")
        if method == "GET":
            query = self.SELECT_QUERY.format(table_name) + \
                self.GET_LIST_ID_BASED.format(field_name, fetch_id)
            flag, data = utils_object.execute_query(connection, query)
            response = utils_object.generate_success_response(status_code=200, message=data[0])
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response
