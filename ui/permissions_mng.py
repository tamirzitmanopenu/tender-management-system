import streamlit as st
from tools.api import get, post

st.header("ניהול קטגוריות")

# Add category
with st.form("add_category"):
    name = st.text_input("שם קטגוריה")
    submitted = st.form_submit_button("שמור")
if submitted:
    resp = post("/categories", json={"category_name": name})
    if resp.ok:
        st.success("הקטגוריה נוספה")
    else:
        st.error("נכשלה הוספת הקטגוריה")

# List categories
resp = get("/categories")
if resp.ok:
    cats = resp.json()
    if cats:
        st.table(cats)
    else:
        st.info("אין קטגוריות")
else:
    st.error("שגיאה בשליפת קטגוריות")
