import json

import flask

from string_literals import CONSTANTS, ERROR_MESSAGE
from sql_operations import SQL_METHODS


class ValidationMethods(CONSTANTS, ERROR_MESSAGE):
    __slots__ = ()

    def pre_check(self, request_details):
        flag = self.validate_method(request_details)
        if not flag:
            return self.generate_error_response("method")
        flag, message = self.validate_header(request_details)
        if not flag:
            return self.generate_error_response("header", message)
        flag = self.validate_content_type(request_details)
        if not flag:
            return self.generate_error_response("content_type")
        flag = self.validate_payload(request_details)
        if not flag:
            return self.generate_error_response("payload", status_code=500)
        flag, message = self.validate_query_params(request_details)
        if not flag:
            return self.generate_error_response("query_params", message)
        return True, request_details

    def generate_error_response(self, request_detail_type, message=None, status_code=400):

        if request_detail_type == "method":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.INVALID_METHOD
        elif request_detail_type == "content_type":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.INVALID_CONTENT_TYPE
        elif request_detail_type == "header":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = message
        elif request_detail_type == "payload":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.INVALID_PAYLOAD
        elif request_detail_type == "query_params":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = message
        print(self.ERROR_MESSAGE_TEMPLATE)
        return False, flask.Response(json.dumps(self.ERROR_MESSAGE_TEMPLATE), status=status_code, mimetype='application/json')

    def generate_success_response(self, status_code, message):
        return flask.Response(json.dumps(message), status=status_code, mimetype='application/json')

    def validate_method(self, request_details):
        flag = False
        method = request_details.get("method")
        if method.upper() in self.ALLOWED_METHODS:
            flag = True
        return flag

    def validate_header(self, request_details):
        headers = [item for item in request_details.get("headers").keys()]
        missing_header = list()
        for header in self.MANDATORY_HEADERS:
            if header not in headers:
                missing_header.append(header)
        if missing_header:
            message = ", ".join(missing_header)
            message = self.INVALID_HEADER.format(message)
            return False, message
        else:
            return True, ""

    def validate_content_type(self, request_details):
        content_type = request_details.get("headers").get("content-type")
        flag = False
        if content_type == self.JSON_CONTENT_TYPE:
            flag = True
        return flag

    def validate_payload(self, request_details):
        method = request_details.get("method")
        if method in self.NON_GET_METHODS:
            payload = request_details.get("payload")
            try:
                payload = json.loads(payload)
                return True
            except:
                return False
        else:
            return True

    def validate_query_params(self, request_details):
        query_params = request_details.get("query_params")
        method = request_details.get("method")
        if method == self.GET_METHOD:
            fault_param = list()
            record_start = query_params.get("record_start")
            if record_start is None or record_start.isdigit():
                pass
            else:
                fault_param.append("record_start")

            record_end = query_params.get("record_end")
            if record_end is None or record_end.isdigit():
                pass
            else:
                fault_param.append("record_end")
            if len(fault_param) == 0:
                return True, ""
            else:
                message = ", ".join(fault_param)
                message = self.INVALID_RECORDS_VALUE.format(message)
                return False, message
        else:
            return True, ""




class UTILITY_METHODS(SQL_METHODS, ValidationMethods):
    __slots__ = ()

    def get_request_details(self, request):
        request_details = dict()
        request_details["method"] = request.method
        request_details["query_params"] = request.args.to_dict()
        request_details["headers"] = {key.lower(): value for key, value in dict(request.headers).items()}
        request_details["payload"] = request.data.decode("utf-8")
        return request_details

    def generate_flask_app(self):
        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        return app

    def query_param_null_value_generator(self, table_name, request_details):
        connection = self.mysql_connector()
        query_params = request_details.get("query_params")
        record_start = query_params.get("record_start")
        record_end = query_params.get("record_end")
        table_row_count = self.row_counter(connection, table_name)
        if record_start is None:
            query_params['record_start'] = 0
        else:
            query_params['record_start'] = int(query_params['record_start'])
        if record_end is None:
            query_params['record_end'] = table_row_count
        else:
            query_params['record_end'] = int(query_params['record_end'])
        return request_details
