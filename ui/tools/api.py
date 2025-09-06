import os
import json
import requests
from requests import Response

from settings.constants import BASE_URL, DEV_BASE_URL

if os.getenv("ENV") == "dev":
    base_url = DEV_BASE_URL
else:
    base_url = BASE_URL


def get(path: str, **kwargs):
    """Send a GET request to the backend"""
    try:
        return requests.get(f"{base_url}{path}", **kwargs)
    except Exception as e:
        print(e)
        resp = Response()
        resp.status_code = 500
        resp._content = json.dumps({"error": str(e)}).encode()
        resp.headers["Content-Type"] = "application/json"
        return resp


def post(path: str, **kwargs):
    """Send a POST request to the backend"""
    try:
        return requests.post(f"{base_url}{path}", **kwargs)
    except Exception as e:
        print(e)
        resp = Response()
        resp.status_code = 500
        resp._content = json.dumps({"error": str(e)}).encode()
        resp.headers["Content-Type"] = "application/json"
        return resp


def delete(path: str, **kwargs):
    """Send a DELETE request to the backend"""
    try:
        return requests.delete(f"{base_url}{path}", **kwargs)
    except Exception as e:
        print(e)
        resp = Response()
        resp.status_code = 500
        resp._content = json.dumps({"error": str(e)}).encode()
        resp.headers["Content-Type"] = "application/json"
        return resp
