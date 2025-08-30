import streamlit as st

from tools.design import set_rtl
from settings.constants import WEBSITE_TITLE, WEBSITE_WELCOME_TEXT

st.title(WEBSITE_TITLE)
st.write(WEBSITE_WELCOME_TEXT)

# יישור לימין
set_rtl()

pages = {
    "פרויקטים": [
        st.Page("project_mng.py", title="ניהול"),
        st.Page("project_new.py", title="חדש"),
    ],
    "ספקים": [
        st.Page("supplier_mng.py", title="ניהול"),
        st.Page("supplier_new.py", title="חדש"),
    ],
    "קטגוריות": [
        st.Page("permissions_mng.py", title="ניהול"),
    ],
    "הצעות": [
        st.Page("offer_new.py", title="הגשה"),
    ],
    "דוחות": [
        st.Page("reports.py", title="השוואה"),
        st.Page("ai_recom.py", title="המלצת AI"),
    ],
}

pg = st.navigation(pages)
pg.run()
