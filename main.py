import json

from flask import request

from utils import UTILITY_METHODS
from operations import GENERAL_OPERATIONS

utils_object = UTILITY_METHODS()
operations_object = GENERAL_OPERATIONS()

app = utils_object.generate_flask_app()


@app.route("/actor", methods=["GET"])
def home():
    request_details = utils_object.get_request_details(request)
    flag, request_details = utils_object.pre_check(request_details)
    if not flag:
        return request_details
    response = operations_object.get_actor(request_details)
    return response


app.run()
