import streamlit as st
from tools.add_data import register_business
from settings.constants import (
    BUSINESS_NEW_HEADER,
    BUSINESS_COMPANY_NAME,
    BUSINESS_ID_LABEL,
    SAVE_BTN,
    BUSINESS_ADD_SUCCESS,
    BUSINESS_ADD_FAILURE,
    ICON_SAVE,
)

from tools.helpers import require_permission


@require_permission('Admin')
def business_new():
    st.header(BUSINESS_NEW_HEADER)

    with st.form("add_business"):
        company_name = st.text_input(BUSINESS_COMPANY_NAME)
        business_id = st.text_input(BUSINESS_ID_LABEL)
        submitted = st.form_submit_button(SAVE_BTN, icon=ICON_SAVE)

    if submitted:
        resp = register_business(company_name, business_id)
        if resp:
            st.success(BUSINESS_ADD_SUCCESS)
        else:
            st.error(BUSINESS_ADD_FAILURE)
            st.stop()


business_new()
