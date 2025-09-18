import os
import streamlit as st

from settings.constants import (
    BUTTON_TYPE_PRIMARY,
    LOGIN_HEADER,
    LOGIN_INFO_PROMPT,
    LOGIN_INVALID_CREDENTIALS_ERROR,
    LOGIN_PASSWORD_LABEL,
    LOGIN_PASSWORD_PLACEHOLDER,
    LOGIN_PASSWORD_REQUIRED_ERROR,
    LOGIN_SUBMIT_BUTTON_LABEL,
    LOGIN_SUCCESS_TOAST,
    LOGIN_USERNAME_LABEL,
    LOGIN_USERNAME_PLACEHOLDER,
    LOGIN_USERNAME_REQUIRED_ERROR,
    LOGOUT_SUCCESS_TOAST,
)


def authenticate_user(username: str, password: str) -> bool:
    """בדיקת פרטי משתמש מול מסד הנתונים"""
    try:
        # ייבוא מקומי כדי למנוע תלות מעגלית
        from tools.fetch_data import fetch_user_details
        user_data = fetch_user_details(username)
    except Exception:
        user_data = {}

    expected_password = os.getenv("APP_PASSWORD")
    print(f"expected_password is {expected_password}")
    return expected_password is not None and password == expected_password


def login() -> bool:
    """
    פונקציית התחברות למערכת
    מחזירה True אם ההתחברות הצליחה, False אחרת
    """
    st.subheader(LOGIN_HEADER)

    # שדות קלט
    username = st.text_input(LOGIN_USERNAME_LABEL, placeholder=LOGIN_USERNAME_PLACEHOLDER)
    password = st.text_input(
        LOGIN_PASSWORD_LABEL,
        type="password",
        placeholder=LOGIN_PASSWORD_PLACEHOLDER
    )

    # כפתור התחברות
    if st.button(LOGIN_SUBMIT_BUTTON_LABEL, type=BUTTON_TYPE_PRIMARY, use_container_width=True):
        if not username:
            st.error(LOGIN_USERNAME_REQUIRED_ERROR)
            return False

        if not password:
            st.error(LOGIN_PASSWORD_REQUIRED_ERROR)
            return False

        # בדיקת פרטי ההתחברות
        if authenticate_user(username, password):
            st.toast(LOGIN_SUCCESS_TOAST.format(username=username))
            # שמירת המשתמש ב-session state
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.rerun()
        else:
            st.error(LOGIN_INVALID_CREDENTIALS_ERROR)
            return False

    # הצגת הודעה אם עדיין לא הוזנו פרטים
    if not password:
        st.info(LOGIN_INFO_PROMPT)

    return False


# בדיקה אם המשתמש כבר מחובר
def logout():
    """
    פונקציית יציאה מהמערכת
    """
    st.session_state['logged_in'] = False
    st.toast(LOGOUT_SUCCESS_TOAST)
    st.rerun()


def get_username():
    if "user" in st.session_state:
        return st.session_state.user
    else:
        print("can not find user in session state")
        return None
