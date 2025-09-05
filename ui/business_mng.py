import streamlit as st
from tools.fetch_data import fetch_business

st.header("עסקים")

suppliers = fetch_business()
if suppliers:
    st.dataframe(suppliers)
else:
    st.info("אין עסקים")
