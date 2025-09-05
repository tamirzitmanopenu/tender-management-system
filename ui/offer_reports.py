import streamlit as st

from settings.constants import (
    REPORTS_HEADER,
    SELECT_PROJECT,
    REPORTS_FETCH_BTN,
    REPORTS_FETCH_ERROR,
    REPORTS_SELECT_CATEGORY_AND_SUPPLIER,
    REPORTS_DETAILS_BTN,
    REPORTS_DETAILS_ERROR,
    SELECT_CATEGORY, REPORTS_DETAILED_HEADER, REPORTS_AI_RECOM, REPORTS_AI_BTN_HELP, REPORTS_AI_BTN_TEXT,
    REPORTS_AI_ERROR,
)
from tools.fetch_data import fetch_comparison, fetch_details, fetch_projects, fetch_ai_recom, fetch_categories
from tools.helpers import ensure_dict, show_ai_recom

st.header(REPORTS_HEADER)

# Fetch projects and display selector
projects = fetch_projects()
project_name = st.selectbox(SELECT_PROJECT, list(projects.keys()))
project_id = projects.get(project_name)

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
    selected_category = st.selectbox(SELECT_CATEGORY, category_list)

    # Filter data by selected category
    filtered_data = [row for row in comparison_data if row["category_name"] == selected_category]
    # Display filtered dataframe
    st.dataframe(filtered_data)
    less_than_two_offers = len(filtered_data) < 2

    if not less_than_two_offers:
        st.bar_chart(filtered_data,x='company_name',y='total_category_price',color="company_name", stack=False,y_label="מחיר",x_label="",horizontal=True)

    st.divider()
    with st.form(REPORTS_AI_RECOM):
        st.header(REPORTS_AI_RECOM)

        categories = fetch_categories()
        category_id = categories.get(selected_category)

        if less_than_two_offers:
            st.info(REPORTS_AI_BTN_HELP)
        submitted = st.form_submit_button(REPORTS_AI_BTN_TEXT, disabled=less_than_two_offers, width="stretch")

        if submitted:

            ai_recom = fetch_ai_recom(json_input={"project_id": project_id, "category_id": category_id})
            ai_recom = ensure_dict(ai_recom)

            if ai_recom:
                show_ai_recom(ai_recom)
            else:
                st.error(REPORTS_AI_ERROR)
    st.divider()
    st.header(REPORTS_DETAILED_HEADER)
    # Build options from filtered data
    options = {
        f"{row['company_name']} - {row['category_name']}": row["business_category_id"]
        for row in filtered_data
    }

    # Let user select supplier from filtered list
    selection = st.selectbox(REPORTS_SELECT_CATEGORY_AND_SUPPLIER, list(options.keys()))
    bc_id = options.get(selection)

    if st.button(REPORTS_DETAILS_BTN) and bc_id:
        details = fetch_details(project_id, bc_id)
        if details is None:
            st.error(REPORTS_DETAILS_ERROR)
        else:
            st.dataframe(details)
