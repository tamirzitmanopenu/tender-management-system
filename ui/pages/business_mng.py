import streamlit as st
from tools.fetch_data import fetch_business

from settings.constants import BUSINESS_LIST_EMPTY_INFO, BUSINESS_MANAGE_HEADER
from tools.helpers import require_permission


@require_permission('Admin')
def business_mng():
    st.header(BUSINESS_MANAGE_HEADER)

    suppliers = fetch_business()
    if suppliers:
        st.dataframe(
            suppliers,
            column_config={
                "business_id": "מזהה עסק",
                "company_name": "שם החברה"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info(BUSINESS_LIST_EMPTY_INFO)


business_mng()
