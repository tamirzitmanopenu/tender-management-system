import streamlit as st
from tools.api import post

st.header("קטגוריה חדשה")

# Add category
with st.form("add_category"):
    name = st.text_input("שם קטגוריה")
    submitted = st.form_submit_button("שמור")
if submitted:
    resp = post("/categories", json={"category_name": name})
    if resp.ok:
        st.success("הקטגוריה נוספה")
    elif resp.status_code == 409:
        st.warning("הקטגוריה כבר קיימת")
    else:
        st.error("נכשלה הוספת הקטגוריה")
        st.stop()

