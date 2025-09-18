import streamlit as st
from tools.fetch_data import fetch_business

from tools.helpers import require_permission


@require_permission('Admin')
def business_mng():
    st.header("עסקים")

    suppliers = fetch_business()
    if suppliers:
        st.dataframe(suppliers)
    else:
        st.info("אין עסקים")


business_mng()
