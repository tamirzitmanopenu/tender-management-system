import os
from pathlib import Path

import streamlit as st

from tools.design import set_rtl
from settings.constants import (
    WEBSITE_TITLE,
    NAV_PROJECTS,
    NAV_BUSINESSES,
    NAV_CATEGORIES,
    NAV_OFFERS,
    PAGE_MANAGE,
    PAGE_NEW, ICON_MANAGE, ICON_NEW, ICON_OFFERS, PAGE_REPORT, ICON_REPORTS, ICON_REFRESH, WEBSITE_LOGO_PATH,
)
from dotenv import load_dotenv

from tools.auth import login, logout
from tools.helpers import require_permission


def init_session_state():
    if 'business_selections' not in st.session_state:
        st.session_state.business_selections = {}
    if 'prices' not in st.session_state:
        st.session_state.prices = {}
    if "comparison_data" not in st.session_state:
        st.session_state["comparison_data"] = None
    if "logged_in" not in st.session_state:
        st.session_state['logged_in'] = False

st.set_page_config(
    page_icon=ICON_OFFERS,
    layout="centered",
)
load_dotenv()  # loads from .env into os.environ
env = os.getenv("ENV", "")

# יישור לימין
set_rtl()

init_session_state()

st.header(WEBSITE_TITLE)
st.divider()
@require_permission('Employee', 'Admin')
def employee_function():
    st.title("לעובדים ומנהלים")
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
    pg = st.navigation(pages)
    pg.run()

logo_path = Path(WEBSITE_LOGO_PATH)

if logo_path.exists():
    st.sidebar.image(str(logo_path))
if st.sidebar.button("", icon=ICON_REFRESH, help="רענון נתונים", width="stretch"):
    st.cache_data.clear()
st.sidebar.title(f"{env}")


if not st.session_state.logged_in:
    # שימוש בפונקציה
    if not login():
        st.stop()
else:
    with st.sidebar:
        st.subheader(f"  👋 יציאה מהמערכת")
        st.write(f"משתמש מחובר  {st.session_state['user']}")
        logout()

employee_function()
st.divider()
# footer
