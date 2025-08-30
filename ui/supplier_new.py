import streamlit as st
from tools.api import post

st.header("ספק חדש")

with st.form("add_supplier"):
    company_name = st.text_input("שם חברה")
    business_id = st.text_input("מספר ח.פ")
    submitted = st.form_submit_button("שמור")

if submitted:
    data = {"company_name": company_name, "business_id": business_id}
    resp = post("/businesses", json=data)
    if resp.ok:
        st.success("הספק נוצר")
    else:
        st.error("נכשלה יצירת הספק")
