import streamlit as st
from tools.api import get, post

st.header("ניהול קטגוריות")

# List categories
resp = get("/categories")
if resp.ok:
    cats = resp.json()
    if cats:
        st.dataframe(cats)
    else:
        st.info("אין קטגוריות")
else:
    st.error("שגיאה בשליפת קטגוריות")
