"""
All route functions are written here
"""
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
            request_details = utils_object.param_null_value_generator(
                connection=connection,
                request_details=request_details,
                table_name=table_name)
            query_params = request_details.get("query_params")
            record_start = query_params.get("record_start")
            record_end = query_params.get("record_end")
            query = self.SELECT_ACTOR + self.GET_LIST_WHERE_CONDITION.format("actor_id",
                                                                             record_start,
                                                                             record_end)
            data = utils_object.execute_query(connection, query)
            response = utils_object.generate_success_response(status_code=200, message=data)
        else:
            response = utils_object.generate_error_response(validation_type="method")
        return response
