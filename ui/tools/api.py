import os
import requests

from settings.constants import BASE_URL, DEV_BASE_URL

if os.getenv("ENV") == "dev":
    base_url = DEV_BASE_URL
else:
    base_url = BASE_URL


def get(path: str, **kwargs):
    """Send a GET request to the backend"""
    return requests.get(f"{base_url}{path}", **kwargs)


def post(path: str, **kwargs):
    """Send a POST request to the backend"""
    return requests.post(f"{base_url}{path}", **kwargs)


def delete(path: str, **kwargs):
    """Send a DELETE request to the backend"""
    return requests.delete(f"{base_url}{path}", **kwargs)
