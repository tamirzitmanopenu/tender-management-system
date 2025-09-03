import os

import streamlit as st

from tools.design import set_rtl
from settings.constants import (
    WEBSITE_TITLE,
    WEBSITE_WELCOME_TEXT,
    NAV_PROJECTS,
    NAV_SUPPLIERS,
    NAV_CATEGORIES,
    NAV_OFFERS,
    PAGE_MANAGE,
    PAGE_NEW, ICON_MANAGE, ICON_NEW, ICON_OFFERS, PAGE_REPORT, ICON_REPORTS,
)
from dotenv import load_dotenv

load_dotenv()  # loads from .env into os.environ
env = os.getenv("ENV", "")

st.title(f"{WEBSITE_TITLE} {env}")
st.write(WEBSITE_WELCOME_TEXT)
# יישור לימין
set_rtl()

pages = {
    NAV_PROJECTS: [
        st.Page("project_new.py", title=PAGE_NEW, icon=ICON_NEW),
        st.Page("project_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
    ],
    NAV_SUPPLIERS: [
        st.Page("supplier_new.py", title=PAGE_NEW, icon=ICON_NEW),
        st.Page("supplier_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
    ],
    NAV_CATEGORIES: [
        st.Page("category_new.py", title=PAGE_NEW, icon=ICON_NEW),
        st.Page("category_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
    ],
    NAV_OFFERS: [
        st.Page("offer_new.py", title=PAGE_NEW, icon=ICON_NEW),
        st.Page("offer_reports.py", title=PAGE_REPORT, icon=ICON_REPORTS),
    ],
}

#TODO: Update
st.set_page_config(
    page_icon=ICON_OFFERS,
    layout="centered",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
pg = st.navigation(pages)
pg.run()
