import streamlit as st
from tools.add_data import register_business

st.header("עסק חדש")

with st.form("add_business"):
    company_name = st.text_input("שם חברה")
    business_id = st.text_input("מספר ח.פ")
    submitted = st.form_submit_button("שמור")

if submitted:
    resp = register_business(company_name, business_id)
    if resp:
        st.success("העסק נוצר")
        print(resp)
    else:
        st.error("נכשלה יצירת העסק")
        st.stop()
