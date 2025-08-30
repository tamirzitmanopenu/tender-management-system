import json
import streamlit as st
from tools.api import post

st.header("הגשת הצעה")

with st.form("offer_form"):
    project_id = st.text_input("מזהה פרויקט")
    bc_id = st.text_input("מזהה קטגוריית ספק")
    items_text = st.text_area("פריטים (JSON)", "[]")
    submitted = st.form_submit_button("שלח")

if submitted:
    try:
        items = json.loads(items_text)
    except json.JSONDecodeError:
        st.error("מבנה JSON לא תקין")
        items = None
    if items is not None:
        data = {
            "project_id": project_id,
            "business_category_id": bc_id,
            "items": items,
        }
        resp = post("/offers", json=data)
        if resp.ok:
            st.success("ההצעה נשלחה")
        else:
            st.error("נכשלה שליחת ההצעה")
