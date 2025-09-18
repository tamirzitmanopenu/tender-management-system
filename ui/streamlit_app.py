import os

from pathlib import Path

import streamlit as st

from tools.design import set_rtl
from settings.constants import (
    NAV_BUSINESSES, NAV_CATEGORIES, NAV_OFFERS, NAV_PROJECTS, PAGE_MANAGE, PAGE_NEW, PAGE_REPORT, WEBSITE_TITLE, ICON_OFFERS, ICON_REFRESH, WEBSITE_LOGO_PATH, ICON_MANAGE, ICON_NEW,ICON_OFFERS, ICON_REPORTS
)
from dotenv import load_dotenv

from tools.auth import login, logout, get_username
from tools.helpers import get_user_permission_name


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
# Load .env from parent directory (project root)
load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')
env = os.getenv("ENV", "")
# יישור לימין
set_rtl()

init_session_state()

st.header(WEBSITE_TITLE)
st.divider()

logo_path = Path(WEBSITE_LOGO_PATH)

if logo_path.exists():
    st.sidebar.image(str(logo_path))
if st.sidebar.button("", icon=ICON_REFRESH, help="רענון נתונים", width="stretch"):
    st.cache_data.clear()
st.sidebar.title(f"{env}")


# הגדרת דפי ברירת מחדל לפני ההתחברות
offer_page_path = "pages/offer_new.py"

# הגדרת דפים בסיסיים שיוצגו לפני ההתחברות
default_pages = {
    NAV_PROJECTS: [
        st.Page("pages/project_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
    ],
}

if not st.session_state.logged_in:
    # הגדרת navigation לפני ההתחברות עם השמות הנכונים
    pg = st.navigation(default_pages)
    # שימוש בפונקציה
    if not login():
        pg.run()
        st.stop()

with st.sidebar:
    st.write(f"משתמש מחובר  {st.session_state['user']}")
    if st.button(f"  👋 יציאה מהמערכת"):
        logout()

username = get_username()
print(f"username is : {username}")
user_permission = get_user_permission_name(username)
print(f"user_permission is : {user_permission}")

pages = {}

if user_permission == 'Admin':
    pages = {
        NAV_PROJECTS: [
            st.Page("pages/project_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
            st.Page("pages/project_new.py", title=PAGE_NEW, icon=ICON_NEW),
        ],
        NAV_BUSINESSES: [
            st.Page("pages/business_new.py", title=PAGE_NEW, icon=ICON_NEW),
            st.Page("pages/business_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
        ],
        NAV_CATEGORIES: [
            st.Page("pages/category_new.py", title=PAGE_NEW, icon=ICON_NEW),
            st.Page("pages/category_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
        ],
        NAV_OFFERS: [
            st.Page(offer_page_path, title=PAGE_NEW, icon=ICON_NEW),
            st.Page("pages/offer_reports.py", title=PAGE_REPORT, icon=ICON_REPORTS),
        ],
    }
else:
    pages = {
        NAV_OFFERS: [
            st.Page(offer_page_path, title=PAGE_NEW, icon=ICON_NEW),
        ],
    }

pg = st.navigation(pages)
pg.run()

st.divider()
# footer
