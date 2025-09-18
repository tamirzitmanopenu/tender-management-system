import streamlit as st
from tools.api import get, post
from tools.fetch_data import fetch_categories
from settings.constants import CATEGORY_LIST_EMPTY_INFO, NAV_CATEGORIES

from tools.helpers import require_permission


@require_permission('Admin')
def category_mng():
    st.header(NAV_CATEGORIES)

    # List categories
    cats = fetch_categories()
    if cats:
        st.dataframe(cats)
    else:
        st.info(CATEGORY_LIST_EMPTY_INFO)


category_mng()
