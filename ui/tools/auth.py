import os
import streamlit as st


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
    st.subheader("🔐 התחברות למערכת")

    # שדות קלט
    username = st.text_input("שם משתמש:", placeholder="הזן את שם המשתמש שלך")
    password = st.text_input("סיסמה:", type="password", placeholder="הזן את הסיסמה")

    # כפתור התחברות
    if st.button("התחבר", type="primary", use_container_width=True):
        if not username:
            st.error("❌ נא להזין שם משתמש")
            return False

        if not password:
            st.error("❌ נא להזין סיסמה")
            return False

        # בדיקת פרטי ההתחברות
        if authenticate_user(username, password):
            st.toast(f"✅ ברוך הבא, {username}!")
            # שמירת המשתמש ב-session state
            st.session_state['logged_in'] = True 
            st.session_state['user'] = username
            st.rerun()
        else:
            st.error("❌ שם משתמש או סיסמה שגויים")
            return False

    # הצגת הודעה אם עדיין לא הוזנו פרטים
    if not password:
        st.info("ℹ️ נא להזין פרטי התחברות")

    return False


# בדיקה אם המשתמש כבר מחובר
def logout():
    """
    פונקציית יציאה מהמערכת
    """
    st.session_state['logged_in'] = False
    st.toast("✅ התנתקת בהצלחה!")
    st.rerun()


def get_username():
    if "user" in st.session_state:
        return st.session_state.user
    else:
        print("can not find user in session state")
        return None
