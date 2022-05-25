import json

from sql_operations import SQL_METHODS
from string_literals import SQL_CONSTANTS
from utils import UTILITY_METHODS

utils_object = UTILITY_METHODS()

class GENERAL_OPERATIONS(SQL_CONSTANTS):
    __slots__ = ()

    def get_actor(self, request_details):
        payload = request_details.get("payload")
        method = request_details.get("method")
        if method == "GET":
            table_name = "actor"
            request_details = utils_object.query_param_null_value_generator(table_name, request_details)
            print(json.dumps(request_details))
            query_params = request_details.get("query_params")
            record_start = query_params.get("record_start")
            record_end = query_params.get("record_end")
            query = self.SELECT_ACTOR + self.GET_LIST_WHERE_CONDITION.format("actor_id", record_start, record_end)
            data = utils_object.execute_query(query, record_start, record_end)
            response = utils_object.generate_success_response(200, data)
            return response


