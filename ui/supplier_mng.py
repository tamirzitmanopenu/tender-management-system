import streamlit as st
from tools.api import get
from tools.fetch_data import fetch_business

st.header("ניהול ספקים")


suppliers = fetch_business()
if suppliers:
    st.dataframe(suppliers)
else:
    st.info("אין ספקים")
