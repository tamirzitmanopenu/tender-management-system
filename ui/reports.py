import streamlit as st

from settings.constants import (
    REPORTS_HEADER,
    REPORTS_SELECT_PROJECT,
    REPORTS_FETCH_BTN,
    REPORTS_FETCH_ERROR,
    REPORTS_SELECT_CATEGORY_AND_SUPPLIER,
    REPORTS_DETAILS_BTN,
    REPORTS_DETAILS_ERROR,
    REPORTS_SELECT_CATEGORY_ONLY, REPORTS_DETAILED_HEADER,
)
from tools.fetch_data import fetch_comparison, fetch_details, fetch_projects

st.header(REPORTS_HEADER)

# Fetch projects and display selector
projects = fetch_projects()
project_name = st.selectbox(REPORTS_SELECT_PROJECT, list(projects.keys()))
project_id = projects.get(project_name)

# Initialize session state
if "comparison_data" not in st.session_state:
    st.session_state["comparison_data"] = None

# Fetch comparison data
if st.button(REPORTS_FETCH_BTN) and project_id:
    st.session_state["comparison_data"] = fetch_comparison(project_id)
    if st.session_state["comparison_data"] is None:
        st.error(REPORTS_FETCH_ERROR)

comparison_data = st.session_state.get("comparison_data")
if comparison_data:
    # Extract unique categories
    category_list = sorted(set(row["category_name"] for row in comparison_data))

    # Allow user to filter by category
    selected_category = st.selectbox(REPORTS_SELECT_CATEGORY_ONLY, category_list)

    # Filter data by selected category
    filtered_data = [row for row in comparison_data if row["category_name"] == selected_category]

    # Display filtered dataframe
    st.dataframe(filtered_data)

    # Build options from filtered data
    options = {
        f"{row['company_name']} - {row['category_name']}": row["business_category_id"]
        for row in filtered_data
    }
    st.divider()
    st.header(REPORTS_DETAILED_HEADER)

    # Let user select supplier from filtered list
    selection = st.selectbox(REPORTS_SELECT_CATEGORY_AND_SUPPLIER, list(options.keys()))
    bc_id = options.get(selection)

    if st.button(REPORTS_DETAILS_BTN) and bc_id:
        details = fetch_details(project_id, bc_id)
        if details is None:
            st.error(REPORTS_DETAILS_ERROR)
        else:
            st.json(details)
