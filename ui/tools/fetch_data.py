import json

import streamlit as st

from tools.api import get, post

from settings.constants import FETCH_PROJECTS, FETCH_CATEGORIES, FETCH_TASKS, FETCH_COMPARISON, FETCH_TASKS_DETAILS, \
    FETCH_AI_RECOM


@st.cache_resource(show_spinner=FETCH_PROJECTS)
def fetch_projects() -> dict:
    resp = get("/projects")
    if resp.ok:
        return {p["name"]: p["project_id"] for p in resp.json()}
    return {}


@st.cache_resource(show_spinner=FETCH_CATEGORIES)
def fetch_categories() -> dict:
    resp = get("/categories")
    if resp.ok:
        return {c["category_name"]: c["category_id"] for c in resp.json()}
    return {}


@st.cache_resource(show_spinner=FETCH_TASKS)
def fetch_tasks(project_id: str, category_id: str) -> list[dict]:
    resp = get(f"/projects/project_tasks?project_id={project_id}&category_id={category_id}")
    if resp.ok:
        return resp.json().get("items", [])
    return []


@st.cache_resource(show_spinner=FETCH_COMPARISON)
def fetch_comparison(project_id: str) -> list:
    resp = get(f"/projects/{project_id}/category-comparison")
    if resp.ok:
        return resp.json().get("data", [])
    return []


@st.cache_resource(show_spinner=FETCH_TASKS_DETAILS)
def fetch_details(project_id: str, bc_id: str):
    resp = get(
        f"/projects/{project_id}/category-comparison/details",
        json={"business_category_id": bc_id},
    )
    if resp.ok:
        return resp.json().get("data", [])
    return []


@st.cache_resource(show_spinner=FETCH_AI_RECOM)
def fetch_ai_recom(json_input: dict) -> dict:
    resp = post("/ai/recommendations", json=json_input)
    if resp.ok:
        return json.loads(resp.json().get("ai_result"))
    return {}
