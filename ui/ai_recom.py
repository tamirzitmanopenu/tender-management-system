import streamlit as st
from tools.api import post

st.header("המלצת AI")

with st.form("ai_form"):
    project_id = st.text_input("מזהה פרויקט")
    category_id = st.text_input("מזהה קטגוריה")
    submitted = st.form_submit_button("קבל המלצה")

if submitted:
    resp = post("/ai/recommendations", json={"project_id": project_id, "category_id": category_id})
    if resp.ok:
        st.dataframe(resp.json().get("ai_result"))
    else:
        st.error("שגיאה בקבלת המלצה")
