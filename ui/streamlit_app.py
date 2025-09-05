import os

import streamlit as st

from tools.design import set_rtl
from settings.constants import (
    WEBSITE_TITLE,
    WEBSITE_WELCOME_TEXT,
    NAV_PROJECTS,
    NAV_BUSINESSES,
    NAV_CATEGORIES,
    NAV_OFFERS,
    PAGE_MANAGE,
    PAGE_NEW, ICON_MANAGE, ICON_NEW, ICON_OFFERS, PAGE_REPORT, ICON_REPORTS, ICON_REFRESH, WEBSITE_LOGO_PATH,
)
from dotenv import load_dotenv


def init_session_state():
    if 'business_selections' not in st.session_state:
        st.session_state.business_selections = {}
    if 'prices' not in st.session_state:
        st.session_state.prices = {}
    if "comparison_data" not in st.session_state:
        st.session_state["comparison_data"] = None


load_dotenv()  # loads from .env into os.environ
env = os.getenv("ENV", "")

# יישור לימין
set_rtl()

init_session_state()

col1, _, _, col4 = st.columns([0.8, 0.05, 0.05, 0.6])
with col1:
    st.image(WEBSITE_LOGO_PATH)
with col4:
    st.title(WEBSITE_TITLE)
    st.caption(
        f"{WEBSITE_WELCOME_TEXT}<br>{WEBSITE_TITLE} {env}",
        unsafe_allow_html=True
    )

if st.button("", icon=ICON_REFRESH, help="רענון נתונים"):
    st.cache_data.clear()
pages = {
    NAV_PROJECTS: [
        st.Page("project_new.py", title=PAGE_NEW, icon=ICON_NEW),
        st.Page("project_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
    ],
    NAV_BUSINESSES: [
        st.Page("business_new.py", title=PAGE_NEW, icon=ICON_NEW),
        st.Page("business_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
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

st.divider()
# footer
