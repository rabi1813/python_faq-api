"""
Main execution file
"""
from flask import request

from common_utils import CommonUtilsMethods
from utils import UtilityMethods
from operations import GeneralOperations

common_utils_object = CommonUtilsMethods()
utils_object = UtilityMethods()
operations_object = GeneralOperations()
app = common_utils_object.generate_flask_app()


@app.route("/actor", methods=["GET"])
def actor():
    """
    Function to get actor details
    :return: List of actors
    """
    request_details = common_utils_object.get_request_details(request)
    flag, request_details = utils_object.pre_check(request_details)
    if not flag:
        return request_details
    response = operations_object.get_actor(request_details)
    return response


if __name__ == "__main__":
    app.run()
