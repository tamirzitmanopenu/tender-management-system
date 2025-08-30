import streamlit as st

from tools.api import get
from settings.constants import (
    REPORTS_HEADER,
    REPORTS_SELECT_PROJECT,
    REPORTS_FETCH_BTN,
    REPORTS_FETCH_ERROR,
    REPORTS_SELECT_CATEGORY,
    REPORTS_DETAILS_BTN,
    REPORTS_DETAILS_ERROR,
)


def fetch_projects() -> dict:
    resp = get("/projects")
    if resp.ok:
        return {p["name"]: p["project_id"] for p in resp.json()}
    return {}


def fetch_comparison(project_id: str):
    resp = get(f"/projects/{project_id}/category-comparison")
    if resp.ok:
        return resp.json().get("data", [])
    return None


def fetch_details(project_id: str, bc_id: str):
    resp = get(
        f"/projects/{project_id}/category-comparison/details",
        json={"business_category_id": bc_id},
    )
    if resp.ok:
        return resp.json().get("data", [])
    return None


st.header(REPORTS_HEADER)
projects = fetch_projects()
project_name = st.selectbox(REPORTS_SELECT_PROJECT, list(projects.keys()))
project_id = projects.get(project_name)

if "comparison_data" not in st.session_state:
    st.session_state["comparison_data"] = None

if st.button(REPORTS_FETCH_BTN) and project_id:
    st.session_state["comparison_data"] = fetch_comparison(project_id)
    if st.session_state["comparison_data"] is None:
        st.error(REPORTS_FETCH_ERROR)

comparison_data = st.session_state.get("comparison_data")
if comparison_data:
    st.dataframe(comparison_data)
    options = {
        f"{row['company_name']} - {row['category_name']}": row["business_category_id"]
        for row in comparison_data
    }
    selection = st.selectbox(REPORTS_SELECT_CATEGORY, list(options.keys()))
    bc_id = options.get(selection)
    if st.button(REPORTS_DETAILS_BTN) and bc_id:
        details = fetch_details(project_id, bc_id)
        if details is None:
            st.error(REPORTS_DETAILS_ERROR)
        else:
            st.json(details)
