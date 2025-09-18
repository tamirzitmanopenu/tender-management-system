"""Application wide constants used by the Streamlit UI."""

# Generic
BASE_URL = "https://tendysys.pythonanywhere.com/api"
DEV_BASE_URL = "http://127.0.0.1:5000/api"

# Styling & Layout
PAGE_LAYOUT_CENTERED = "centered"
UI_WIDTH_STRETCH = "stretch"
BUTTON_TYPE_PRIMARY = "primary"
PILLS_SELECTION_MODE_MULTI = "multi"
HIGHLIGHT_MIN_COLOR = "#d6f5d6"
RTL_STYLE = """
<style>
  /* Apply global RTL */
  html, body {
    direction: rtl;
    unicode-bidi: isolate;
  }

  /* Force charts and visualizations to LTR */
  .stPlotlyChart, .stVegaLiteChart, .vega-embed, .js-plotly-plot {
    direction: ltr !important;
    text-align: left !important;
  }

  /* Sidebar RTL */
  [data-testid="stSidebar"] {
    direction: rtl;
    text-align: right;
  }

  /* Fix for collapsed navigation pane - prevent content overflow */
  [data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    overflow: hidden !important;
  }

  [data-testid="stSidebar"][aria-expanded="false"] > div {
    display: none !important;
  }

  /* Fix collapse/expand arrow direction for RTL */
  [data-testid="collapsedControl"] svg,
  [data-testid="baseButton-header"] svg,
  button[kind="header"] svg {
    transform: scaleX(-1) !important;
  }

  /* Ensure sidebar toggle button is positioned correctly */
  [data-testid="collapsedControl"] {
    right: auto !important;
    left: 1rem !important;
  }

  /* Common form elements and labels */
  label, input, textarea, select, .stTextInput input, .stTextArea textarea, .stSelectbox, .stRadio {
    direction: rtl;
    text-align: right;
  }

  /* Markdown text containers */
  .markdown-text-container {
    text-align: right;
  }

  /* Checkbox labels */
  .stCheckbox > label {
    direction: rtl;
    text-align: right;
  }

  /* FIXED: Regular Buttons RTL with proper alignment */
  [data-testid="stButton"] > button {
    direction: rtl !important;
    text-align: right !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.5rem !important;
    flex-direction: row-reverse !important;
    padding: 0.375rem 0.75rem !important;
    min-height: 38px !important;
    box-sizing: border-box !important;
  }

  /* FIXED: Form Submit Buttons - specific targeting */
  [data-testid="stFormSubmitButton"] button {
    direction: rtl !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-direction: row-reverse !important;
    gap: 0.25rem !important;
    padding: 0.375rem 0.75rem !important;
  }

  /* Fix Form Submit Button icon positioning */
  [data-testid="stFormSubmitButton"] button > span[data-testid="stIconMaterial"] {
    order: 2 !important;
    margin-left: 0.25rem !important;
    margin-right: 0 !important;
    flex-shrink: 0 !important;
  }

  /* Fix Form Submit Button text positioning */
  [data-testid="stFormSubmitButton"] button > div[data-testid="stMarkdownContainer"] {
    order: 1 !important;
    margin-right: 0 !important;
    margin-left: 0 !important;
    text-align: right !important;
  }

  /* Ensure form submit button text is properly aligned */
  [data-testid="stFormSubmitButton"] button p {
    margin: 0 !important;
    text-align: right !important;
    direction: rtl !important;
  }

  /* Handle regular button icons */
  [data-testid="stButton"] .material-icons,
  [data-testid="stButton"] [class^="material-icons"],
  [data-testid="stButton"] svg {
    direction: ltr !important;
    unicode-bidi: isolate !important;
    flex-shrink: 0 !important;
    margin: 0 !important;
  }

  /* Handle regular button text */
  [data-testid="stButton"] > button span,
  [data-testid="stButton"] > button p {
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
    white-space: nowrap !important;
  }

  /* Expander spacing fix - target the actual HTML structure */
  .stExpander summary .st-emotion-cache-c36nl0 {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    flex-direction: row !important;
  }

  /* Target the icon container specifically */
  .stExpander summary [data-testid="stIconMaterial"] {
    margin-left: 0.5rem !important;
    margin-right: 0 !important;
  }

  /* Target the markdown container in expander */
  .stExpander summary [data-testid="stMarkdownContainer"] {
    margin-right: 0.5rem !important;
    margin-left: 0 !important;
  }
</style>
"""

# Landing page
WEBSITE_TITLE = "מערכת המכרזים - TendySys"
WEBSITE_LOGO_PATH = "ui/settings/yankovich_logo.png"

# Sidebar
SIDEBAR_REFRESH_HELP = "רענון נתונים"
SIDEBAR_LOGGED_IN_TEMPLATE = "משתמש מחובר  {user}"
SIDEBAR_LOGOUT_BUTTON_LABEL = "  👋 יציאה מהמערכת"

# Authentication & Session
LOGIN_HEADER = "🔐 התחברות למערכת"
LOGIN_USERNAME_LABEL = "שם משתמש:"
LOGIN_USERNAME_PLACEHOLDER = "הזן את שם המשתמש שלך"
LOGIN_PASSWORD_LABEL = "סיסמה:"
LOGIN_PASSWORD_PLACEHOLDER = "הזן את הסיסמה"
LOGIN_SUBMIT_BUTTON_LABEL = "התחבר"
LOGIN_USERNAME_REQUIRED_ERROR = "❌ נא להזין שם משתמש"
LOGIN_PASSWORD_REQUIRED_ERROR = "❌ נא להזין סיסמה"
LOGIN_INVALID_CREDENTIALS_ERROR = "❌ שם משתמש או סיסמה שגויים"
LOGIN_INFO_PROMPT = "ℹ️ נא להזין פרטי התחברות"
LOGIN_SUCCESS_TOAST = "✅ ברוך הבא, {username}!"
LOGOUT_SUCCESS_TOAST = "✅ התנתקת בהצלחה!"

# Permission & Access
PERMISSION_FETCH_ERROR = "שגיאה בשליפת הרשאות המשתמש: {error}"
PERMISSION_ERROR_TITLE = "🚫 **אין לך הרשאה לגשת לעמוד זה**"
PERMISSION_ERROR_USERNAME_TEMPLATE = "משתמש: {username}{current_permission}"
PERMISSION_ERROR_REQUIRED_TEMPLATE = "הרשאות נדרשות: {permissions}"
PERMISSION_CURRENT_PERMISSION_TEMPLATE = " (הרשאה נוכחית: {permission})"
PERMISSION_GUIDANCE_MESSAGE = (
    "💡 **מה ניתן לעשות?**\n"
    "- פנה למנהל המערכת לעדכון הרשאות\n"
    "- חזור לעמוד הראשי\n"
    "- התנתק והתחבר עם משתמש אחר"
)
PERMISSION_GO_HOME_BUTTON_LABEL = "🏠 חזור לעמוד הראשי"
PERMISSION_LOGOUT_BUTTON_LABEL = "🚪 התנתק"
AUTH_REQUIRED_ERROR = "🔒 **נדרשת התחברות למערכת**"
AUTH_REQUIRED_INFO = "אנא התחבר כדי לגשת לתוכן זה"
USER_IDENTIFICATION_ERROR = "🚫 **שגיאה בזיהוי המשתמש**"

# Navigation labels
NAV_PROJECTS = "פרויקטים"
NAV_BUSINESSES = "קבלני משנה"
NAV_CATEGORIES = "תחומים"
NAV_OFFERS = "הצעות"

# Page labels
PAGE_MANAGE = "ניהול"
PAGE_NEW = "חדש"
PAGE_COMPARE = "השוואת הצעות"
PAGE_REPORT = "דוחות"

# Page paths
PAGE_PROJECT_MANAGE_PATH = "pages/project_mng.py"
PAGE_PROJECT_NEW_PATH = "pages/project_new.py"
PAGE_BUSINESS_NEW_PATH = "pages/business_new.py"
PAGE_BUSINESS_MANAGE_PATH = "pages/business_mng.py"
PAGE_CATEGORY_NEW_PATH = "pages/category_new.py"
PAGE_CATEGORY_MANAGE_PATH = "pages/category_mng.py"
PAGE_OFFER_NEW_PATH = "pages/offer_new.py"
PAGE_OFFER_REPORTS_PATH = "pages/offer_reports.py"

# Icons
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

# Fetch spinners
FETCH_PROJECTS = "טוען פרויקטים"
FETCH_CATEGORIES = "טוען קטגוריות"
FETCH_TASKS = "טוען משימות"
FETCH_COMPARISON = "טוען נתוני השוואה"
FETCH_TASKS_DETAILS = "טוען נתוני משימות מפורטים"
FETCH_AI_RECOM = "טוען המלצת AI"

# Selection labels
SELECT_PROJECT = "בחר פרויקט"
SELECT_CATEGORY = "בחר קטגוריה"
SELECT_BUSINESSES = "בחר בקבלני משנה"

# Buttons
SAVE_BTN = "שמור"
PROJECT_FILES_BTN = "קבצי פרויקט"
PROJECT_DELETE_BTN = "מחיקה"
PROJECT_ASSIGN_BUSINESS_BTN = "הקצאת קבלני משנה לפרויקט"
BUSINESS_ASSIGN_SUBMIT_LABEL = "הפצת מכרז"

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
PROJECT_NEW_HEADER = "פרויקט חדש"
PROJECT_DEADLINE_NOT_SET = "טרם נקבע"
PROJECTS_EMPTY_INFO = "לא נמצאו פרויקטים במערכת"
PROJECT_MISSING_FIELD_ERROR = "השדה '{label}' חסר"
ERROR_SEPARATOR = " , "
PROJECT_SKN_FILE_EXTENSION = "skn"

# Project dialogs & files
BUSINESS_ASSIGN_DIALOG_TITLE = "הקצאת עסקים לקטגוריות"
BUSINESS_ASSIGN_NO_CATEGORIES_WARNING = "לא נמצאו קטגוריות בפרויקט זה"
BUSINESS_ASSIGN_UNREGISTERED_LABEL = "קבלני משנה שאינם רשומים בקטגוריה"
BUSINESS_ASSIGN_UNREGISTERED_HELP = (
    "אין אפשרות לבחור בקבלני משנה שאינם רשומים בקטגוריה - יש לרשום אותם בחלון ניהול קבלני משנה"
)
BUSINESS_ASSIGN_NO_SELECTIONS_WARNING = "לא נמצאו בחירות חדשות"
BUSINESS_ASSIGN_EMAIL_SUBJECT = "הזמנה להגשת הצעה למכרז"
BUSINESS_ASSIGN_EMAIL_PARTIAL_WARNING = "נרשמו בחירות אך חלק מההזמנות לא נשלחו"
BUSINESS_ASSIGN_EMAIL_SUCCESS = "נשלחו הזמנות בהצלחה"
BUSINESS_ASSIGN_EMAIL_FAILURE_WARNING = "נרשם בהצלחה אך שליחת המיילים נכשלה"
PROJECT_DELETE_DIALOG_TITLE = "מחיקה"
PROJECT_DELETE_REASON_LABEL = "כתוב את סיבת המחיקה"
PROJECT_DELETE_CONFIRM_LABEL = "מחק"
PROJECT_DELETE_SUCCESS = "הפרויקט נמחק"
PROJECT_DELETE_FAILURE = "נכשלה מחיקת הפרויקט"
PROJECT_FILES_DIALOG_TITLE = "קבצי פרויקט"
PROJECT_FILES_EMPTY_WARNING = "אין קבצים להצגה"
PROJECT_FILES_DOWNLOAD_TEMPLATE = " הורד קובץ {file_type} [כאן]({download_url}) "

# Date formats
API_DATE_FORMAT = "%Y-%m-%d"
DATE_DISPLAY_FORMAT = "%d/%m/%Y"
DATE_FALLBACK_EM_DASH = "—"

# Offer submission page
OFFER_HEADER = "הגשת הצעה"
OFFER_SELECT_CATEGORY = "בחר קטגוריית ספק"
OFFER_SUBMIT_BTN = "שלח"
OFFER_SUBMIT_SUCCESS = "ההצעה נשלחה"
OFFER_SUBMIT_ERROR = "נכשלה שליחת ההצעה"
OFFER_NO_PROJECTS_WARNING = "No Projects Found"
OFFER_CATEGORY_DISPLAY_CAPTION = "מציג: {category_name}"
OFFER_NO_TASKS_INFO = "לא נמצאו משימות בקטגוריה זו"
OFFER_UNIT_PRICE_LABEL = "מחיר ליחידה"
OFFER_MIN_UNIT_PRICE = 0.0
OFFER_UNIT_PRICE_STEP = 5.0
OFFER_UNIT_CAPTION_TEMPLATE = "יחידת מידה: {unit}"
OFFER_QUANTITY_CAPTION_TEMPLATE = "כמות: {quantity}"
OFFER_TASK_TOTAL_TEMPLATE = "סה\"כ: ₪{value:,.2f}"
OFFER_TOTAL_SUM_TEMPLATE = "### סה\"כ הצעת מחיר: ₪{value:,.2f}"
OFFER_NO_BUSINESS_CATEGORY_ERROR = "לא נמצאה קטגוריה עסקית עבור העסק שלך בקטגוריה זו. לא ניתן להגיש הצעה."

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
REPORTS_PRICE_Y_LABEL = "מחיר"
REPORTS_SUPPLIER_OPTION_TEMPLATE = "{company_name} - {category_name}"

# AI recommendations
AI_REPORT_SUPPLIERS_EXPANDER_TITLE = "📊 השוואת ספקים"
AI_REPORT_SUPPLIERS_COLUMNS = ["ספק", "מחיר כולל", "דירוג", "תקציר חוות דעת", "חוזקות", "חולשות"]
AI_REPORT_QUICK_SUMMARY_TITLE = "⚡ תמצית מהירה"
AI_REPORT_CHEAPEST_SUPPLIER_LABEL = "הספק הזול"
AI_REPORT_LOWEST_PRICE_LABEL = "מחיר זול ביותר"
AI_REPORT_SUPPLIERS_COUNT_LABEL = "מס׳ ספקים"
AI_REPORT_NO_COMPARISON_INFO = "לא נמצאו נתוני השוואה להצגה."
AI_REPORT_PRICE_ANALYSIS_EXPANDER_TITLE = "💰 ניתוח מחירים"
AI_REPORT_CHEAPEST_SUPPLIER_TEMPLATE = "הזולה ביותר: **{supplier}**"
AI_REPORT_NO_PRICE_GAPS_INFO = "לא נמצאו פערי מחירים להצגה."
AI_REPORT_RECOMMENDATION_EXPANDER_TITLE = "⭐ המלצה"
AI_REPORT_RECOMMENDED_SUPPLIER_TEMPLATE = "✅ ספק מומלץ: **{supplier}**"
AI_REPORT_ESTIMATED_PRICE_TEMPLATE = "מחיר משוער: {price}"
AI_REPORT_KEY_REASONS_TITLE = "**נימוקים מרכזיים:**"
AI_REPORT_REASON_BULLET_TEMPLATE = "- {reason}"
AI_REPORT_DOWNLOAD_LABEL = "⬇️ הורדת ניתוח AI"
AI_REPORT_DOWNLOAD_FILENAME = "ai_recommendation.xlsx"
AI_REPORT_DOWNLOAD_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Business pages
BUSINESS_NEW_HEADER = "עסק חדש"
BUSINESS_COMPANY_NAME = "שם חברה"
BUSINESS_ID_LABEL = "מספר ח.פ"
BUSINESS_ADD_SUCCESS = "העסק נוצר"
BUSINESS_ADD_FAILURE = "נכשלה יצירת העסק"
BUSINESS_ADD_EXISTS = "העסק כבר קיים"
BUSINESS_MANAGE_HEADER = "עסקים"
BUSINESS_LIST_EMPTY_INFO = "אין עסקים"

# Business operations
BUSINESS_SELECTION_SAVE_ERROR = "אירעה שגיאה בשמירת הבחירה"
BUSINESS_CATEGORY_LINK_ERROR = "אירעה שגיאה ביצירת שיוך קטגוריה לעסק"

# Category pages
CATEGORY_NEW_HEADER = "קטגוריה חדשה"
CATEGORY_NAME_LABEL = "שם קטגוריה"
CATEGORY_ADD_SUCCESS = "הקטגוריה נוספה"
CATEGORY_ADD_EXISTS = "הקטגוריה כבר קיימת"
CATEGORY_ADD_FAILURE = "נכשלה הוספת הקטגוריה"
CATEGORY_LIST_EMPTY_INFO = "אין קטגוריות"

# Field labels
FIELD_LABELS = {
    "new_project_name": "שם הפרויקט",
    "new_deadline": "תאריך יעד לקבלת הצעות",
    "uploaded_skn": "קובץ כתב כמויות",
    "uploaded_other": "קובץ נוסף",
    "file_type": "סוג הקובץ"
}
