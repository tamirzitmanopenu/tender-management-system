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
        # המרת dict לרשימה של tuples לטבלה
        cats_list = [{"category_id": cat_id, "category_name": cat_name} 
                     for cat_name, cat_id in cats.items()]
        st.dataframe(
            cats_list,
            column_config={
                "category_id": "מזהה קטגוריה",
                "category_name": "שם הקטגוריה"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info(CATEGORY_LIST_EMPTY_INFO)


category_mng()
