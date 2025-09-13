import os
import streamlit as st


def authenticate_user(password: str) -> bool:
    """בדיקת סיסמה מול ערך מהסביבה (APP_PASSWORD)"""
    expected_password = os.environ.get("APP_PASSWORD")
    if expected_password is None:
        # לא הוגדרה סיסמה בסביבה, דחה את כל הנסיונות
        return False
    return password == str(expected_password)


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

        # בדיקת סיסמה
        if authenticate_user(password):
            st.toast(f"✅ ברוך הבא, {username}!")
            # שמירת המשתמש ב-session state
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.rerun()
        else:
            st.error("❌ סיסמה שגויה, נסה שנית")
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

    if st.button("התנתק", type="secondary", use_container_width=True):
        st.session_state['logged_in'] = False
        st.toast("✅ התנתקת בהצלחה!")
        st.rerun()


def get_username():
    if "user" in st.session_state:
        return st.session_state.user
    else:
        print("can not find user in session state")
        return None
