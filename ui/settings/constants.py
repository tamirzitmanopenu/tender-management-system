"""Application wide constants used by the Streamlit UI."""

# Generic
BASE_URL = "https://tendysys.pythonanywhere.com/api"
DEV_BASE_URL = "http://127.0.0.1:5000/api"

# Landing page
WEBSITE_TITLE = "י ינקוביץ 🎈"
WEBSITE_WELCOME_TEXT = "ברוכים הבאים למערכת המכרזים"

# Offer submission page
OFFER_HEADER = "הגשת הצעה"
OFFER_SELECT_PROJECT = "בחר פרויקט"
OFFER_SELECT_CATEGORY = "בחר קטגוריית ספק"
OFFER_SUBMIT_BTN = "שלח"
OFFER_SUBMIT_SUCCESS = "ההצעה נשלחה"
OFFER_SUBMIT_ERROR = "נכשלה שליחת ההצעה"

# Reports page
REPORTS_HEADER = "דוח השוואת קטגוריות"
REPORTS_SELECT_PROJECT = "בחר פרויקט"
REPORTS_FETCH_BTN = "טען השוואת פרויקט"
REPORTS_FETCH_ERROR = "שגיאה בהפקת הדוח"
REPORTS_SELECT_CATEGORY_AND_SUPPLIER = "בחר ספק בקטגוריה"
REPORTS_SELECT_CATEGORY_ONLY = "קטגוריה להצגה"
REPORTS_DETAILED_HEADER = "פירוט לפי ספק בקטגורה"

REPORTS_DETAILS_BTN = "הצג פרטים"
REPORTS_DETAILS_ERROR = "שגיאה בפרטי הדוח"

# Navigation labels
NAV_PROJECTS = "פרויקטים"
NAV_SUPPLIERS = "ספקים"
NAV_CATEGORIES = "קטגוריות"
NAV_OFFERS = "הצעות"
NAV_REPORTS = "דוחות"

PAGE_MANAGE = "ניהול"
PAGE_NEW = "חדש"
PAGE_SUBMIT = "הגשה"
PAGE_COMPARE = "השוואה"
PAGE_AI_RECOM = "המלצת AI"

# constants.py
FIELD_LABELS = {
    "new_project_name": "שם הפרויקט",
    "new_deadline": "תאריך היעד",
    "uploaded_skn": "קובץ כתב כמויות",
    "file_type": "סוג הקובץ"
}
