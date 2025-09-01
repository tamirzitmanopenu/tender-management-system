import streamlit as st

from tools.design import set_rtl
from settings.constants import (
    WEBSITE_TITLE,
    WEBSITE_WELCOME_TEXT,
    NAV_PROJECTS,
    NAV_SUPPLIERS,
    NAV_CATEGORIES,
    NAV_OFFERS,
    NAV_REPORTS,
    PAGE_MANAGE,
    PAGE_NEW,
    PAGE_COMPARE,
)

st.title(WEBSITE_TITLE)
st.write(WEBSITE_WELCOME_TEXT)

# יישור לימין
set_rtl()

pages = {
    NAV_PROJECTS: [
        st.Page("project_mng.py", title=PAGE_MANAGE),
        st.Page("project_new.py", title=PAGE_NEW),
    ],
    NAV_SUPPLIERS: [
        st.Page("supplier_mng.py", title=PAGE_MANAGE),
        st.Page("supplier_new.py", title=PAGE_NEW),
    ],
    NAV_CATEGORIES: [
        st.Page("category_mng.py", title=PAGE_MANAGE),
        st.Page("category_new.py", title=PAGE_NEW),
    ],
    NAV_OFFERS: [
        st.Page("offer_new.py", title=PAGE_NEW),
    ],
    NAV_REPORTS: [
        st.Page("reports.py", title=PAGE_COMPARE)
    ],
}

pg = st.navigation(pages)
pg.run()
