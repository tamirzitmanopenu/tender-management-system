import os
import requests
from dotenv import load_dotenv
from pathlib import Path

from settings.constants import BASE_URL, DEV_BASE_URL

from tools.auth import get_username

# Load .env from parent directory (project root)
load_dotenv(Path(__file__).parent.parent.parent / '.env')

if os.getenv("ENV") == "dev":
    base_url = DEV_BASE_URL
else:
    base_url = BASE_URL
def get(path: str, **kwargs):
    """Send a GET request to the backend"""
    try:
        full_url = f"{base_url}{path}"    
        username = get_username()
        response = requests.get(full_url, **kwargs, headers={'X-User': username})
        return response
    except Exception as e:
        # TODO: Consider fixing return None while None does not have .ok attribute
        print(f"Exception in GET request: {e}")
        return None


def post(path: str, **kwargs):
    """Send a POST request to the backend"""
    try:
        return requests.post(f"{base_url}{path}", **kwargs, headers={'X-User': get_username()})
    except Exception as e:
        print(e)
        return None


def put(path: str, **kwargs):
    """Send a PUT request to the backend"""
    try:
        return requests.put(f"{base_url}{path}", **kwargs, headers={'X-User': get_username()})
    except Exception as e:
        print(e)
        return None


def delete(path: str, **kwargs):
    """Send a DELETE request to the backend"""
    try:
        return requests.delete(f"{base_url}{path}", **kwargs, headers={'X-User': get_username()})
    except Exception as e:
        print(e)
        return None
