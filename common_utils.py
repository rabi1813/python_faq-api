"""
Common Utilities
"""
import json
import flask
import yaml
from string_literals import Constants, ErrorMessages


class CommonUtilsMethods:
    """
    Class for Common Utility Methods
    """
    __slots__ = ()

    @staticmethod
    def get_request_details(request):
        """
        Fetch API Request Details
        :param request: API Request
        :return: Request details
        """
        request_details = {
            "method": request.method,
            "query_params": request.args.to_dict(),
            "headers": {key.lower(): value
                        for key, value in dict(request.headers).items()},
            "payload": request.data.decode("utf-8")
        }
        return request_details

    @staticmethod
    def generate_flask_app():
        """
        Generate Flask app object
        :return: Flask app object
        """
        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        return app

    @staticmethod
    def read_config_file():
        """
        Read Config File
        :return:Config Data
        """
        with open(Constants.CONFIG_FILE, 'r') as config:
            config_details = yaml.load(config, Loader=yaml.FullLoader)
        return config_details


class ValidationMethods(Constants, ErrorMessages):
    """
    Validation Methods
    """
    __slots__ = ()

    def pre_check(self, request_details):
        """
        Methods to call all validations
        :param request_details: API request details
        :return: If false, returns (False, Error_message)
                 If true, returns (True, API request details)
        """
        flag = self.validate_method(request_details)
        if not flag:
            return self.generate_error_response(validation_type="method")
        flag, message = self.validate_header(request_details)
        if not flag:
            return self.generate_error_response(validation_type="header", message=message)
        flag = self.validate_content_type(request_details)
        if not flag:
            return self.generate_error_response(validation_type="content_type")
        flag = self.validate_payload(request_details)
        if not flag:
            return self.generate_error_response(validation_type="payload", status_code=500)
        flag, message = self.validate_query_params(request_details)
        if not flag:
            return self.generate_error_response(validation_type="query_params", message=message)
        return True, request_details

    def generate_error_response(self, validation_type=None, message=None, status_code=400):
        """
        Generate Error response
        :param validation_type: Validation Type
        :param message: Error Message
        :param status_code: Error Status Code
        :return: Flask response Object
        """
        if validation_type == "method":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.INVALID_METHOD
        elif validation_type == "content_type":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.INVALID_CONTENT_TYPE
        elif validation_type == "header":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = message
        elif validation_type == "payload":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.INVALID_PAYLOAD
        elif validation_type == "query_params":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = message
        elif validation_type == "db_connect":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.DB_CONNECTION_FAIL
        elif validation_type == "id_generation":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.ID_GENERATION_FAILURE
        elif validation_type == "pre_delete_check":
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = message
        else:
            self.ERROR_MESSAGE_TEMPLATE["error_message"] = self.GENERAL_ERROR_MESSAGE
        return False, flask.Response(json.dumps(self.ERROR_MESSAGE_TEMPLATE), status=status_code,
                                     mimetype='application/json')

    @staticmethod
    def generate_success_response(status_code, message):
        """
        Generate Success response
        :param message: Success Message
        :param status_code: Success Status Code
        :return: Flask response Object
        """
        return flask.Response(json.dumps(message), status=status_code, mimetype='application/json')

    def validate_method(self, request_details):
        """
        Validate API Methods
        :param request_details: API Request details
        :return: True/False
        """
        flag = False
        method = request_details.get("method")
        if method.upper() in self.ALLOWED_METHODS:
            flag = True
        return flag

    def validate_header(self, request_details):
        """
        Validate API Headers
        :param request_details: API Request details
        :return: If false, returns (False, Error_message)
                 If true, returns (True, "")
        """
        headers = request_details.get("headers").keys()
        missing_header = []
        for header in self.MANDATORY_HEADERS:
            if header not in headers:
                missing_header.append(header)
        if missing_header:
            message = ", ".join(missing_header)
            message = self.INVALID_HEADER.format(message)
            return False, message
        return True, ""

    def validate_content_type(self, request_details):
        """
        Validate Content-Type
        :param request_details: API Request details
        :return: True/False
        """
        content_type = request_details.get("headers").get("content-type")
        flag = False
        if content_type == self.JSON_CONTENT_TYPE:
            flag = True
        return flag

    def validate_payload(self, request_details):
        """
        Validate API Request body
        :param request_details: API Request details
        :return: True/False
        """
        method = request_details.get("method")
        if method in self.NON_GET_METHODS:
            payload = request_details.get("payload")
            try:
                payload = json.loads(payload)
                return True
            except json.decoder.JSONDecodeError as exp:
                print(str(exp))
                return False
        else:
            return True

    def validate_query_params(self, request_details):
        """
        Validate API Query Parameters
        :param request_details: API Request details
        :return: If false, returns (False, Error_message)
                 If true, returns (True, "")
        """
        query_params = request_details.get("query_params")
        method = request_details.get("method")
        if method == self.GET_METHOD:
            fault_param = []
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
            message = ", ".join(fault_param)
            message = self.INVALID_RECORDS_VALUE.format(message)
            return False, message
        return True, ""
