import streamlit as st
from tools.api import get, post
from tools.fetch_data import fetch_categories
from settings.constants import NAV_CATEGORIES

st.header(NAV_CATEGORIES)


# List categories
cats = fetch_categories()
if cats:
    st.dataframe(cats)
else:
    st.info("אין קטגוריות")
