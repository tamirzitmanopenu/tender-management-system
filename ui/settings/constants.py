"""Application wide constants used by the Streamlit UI."""

# Generic
BASE_URL = "https://tendysys.pythonanywhere.com/api"
DEV_BASE_URL = "http://127.0.0.1:5000/api"

# Landing page
WEBSITE_TITLE = "מערכת המכרזים - TendySys"
WEBSITE_LOGO_PATH = "ui/settings/yankovich_logo.png"

# Project page
PROJECT_REQUIRED_FORM_KEYS = ['new_project_name', 'new_deadline', 'uploaded_skn']
PROJECT_SKN_PROCESS_TEXT = "מעבד את נתוני כתב הכמויות"
PROJECT_CREATION_SUCCESS_TEXT = "נוצר פרויקט {name}"
PROJECT_CREATION_FAILURE_TEXT = "נכשלה יצירת הפרויקט"
PROJECT_SKN_UPLOAD_SUCCESS_TEXT = "הועלה קובץ {filename}"
PROJECT_SKN_UPLOAD_FAILURE_TEXT = "נכשלה העלאת הקובץ"
PROJECT_SKN_PROCESS_SUCCESS_TEXT = "עיבוד כתב כמויות בוצע בהצלחה"
PROJECT_SKN_PROCESS_FAILURE_TEXT = "נכשל עיבוד הקובץ"
PROJECT_OTHER_UPLOAD_SUCCESS_TEXT = "הועלה קובץ {filename}"
PROJECT_OTHER_UPLOAD_FAILURE_TEXT = "נכשלה העלאת הקובץ"
PROJECT_FILE_TYPE_SKN = "כתב כמויות"

# Offer submission page
OFFER_HEADER = "הגשת הצעה"
OFFER_SELECT_CATEGORY = "בחר קטגוריית ספק"
OFFER_SUBMIT_BTN = "שלח"
OFFER_SUBMIT_SUCCESS = "ההצעה נשלחה"
OFFER_SUBMIT_ERROR = "נכשלה שליחת ההצעה"

# Reports page
REPORTS_HEADER = "השוואת הצעות"

REPORTS_FETCH_BTN = "טען השוואת פרויקט"
REPORTS_FETCH_ERROR = "שגיאה בהפקת הדוח"
REPORTS_SELECT_CATEGORY_AND_SUPPLIER = "בחר ספק בקטגוריה"
REPORTS_AI_RECOM = "המלצת AI"
REPORTS_DETAILED_HEADER = "פירוט לפי ספק בקטגורה"

REPORTS_DETAILS_BTN = "הצג פרטים"
REPORTS_DETAILS_ERROR = "שגיאה בפרטי הדוח"
REPORTS_AI_BTN_HELP = "ניתן להשוות בקטגוריות בהן יש לפחות 2 הצעות"
REPORTS_AI_BTN_TEXT = "קבל המלצה"
REPORTS_AI_ERROR = "שגיאה בקבלת המלצה. נסה שוב או בדוק את הפרמטרים."

# Navigation labels
NAV_PROJECTS = "פרויקטים"
NAV_BUSINESSES = "קבלני משנה"
NAV_CATEGORIES = "תחומים"
NAV_OFFERS = "הצעות"

PAGE_MANAGE = "ניהול"
PAGE_NEW = "חדש"
PAGE_COMPARE = "השוואת הצעות"
PAGE_REPORT = "דוחות"

ICON_PROJECTS = ":material/folder:"
ICON_SUPPLIERS = ":material/business:"
ICON_CATEGORIES = ":material/category:"
ICON_OFFERS = ":material/local_offer:"

ICON_MANAGE = ":material/settings:"
ICON_NEW = ":material/add:"
ICON_REPORTS = ":material/analytics:"  # גרף עמודות
ICON_REFRESH = ":material/refresh:"
ICON_FILES = ":material/description:"
ICON_DELETE = ":material/delete:"
ICON_ASSIGN = ":material/handshake:"
ICON_SAVE = ":material/save:"
ICON_SEND = ":material/send:"


FETCH_PROJECTS = "טוען פרויקטים"
FETCH_CATEGORIES = "טוען קטגוריות"
FETCH_TASKS = "טוען משימות"
FETCH_COMPARISON = "טוען נתוני השוואה"
FETCH_TASKS_DETAILS = "טוען נתוני משימות מפורטים"
FETCH_AI_RECOM = "טוען המלצת AI"

SELECT_PROJECT = "בחר פרויקט"
SELECT_CATEGORY = "בחר קטגוריה"
SELECT_BUSINESSES = "בחר בקבלני משנה"

SAVE_BTN = "שמור"

PROJECT_FILES_BTN = "קבצי פרויקט"
PROJECT_DELETE_BTN = "מחיקה"
PROJECT_ASSIGN_BUSINESS_BTN = "הקצאת קבלני משנה לפרויקט"

CATEGORY_NEW_HEADER = "קטגוריה חדשה"
CATEGORY_NAME_LABEL = "שם קטגוריה"
CATEGORY_ADD_SUCCESS = "הקטגוריה נוספה"
CATEGORY_ADD_EXISTS = "הקטגוריה כבר קיימת"
CATEGORY_ADD_FAILURE = "נכשלה הוספת הקטגוריה"

BUSINESS_NEW_HEADER = "עסק חדש"
BUSINESS_COMPANY_NAME = "שם חברה"
BUSINESS_ID_LABEL = "מספר ח.פ"
BUSINESS_ADD_SUCCESS = "העסק נוצר"
BUSINESS_ADD_FAILURE = "נכשלה יצירת העסק"

PROJECT_NEW_HEADER = "פרויקט חדש"

FIELD_LABELS = {
    "new_project_name": "שם הפרויקט",
    "new_deadline": "תאריך יעד לקבלת הצעות",
    "uploaded_skn": "קובץ כתב כמויות",
    "uploaded_other": "קובץ נוסף",
    "file_type": "סוג הקובץ"
}

