import os
import json
import base64
import hmac
import hashlib
import datetime

from flask import Flask
from flask import jsonify
from flask import request

import requests
import boto3

app = Flask(__name__)

configuration_items = [
    "client_id",
    "client_secret",
    "scope",
    "password",
    "grant_type",
    "cognito_url",
    "aws_region"
]

for configuration_item in configuration_items:
    configuration_item_value = os.environ.get(configuration_item)
    app.config[configuration_item] = configuration_item_value


@app.route("/auth/signup", methods=["GET", "POST"])
def user_signup():
    if not request.is_json:
        return jsonify({"message": "Invalid request"})
    client = boto3.client("cognito-idp", region_name=app.config.get("aws_region", app.config.get("aws_region")))
    email = content["email"]
    orgid = content["orgid"]

    try:
        response = client.admin_create_user(
            UserPoolId=app.config.get("pool_id"),
            Username=email,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
            ValidationData=[
                {
                    'Name': 'string',
                    'Value': email
                },
            ],
            TemporaryPassword=app.config.get("password"),
            ForceAliasCreation=False,
            MessageAction='SUPPRESS',
            DesiredDeliveryMediums=[
                'EMAIL',
            ]
        )
    except Exception as err:
        print(err)
        response = "{'message': 'Invalid email address '}"

    return jsonify(response);


@app.route("/auth/password", methods=["GET", "POST"])
def set_permanent_password():
    if not request.is_json:
        return jsonify({"message": "Invalid request"})

    client = boto3.client("cognito-idp", region_name=app.config.get("aws_region", app.config.get("aws_region")))
    email = content["email"]
    password = app.config.get("password")
    try:
        response = client.admin_set_user_password(
            UserPoolId=app.config.get("pool_id"),
            Username=email,
            Password=password,
            Permanent=True
    )
    except Exception as err:
        print(err)
        response = "{'message': 'Invalid email address '}"

    return jsonify(response);


@app.route("/health")
def health():
    return "I am fine!";
