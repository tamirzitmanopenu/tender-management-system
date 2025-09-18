import streamlit as st
from tools.api import post
from settings.constants import (
    CATEGORY_NEW_HEADER,
    CATEGORY_NAME_LABEL,
    SAVE_BTN,
    CATEGORY_ADD_SUCCESS,
    CATEGORY_ADD_EXISTS,
    CATEGORY_ADD_FAILURE,
    ICON_SAVE,
)
from tools.helpers import require_permission


@require_permission('Admin')
def category_new():
    st.header(CATEGORY_NEW_HEADER)

    # Add category
    with st.form("add_category"):
        name = st.text_input(CATEGORY_NAME_LABEL)
        submitted = st.form_submit_button(SAVE_BTN, icon=ICON_SAVE)
    if submitted:
        resp = post("/categories", json={"category_name": name})
        if resp.ok:
            st.success(CATEGORY_ADD_SUCCESS)
        elif resp.status_code == 409:
            st.warning(CATEGORY_ADD_EXISTS)
        else:
            st.error(CATEGORY_ADD_FAILURE)
            st.stop()


category_new()
