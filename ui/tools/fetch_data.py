import json
from urllib.parse import urlencode

import streamlit as st

from tools.api import get, post

from settings.constants import FETCH_PROJECTS, FETCH_CATEGORIES, FETCH_TASKS, FETCH_COMPARISON, FETCH_TASKS_DETAILS, \
    FETCH_AI_RECOM


@st.cache_data(show_spinner=FETCH_PROJECTS)
def fetch_projects(username: str = None) -> list:
    if username is not None:
        resp = get('/user/accessible-projects', json={"username": username})
    else:
        resp = get("/projects")
    print("-------------------------------")
    print(resp.json())
    if getattr(resp, "ok", False):
        return resp.json().get("data", [])
    return []


@st.cache_data(show_spinner=FETCH_CATEGORIES)
def fetch_categories(project_id: str = None) -> dict:
    url = "/categories"

    params = {}
    if project_id is not None:
        params["project_id"] = project_id
    # append query string if params exist
    if params:
        url += f"?{urlencode(params)}"

    resp = get(url)
    if getattr(resp, "ok", False):
        return {c["category_name"]: c["category_id"] for c in resp.json()}
    return {}


@st.cache_data(show_spinner=FETCH_TASKS)
def fetch_tasks(project_id: str, category_id: str) -> list[dict]:
    resp = get(f"/projects/project_tasks?project_id={project_id}&category_id={category_id}")
    if getattr(resp, "ok", False):
        return resp.json().get("items", [])
    return []


@st.cache_data(show_spinner=FETCH_COMPARISON)
def fetch_comparison(project_id: str) -> list:
    resp = get(f"/projects/{project_id}/category-comparison")
    if getattr(resp, "ok", False):
        return resp.json().get("data", [])
    return []


@st.cache_data
def fetch_business():
    resp = get("/businesses")
    if getattr(resp, "ok", False):
        return resp.json().get("data", [])
    return None


@st.cache_data
def fetch_business_category(category_id: str = None, business_id: str = None):
    url = "/business-category"

    if business_id is None and category_id is None:
        raise ValueError("At least one parameter (category_id or business_id) must be provided")

    params = {}
    if category_id is not None:
        params["category_id"] = category_id

    if business_id is not None:
        params["business_id"] = business_id

    # append query string if params exist
    if params:
        url += f"?{urlencode(params)}"

    resp = get(url)
    if getattr(resp, "ok", False):
        return resp.json().get("data", [])
    return None


@st.cache_data
def fetch_business_category_selection(project_id: str = None, business_category_id: str = None):
    url = "/businesses-category-selections"

    params = {}
    if project_id is not None:
        params["project_id"] = project_id
    if business_category_id is not None:
        params["business_category_id"] = business_category_id

    # append query string if params exist
    if params:
        url += f"?{urlencode(params)}"

    resp = get(url)
    if getattr(resp, "ok", False):
        return resp.json().get("data", [])
    return None


@st.cache_data
def fetch_details(project_id: str, bc_id: str):
    resp = get(
        f"/projects/{project_id}/category-comparison/details",
        json={"business_category_id": bc_id},
    )
    if getattr(resp, "ok", False):
        return resp.json().get("data", [])
    return []


@st.cache_data(show_spinner=FETCH_AI_RECOM)
def fetch_ai_recom(json_input: dict) -> dict:
    resp = post("/ai/recommendations", json=json_input)
    if getattr(resp, "ok", False):
        return json.loads(resp.json().get("ai_result"))
    return {}

@st.cache_data()
def fetch_user_details(username: str) -> dict:
    resp = get("/user/details", json={"username": username})
    if getattr(resp, "ok", False):
        return resp.json().get("data", {})
    return {}

def fetch_permissions() -> list:
    """
    מחזיר רשימת כל ההרשאות במערכת
    """
    resp = get("/permissions")
    if getattr(resp, "ok", False):
        print(f"all permissions are: {resp.json()}")
        return resp.json()
    return []
