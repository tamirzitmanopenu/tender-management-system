import streamlit as st

from tools.api import get


@st.cache_resource
def fetch_projects() -> dict:
    resp = get("/projects")
    if resp.ok:
        return {p["name"]: p["project_id"] for p in resp.json()}
    return {}


@st.cache_resource
def fetch_categories() -> dict:
    resp = get("/categories")
    if resp.ok:
        return {c["category_name"]: c["category_id"] for c in resp.json()}
    return {}


@st.cache_resource
def fetch_tasks(project_id: str, category_id: str) -> list[dict]:
    resp = get(f"/projects/project_tasks?project_id={project_id}&category_id={category_id}")
    if resp.ok:
        return resp.json().get("items", [])
    return []


@st.cache_resource
def fetch_comparison(project_id: str):
    resp = get(f"/projects/{project_id}/category-comparison")
    if resp.ok:
        return resp.json().get("data", [])
    return None


@st.cache_resource
def fetch_details(project_id: str, bc_id: str):
    resp = get(
        f"/projects/{project_id}/category-comparison/details",
        json={"business_category_id": bc_id},
    )
    if resp.ok:
        return resp.json().get("data", [])
    return None
