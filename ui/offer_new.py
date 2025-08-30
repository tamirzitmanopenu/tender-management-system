import streamlit as st

from tools.api import get, post
from settings.constants import (
    OFFER_HEADER,
    OFFER_SELECT_PROJECT,
    OFFER_SELECT_CATEGORY,
    OFFER_SUBMIT_BTN,
    OFFER_SUBMIT_SUCCESS,
    OFFER_SUBMIT_ERROR,
)


def fetch_projects() -> dict:
    resp = get("/projects")
    if resp.ok:
        return {p["name"]: p["project_id"] for p in resp.json()}
    return {}


def fetch_categories() -> dict:
    resp = get("/categories")
    if resp.ok:
        return {c["category_name"]: c["category_id"] for c in resp.json()}
    return {}


def fetch_tasks(project_id: str, category_id: str) -> list[dict]:
    resp = get(f"/projects/{project_id}/category/{category_id}/project_tasks")
    if resp.ok:
        return resp.json().get("items", [])
    return []


st.header(OFFER_HEADER)

projects = fetch_projects()
project_name = st.selectbox(OFFER_SELECT_PROJECT, list(projects.keys()))
project_id = projects.get(project_name)

categories = fetch_categories()
category_name = st.selectbox(OFFER_SELECT_CATEGORY, list(categories.keys()))
category_id = categories.get(category_name)

tasks = fetch_tasks(project_id, category_id) if project_id and category_id else []

with st.form("offer_form"):
    prices = {}
    for task in tasks:
        label = f"{task['description']} ({task['unit']})"
        prices[task["project_task_id"]] = st.number_input(
            label, min_value=0.0, step=0.01, key=f"task_{task['project_task_id']}"
        )
    submitted = st.form_submit_button(OFFER_SUBMIT_BTN)

if submitted:
    items = [
        {"project_task_id": str(task_id), "price_offer": price}
        for task_id, price in prices.items()
    ]
    data = {
        "project_id": str(project_id),
        "business_category_id": str(category_id),
        "items": items,
    }
    resp = post("/offers", json=data)
    if resp.ok:
        st.success(OFFER_SUBMIT_SUCCESS)
    else:
        st.error(OFFER_SUBMIT_ERROR)
