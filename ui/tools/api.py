import requests

from settings.constants import BASE_URL


def get(path: str, **kwargs):
    """Send a GET request to the backend"""
    return requests.get(f"{BASE_URL}{path}", **kwargs)


def post(path: str, **kwargs):
    """Send a POST request to the backend"""
    return requests.post(f"{BASE_URL}{path}", **kwargs)


def delete(path: str, **kwargs):
    """Send a DELETE request to the backend"""
    return requests.delete(f"{BASE_URL}{path}", **kwargs)
