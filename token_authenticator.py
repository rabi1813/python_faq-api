from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime

from common_utils import CommonUtilsMethods
from security_operations import SecurityMethods

common_utils_obj = CommonUtilsMethods()
secure_object = SecurityMethods()


def token_configure(app):
    config_data = secure_object.decrypted_config()
    secret_key = secure_object.load_key(config_data.get("secret")).decode()
    connection_string = generate_sqlalchemy_connection_string(config_data)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return app


def generate_sqlalchemy_connection_string(config_data):
    user = config_data.get("user")
    key_pass = config_data.get("password")
    host = config_data.get("host")
    db_name = config_data.get("db_name")
    connection_string = f"mysql+pymysql://{user}:{key_pass}@{host}/{db_name}"
    return connection_string
