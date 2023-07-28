import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from schema import Schema, And, Optional
from odoo.http import request
from odoo.tools import config

API_KEY = config.get('API_KEY', '5f62651d-f288-414c-8e2f-4da1d1567c97')
SECRET_KEY = config.get('SECRET_KEY', '3c61ed41-1d2b-46ed-9744-db972245c145')


def authenticate():
    auth_token = request.httprequest.headers.get('Authorization')
    actual_auth = requests.auth._basic_auth_str(API_KEY, SECRET_KEY)
    if actual_auth != auth_token:
        return {
            'message': "Invalid credentials",
            "status_code": 401,
            "status": 'Fail'
        }
    return False


def schema_validate(payload, schema):
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as err:
        print("Exception: %s" % str(err))
        return "%s" % str(err).split('\n')[0]
    return False
