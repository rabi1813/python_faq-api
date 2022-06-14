"""
Main execution file
"""
from flask import request

from common_utils import CommonUtilsMethods
from utils import UtilityMethods
from operations import GeneralOperations
from log_services import log_initializer
from string_literals import Constants

common_utils_object = CommonUtilsMethods()
utils_object = UtilityMethods()
ops_object = GeneralOperations()
app = common_utils_object.generate_flask_app()

logger = log_initializer()


@app.route("/query", methods=["GET", "POST", "DELETE"])
def query():
    """
    Function to perform operations on master table
    :return: If True, returns Success response
             If False, returns Error response
    """
    request_details = common_utils_object.get_request_details(request)
    flag, request_details = utils_object.pre_check(request_details)
    if not flag:
        return request_details
    response = ops_object.table_operations(request_details,
                                           operation_type=Constants.QUERY_TABLE_OPERATION)
    return response


@app.route("/query/<query_id>", methods=["GET"])
def query_data(query_id):
    """
    Function to perform get query details based on query_id
    :return: If True, returns Success response
             If False, returns Error response
    """
    request_details = common_utils_object.get_request_details(request)
    flag, request_details = utils_object.pre_check(request_details)
    logger.info(flag, request_details)
    if flag is False:
        return request_details
    response = ops_object.get_records_details(query_id, request_details,
                                              operation_type=Constants.QUERY_TABLE_OPERATION)
    logger.info(response)
    return response


@app.route("/approval", methods=["GET", "POST", "DELETE"])
def approval():
    """
    Function to perform operations on master table
    :return: If True, returns Success response
             If False, returns Error response
    """
    request_details = common_utils_object.get_request_details(request)
    flag, request_details = utils_object.pre_check(request_details)
    if not flag:
        return request_details
    response = ops_object.table_operations(request_details,
                                           operation_type=Constants.PRE_APPROVAL_TABLE_OPERATION)
    return response


@app.route("/approval/<approval_id>", methods=["GET"])
def approval_data(approval_id):
    """
    Function to perform get Pre_approval details based on approval_id
    :return: If True, returns Success response
             If False, returns Error response
    """
    request_details = common_utils_object.get_request_details(request)
    flag, request_details = utils_object.pre_check(request_details)
    logger.info(flag, request_details)
    if flag is False:
        return request_details
    response = ops_object.get_records_details(approval_id, request_details,
                                              operation_type=Constants.PRE_APPROVAL_TABLE_OPERATION)
    logger.info(response)
    return response


if __name__ == "__main__":
    app.run()
