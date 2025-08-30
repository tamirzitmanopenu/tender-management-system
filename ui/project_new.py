import streamlit as st
from tools.api import post

st.header("פרויקט חדש")

with st.form("add_project"):
    name = st.text_input("שם פרויקט")
    deadline = st.date_input("תאריך יעד")
    submitted = st.form_submit_button("שמור")

if submitted:
    data = {"name": name, "deadline_date": str(deadline)}
    resp = post("/projects", json=data)
    if resp.ok:
        st.success(f"נוצר פרויקט {resp.json().get('project_id')}")
    else:
        st.error("נכשלה יצירת הפרויקט")
