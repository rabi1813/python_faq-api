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

    def get_actor(self, request_details):
        """
        Function to get actor list
        :param request_details: API Request Details
        :return: If True, returns actor list
                 If False, returns Error
        """
        flag, connection = sql_object.mysql_connector()
        if flag is False:
            return connection
        method = request_details.get("method")
        if method == "GET":
            table_name = "actor"
            flag, request_details = utils_object.param_null_value_generator(
                connection=connection,
                request_details=request_details,
                table_name=table_name)
            if flag is False:
                return request_details
            query_params = request_details.get("query_params")
            record_start = query_params.get("record_start")
            record_end = query_params.get("record_end")
            query = self.SELECT_QUERY.format(table_name) + self.GET_LIST_WHERE_CONDITION.format("actor_id",
                                                                                                record_start,
                                                                                                record_end)
            data = utils_object.execute_query(connection, query)
            response = utils_object.generate_success_response(status_code=200, message=data)
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response

    def master_table_operations(self, request_details):
        """
        Function to perform master table operations
        :param request_details: API Request Details
        :return: If True, returns Success response
                 If False, returns Error response
        """

        flag, connection = sql_object.mysql_connector()
        if flag is False:
            return connection
        method = request_details.get("method")
        table_name = self.MASTER_TABLE
        if method == "POST":
            response = self.create_master_records(connection, request_details, table_name)
        elif method == "GET":
            response = self.get_master_records_list(connection, request_details, table_name)
        elif method == "DELETE":
            response = self.delete_master_records(connection, request_details, table_name)
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response

    def create_master_records(self, connection, request_details, table_name):
        """
        Create a Master records
        :param connection: MySQL Connector
        :param request_details: API Request Details
        :param table_name: Table name
        :return: If True, returns Master list
                 If False, returns Error response
        """
        payload = request_details.get("payload")
        headers = request_details.get("headers")
        id = sql_object.generate_id(connection, table_name)
        payload["master_id"] = id
        flag, response = utils_object.execute_query(connection, self.INSERT_MASTER_QUERY, payload)
        if flag is False:
            return response
        success_body = {
            "id"
            "message": f"Query ID: {id} generated successfully."
        }
        response = utils_object.generate_success_response(status_code=200, message=success_body)
        return response

    def get_master_records_list(self, connection, request_details, table_name):
        """
        Function to get Master records list
        :param connection: MySQL Connector
        :param request_details: API Request Details
        :param table_name: Table name
        :return: If True, returns Master list
                 If False, returns Error response
        """
        method = request_details.get("method")
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
            query = self.SELECT_QUERY.format(table_name) + self.GET_LIST_WHERE_CONDITION.format("master_id",
                                                                                                record_start,
                                                                                                record_end)
            flag, data = utils_object.execute_query(connection, query)
            response = utils_object.generate_success_response(status_code=200, message=data)
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response

    def delete_master_records(self, connection, request_details, table_name):
        """
        Create a Master records
        :param connection: MySQL Connector
        :param request_details: API Request Details
        :param table_name: Table name
        :return: If True, returns Master list
                 If False, returns Error response
        """
        payload = json.loads(request_details.get("payload"))
        headers = request_details.get("headers")
        master_id = payload["master_id"]
        flag, response = utils_object.pre_delete_check(connection, table_name, "master_id", master_id)
        if flag is False:
            return response
        flag, response = utils_object.execute_query(connection, self.DELETE_MASTER_QUERY, payload)
        if flag is False:
            return response
        success_body = {
            "id"
            "message": f"Query ID: {id} deleted successfully."
        }
        response = utils_object.generate_success_response(status_code=200, message=success_body)
        return response

    def get_master_records_details(self, master_id, request_details):
        """
        Function to get actor list
        :param master_id: Master ID
        :param request_details: API Request Details
        :return: If True, returns Master ID Details
                 If False, returns Error response
        """
        flag, connection = sql_object.mysql_connector()
        if flag is False:
            return connection
        method = request_details.get("method")
        table_name = self.MASTER_TABLE
        if method == "GET":
            query = self.SELECT_QUERY.format(table_name) + self.GET_LIST_ID_BASED.format("master_id",
                                                                                         master_id)
            flag, data = utils_object.execute_query(connection, query)
            response = utils_object.generate_success_response(status_code=200, message=data[0])
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response
