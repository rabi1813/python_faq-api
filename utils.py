"""
Utility methods
"""
from sql_operations import SQLMethods
from common_utils import ValidationMethods
from string_literals import Constants, SQLConstants


class UtilityMethods(SQLMethods, ValidationMethods):
    """
    Utility methods
    """
    __slots__ = ()

    def param_null_value_generator(self, connection, request_details, table_name=None):
        """
        Check if query param values are null and update the values according
        :param connection MySQL Connector
        :param request_details: API request details
        :param table_name: Table name
        :return: API request details with updated query params
        """
        query_params = request_details.get("query_params")
        record_start = query_params.get("record_start")
        record_end = query_params.get("record_end")
        flag, table_row_count = self.row_counter(connection, table_name)

        if flag is False:
            return flag, table_row_count
        if record_start is None:
            query_params['record_start'] = 0
        else:
            query_params['record_start'] = int(query_params['record_start'])
        if record_end is None:
            query_params['record_end'] = table_row_count
        else:
            query_params['record_end'] = int(query_params['record_end'])
        return True, request_details

    @staticmethod
    def table_differentiator(operation_type):
        operation_details = {}
        if operation_type == Constants.QUERY_TABLE_OPERATION:
            operation_details["table_name"] = SQLConstants.QUERY_TABLE
            operation_details["type"] = Constants.QUERY_TABLE_OPERATION
            operation_details["field_name"] = SQLConstants.QUERY_ID
        elif operation_type == Constants.PRE_APPROVAL_TABLE_OPERATION:
            operation_details["table_name"] = SQLConstants.PRE_APPROVAL_TABLE
            operation_details["type"] = Constants.PRE_APPROVAL_TABLE_OPERATION
            operation_details["field_name"] = SQLConstants.PRE_APPROVAL_ID
        return operation_details
