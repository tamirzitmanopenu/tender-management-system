import os

from pathlib import Path

import streamlit as st

from tools.design import set_rtl
from settings.constants import (
    WEBSITE_TITLE, ICON_OFFERS, ICON_REFRESH, WEBSITE_LOGO_PATH,
)
from dotenv import load_dotenv

from tools.auth import login, logout, get_username
from tools.helpers import get_user_permission_name, define_sidebar


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

with st.sidebar:
    st.write(f"משתמש מחובר  {st.session_state['user']}")
    if st.button(f"  👋 יציאה מהמערכת"):
        logout()

username = get_username()
print(f"username is : {username}")
user_permission = get_user_permission_name(username)
print(f"user_permission is : {user_permission}")

define_sidebar(user_permission)

st.divider()
# footer
