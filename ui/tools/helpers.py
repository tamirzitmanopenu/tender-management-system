import json
from io import BytesIO
from datetime import datetime
from functools import wraps

import pandas as pd
import streamlit as st

from settings.constants import (
    AI_REPORT_CHEAPEST_SUPPLIER_LABEL,
    AI_REPORT_CHEAPEST_SUPPLIER_TEMPLATE,
    AI_REPORT_DOWNLOAD_FILENAME,
    AI_REPORT_DOWNLOAD_LABEL,
    AI_REPORT_DOWNLOAD_MIME,
    AI_REPORT_ESTIMATED_PRICE_TEMPLATE,
    AI_REPORT_KEY_REASONS_TITLE,
    AI_REPORT_LOWEST_PRICE_LABEL,
    AI_REPORT_NO_COMPARISON_INFO,
    AI_REPORT_NO_PRICE_GAPS_INFO,
    AI_REPORT_PRICE_ANALYSIS_EXPANDER_TITLE,
    AI_REPORT_QUICK_SUMMARY_TITLE,
    AI_REPORT_REASON_BULLET_TEMPLATE,
    AI_REPORT_RECOMMENDATION_EXPANDER_TITLE,
    AI_REPORT_RECOMMENDED_SUPPLIER_TEMPLATE,
    AI_REPORT_SUPPLIERS_COLUMNS,
    AI_REPORT_SUPPLIERS_COUNT_LABEL,
    AI_REPORT_SUPPLIERS_EXPANDER_TITLE,
    API_DATE_FORMAT,
    AUTH_REQUIRED_ERROR,
    AUTH_REQUIRED_INFO,
    BUSINESS_ASSIGN_DIALOG_TITLE,
    BUSINESS_ASSIGN_EMAIL_FAILURE_WARNING,
    BUSINESS_ASSIGN_EMAIL_PARTIAL_WARNING,
    BUSINESS_ASSIGN_EMAIL_SUBJECT,
    BUSINESS_ASSIGN_EMAIL_SUCCESS,
    BUSINESS_ASSIGN_NO_CATEGORIES_WARNING,
    BUSINESS_ASSIGN_NO_SELECTIONS_WARNING,
    BUSINESS_ASSIGN_SUBMIT_LABEL,
    BUSINESS_ASSIGN_UNREGISTERED_HELP,
    BUSINESS_ASSIGN_UNREGISTERED_LABEL,
    BUTTON_TYPE_PRIMARY,
    DATE_DISPLAY_FORMAT,
    DATE_FALLBACK_EM_DASH,
    FIELD_LABELS,
    HIGHLIGHT_MIN_COLOR,
    ICON_SEND,
    PERMISSION_CURRENT_PERMISSION_TEMPLATE,
    PERMISSION_ERROR_REQUIRED_TEMPLATE,
    PERMISSION_ERROR_TITLE,
    PERMISSION_ERROR_USERNAME_TEMPLATE,
    PERMISSION_FETCH_ERROR,
    PERMISSION_GO_HOME_BUTTON_LABEL,
    PERMISSION_GUIDANCE_MESSAGE,
    PERMISSION_LOGOUT_BUTTON_LABEL,
    PILLS_SELECTION_MODE_MULTI,
    PAGE_OFFER_NEW_PATH,
    PROJECT_DEADLINE_NOT_SET,
    PROJECT_DELETE_CONFIRM_LABEL,
    PROJECT_DELETE_DIALOG_TITLE,
    PROJECT_DELETE_FAILURE,
    PROJECT_DELETE_REASON_LABEL,
    PROJECT_DELETE_SUCCESS,
    PROJECT_EDIT_ADD_FILE_LABEL,
    PROJECT_EDIT_DEADLINE_LABEL,
    PROJECT_EDIT_DIALOG_TITLE,
    PROJECT_EDIT_FAILURE,
    PROJECT_EDIT_FILE_TYPE_LABEL,
    PROJECT_EDIT_FILE_UPLOAD_FAILURE,
    PROJECT_EDIT_FILE_UPLOAD_SUCCESS,
    PROJECT_EDIT_SUBMIT_BTN,
    PROJECT_EDIT_SUCCESS,
    PROJECT_FILES_DIALOG_TITLE,
    PROJECT_FILES_DOWNLOAD_TEMPLATE,
    PROJECT_FILES_EMPTY_WARNING,
    SELECT_BUSINESSES,
    UI_WIDTH_STRETCH,
    USER_IDENTIFICATION_ERROR,
)
from tools.fetch_data import (
    fetch_business,
    fetch_business_category,
    fetch_business_category_selection,
    fetch_categories,
    fetch_permissions,
    fetch_user_details,
)
from tools.add_data import register_business_category_selection, register_business_category
from tools.auth import get_username, logout
from tools.api import delete, get, post, put



def get_user_permission_name(username: str) -> str:
    """
    מקבל שם משתמש ומחזיר את שם ההרשאה שלו מבסיס הנתונים
    """
    print(f"checking permission for user: {username}")
    try:
        user_data = fetch_user_details(username)
        print(f"user_data is :{user_data}")
        if not user_data:
            return None
        permission_id = user_data.get('permission_id')
        if not permission_id:
            return None

        # שליפת שם ההרשאה לפי permission_id
        permissions = fetch_permissions()
        for perm in permissions:
            if perm.get('permission_id') == permission_id:
                return perm.get('permission_name')

        return None

    except Exception as e:
        st.error(PERMISSION_FETCH_ERROR.format(error=e))
        return None


def check_user_permission(required_permissions: list) -> bool:
    """
    בודק אם למשתמש הנוכחי יש את ההרשאות הנדרשות
    
    Args:
        required_permissions: רשימה של שמות הרשאות נדרשות
    
    Returns:
        True אם יש למשתמש הרשאה מתאימה, False אחרת
    """
    # בדיקה אם המשתמש מחובר
    if not st.session_state.get('logged_in', False):
        return False

    username = get_username()
    if not username:
        return False

    user_permission = get_user_permission_name(username)
    if not user_permission:
        return False

    # בדיקה אם ההרשאה של המשתמש נמצאת ברשימת ההרשאות הנדרשות
    return user_permission in required_permissions


def show_permission_error(required_permissions: list, current_permission: str = None):
    """
    מציג הודעת שגיאה כשאין למשתמש הרשאה מתאימה
    """
    username = get_username()
    current_perm_text = (
        PERMISSION_CURRENT_PERMISSION_TEMPLATE.format(permission=current_permission)
        if current_permission
        else ""
    )
    required_permissions_text = ", ".join(required_permissions)

    st.error(
        "\n\n".join(
            [
                PERMISSION_ERROR_TITLE,
                PERMISSION_ERROR_USERNAME_TEMPLATE.format(
                    username=username,
                    current_permission=current_perm_text,
                ),
                PERMISSION_ERROR_REQUIRED_TEMPLATE.format(
                    permissions=required_permissions_text
                ),
            ]
        )
    )

    st.info(PERMISSION_GUIDANCE_MESSAGE)

    # # כפתורים לפעולות נוספות
    col1, col2 = st.columns(2)
    with col1:
        if st.button(PERMISSION_GO_HOME_BUTTON_LABEL, use_container_width=True):
            st.switch_page(PAGE_OFFER_NEW_PATH)

    with col2:
        if st.button(PERMISSION_LOGOUT_BUTTON_LABEL, use_container_width=True):
            logout()


def require_permission(*required_permissions):
    """
    Decorator להגבלת גישה לפונקציות לפי הרשאות משתמש
    
    Usage:
        @require_permission('Admin', 'Manager')
        def my_admin_function():
            pass
    
    Args:
        *required_permissions: הרשאות נדרשות (ניתן להעביר כמה הרשאות)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # בדיקה אם המשתמש מחובר
            if not st.session_state.get('logged_in', False):
                st.error(AUTH_REQUIRED_ERROR)
                st.info(AUTH_REQUIRED_INFO)
                st.stop()
                return None

            # בדיקת הרשאות
            username = get_username()
            if not username:
                st.error(USER_IDENTIFICATION_ERROR)
                st.stop()
                return None

            user_permission = get_user_permission_name(username)
            permissions_list = list(required_permissions)

            if not check_user_permission(permissions_list):
                show_permission_error(permissions_list, user_permission)
                st.stop()
                return None

            # אם הגענו לכאן, יש למשתמש הרשאה מתאימה
            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin_only(func):
    """
    Decorator מקוצר לפונקציות שדורשות הרשאת Admin בלבד
    
    Usage:
        @admin_only
        def my_admin_function():
            pass
    """
    return require_permission('Admin')(func)


# -- Streamlit related helpers --
@st.dialog(BUSINESS_ASSIGN_DIALOG_TITLE)
def business_category_selection(project: dict):
    project_id = project.get("project_id")
    project_name = project.get("project_name")
    project_deadline = project.get("project_deadline", PROJECT_DEADLINE_NOT_SET)

    all_business = fetch_business()
    categories = fetch_categories(project_id=project_id)
    if not categories:
        st.warning(BUSINESS_ASSIGN_NO_CATEGORIES_WARNING)
        return
    with st.form("business_category_selection"):
        for category_name, category_id in categories.items():
            # show first businesses that work at this category, followed by the rest
            business_category_dicts = fetch_business_category(category_id=category_id)
            business_ids_in_category = {b['business_id'] for b in business_category_dicts}

            # Separate businesses into two groups
            in_category = [b for b in all_business if b['business_id'] in business_ids_in_category]
            not_in_category = [b for b in all_business if b['business_id'] not in business_ids_in_category]

            # Enable in-category businesses first

            st.caption(f"{category_name}")

            # Business Selection:
            key = f"bs_p{project_id}_c{category_id}"
            selected_businesses = st.pills(
                label=SELECT_BUSINESSES,
                options=in_category,
                key=key,
                format_func=lambda x: x["company_name"],
                selection_mode=PILLS_SELECTION_MODE_MULTI,
            )
            if not_in_category:
                st.pills(
                    label=BUSINESS_ASSIGN_UNREGISTERED_LABEL,
                    options=not_in_category,
                    key=f"{key}_non",
                    format_func=lambda x: x["company_name"],
                    help=BUSINESS_ASSIGN_UNREGISTERED_HELP,
                    disabled=True
                )

            if selected_businesses:
                st.session_state.business_selections[key] = selected_businesses

            st.divider()

        submitted = st.form_submit_button(
            BUSINESS_ASSIGN_SUBMIT_LABEL,
            width=UI_WIDTH_STRETCH,
            type=BUTTON_TYPE_PRIMARY,
            icon=ICON_SEND,
        )

    if submitted:
        business_category_items = []

        for category_id in categories.values():
            key = f"bs_p{project_id}_c{category_id}"
            selected_businesses = st.session_state.business_selections.get(key, [])

            business_categories = fetch_business_category(category_id=category_id)

            for business in selected_businesses:
                # TODO: validate business_id with the selected business_id and current category_id isn't already exist
                business_id = business["business_id"]
                business_category_id = next(
                    (bc["business_category_id"] for bc in business_categories if bc["business_id"] == business_id),
                    None
                )
                # Handle missing category association
                if business_category_id is None:
                    try:
                        bc_resp = register_business_category(category_id, business_id)
                        business_category_id = bc_resp.get("business_category_id")
                    except Exception as e:
                        st.error(e)

                # Validates selection_id isn't already exist
                if business_category_id:
                    existing = fetch_business_category_selection(project_id=project_id,
                                                                 business_category_id=business_category_id)
                    if not existing:
                        business_category_items.append({
                            "business_category_id": str(business_category_id),
                        })

        if not business_category_items:
            st.warning(BUSINESS_ASSIGN_NO_SELECTIONS_WARNING)
            return
        try:
            bcs_resp = register_business_category_selection(project_id, business_category_items)

            # שליחת מיילים לאחר רישום מוצלח
            if bcs_resp and "created" in bcs_resp:
                selection_ids = [
                    item["selection_id"]
                    for item in bcs_resp["created"]
                    if "selection_id" in item
                ]

                if selection_ids:
                    try:
                        formatted_deadline = datetime.strptime(
                            project_deadline,
                            API_DATE_FORMAT
                        ).strftime(DATE_DISPLAY_FORMAT)
                    except ValueError:
                        print("תאריך הדדליין של הפרויקט אינו בפורמט תקין (YYYY-MM-DD).")
                        formatted_deadline = DATE_FALLBACK_EM_DASH

                    email_data = {
                        "items": selection_ids,
                        "subject": BUSINESS_ASSIGN_EMAIL_SUBJECT,
                        "template_id": "request_offer",
                        "template_variables": {
                            "project_name": project_name,
                            "deadline": formatted_deadline,
                        }
                    }

                    email_resp = post("/send_emails/bulk", json=email_data)
                    if email_resp.ok:
                        if email_resp.json().get("invalid_items"):
                            st.warning(BUSINESS_ASSIGN_EMAIL_PARTIAL_WARNING)
                        st.success(BUSINESS_ASSIGN_EMAIL_SUCCESS)
                    else:
                        st.warning(BUSINESS_ASSIGN_EMAIL_FAILURE_WARNING)

        except Exception as e:
            st.error(e)
            st.stop()


@st.dialog(PROJECT_DELETE_DIALOG_TITLE)
def project_del(proj_id):
    reason = st.text_input(PROJECT_DELETE_REASON_LABEL)
    # Delete project
    if st.button(PROJECT_DELETE_CONFIRM_LABEL, type=BUTTON_TYPE_PRIMARY) and proj_id:
        del_resp = delete(f"/projects/{proj_id}")
        if del_resp.ok:
            st.success(PROJECT_DELETE_SUCCESS)
        else:
            st.error(PROJECT_DELETE_FAILURE)
        st.rerun()


@st.dialog(PROJECT_EDIT_DIALOG_TITLE)
def project_edit(project: dict):
    """עריכת פרויקט קיים - עדכון תאריך יעד והוספת מסמך חדש"""
    project_id = project.get("project_id")
    current_deadline = project.get("deadline_date", PROJECT_DEADLINE_NOT_SET)
    
    # הצגת תאריך נוכחי אם קיים
    if current_deadline and current_deadline != PROJECT_DEADLINE_NOT_SET:
        try:
            current_date = datetime.strptime(current_deadline, API_DATE_FORMAT).date()
        except ValueError:
            current_date = None
    else:
        current_date = None
    
    with st.form("edit_project"):
        # עדכון תאריך יעד
        new_deadline = st.date_input(
            PROJECT_EDIT_DEADLINE_LABEL, 
            value=current_date,
            key='edit_deadline'
        )
        
        # הוספת קובץ חדש (אופציונלי)
        uploaded_file = st.file_uploader(
            PROJECT_EDIT_ADD_FILE_LABEL,
            key='edit_uploaded_file'
        )
        
        file_type = st.text_input(
            PROJECT_EDIT_FILE_TYPE_LABEL,
            key='edit_file_type'
        )
        
        submitted = st.form_submit_button(
            PROJECT_EDIT_SUBMIT_BTN,
            type=BUTTON_TYPE_PRIMARY,
            use_container_width=True
        )
    
    if submitted:
        success = True
        
        # עדכון תאריך יעד
        if new_deadline:
            try:
                update_data = {"deadline_date": new_deadline.strftime(API_DATE_FORMAT)}
                update_resp = put(f"/projects/{project_id}", json=update_data)
                
                if not update_resp.ok:
                    st.error(PROJECT_EDIT_FAILURE)
                    success = False
                    
            except Exception as e:
                st.error(f"{PROJECT_EDIT_FAILURE}: {str(e)}")
                success = False
        
        # העלאת קובץ חדש אם סופק
        if uploaded_file and file_type:
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                data = {"project_id": project_id, "file_type": file_type}
                file_resp = post("/files", files=files, data=data)
                
                if file_resp.ok:
                    st.success(PROJECT_EDIT_FILE_UPLOAD_SUCCESS)
                else:
                    st.error(PROJECT_EDIT_FILE_UPLOAD_FAILURE)
                    success = False
                    
            except Exception as e:
                st.error(f"{PROJECT_EDIT_FILE_UPLOAD_FAILURE}: {str(e)}")
                success = False
        
        # הודעת הצלחה כללית
        if success:
            st.success(PROJECT_EDIT_SUCCESS)
            st.rerun()


@st.dialog(PROJECT_FILES_DIALOG_TITLE)
def project_files(proj_id: str):
    # Get project files data
    proj_resp = get(f"/files/{proj_id}")
    files = proj_resp.json()
    # Filter only files that contain both keys
    valid_files = [f for f in files if 'download_url' in f and 'file_type' in f]

    if not valid_files:
        st.warning(PROJECT_FILES_EMPTY_WARNING)
        return

    for file_data in valid_files:
        st.markdown(
            PROJECT_FILES_DOWNLOAD_TEMPLATE.format(
                file_type=file_data['file_type'],
                download_url=file_data['download_url'],
            )
        )


def show_ai_recom(ai_recom: dict):
    # show_download_as_excel(ai_recom)

    # ----- השוואת ספקים -----
    with st.expander(AI_REPORT_SUPPLIERS_EXPANDER_TITLE, expanded=True):
        comp = ai_recom.get("השוואה", [])
        df_comp = as_df(comp)

        # סידור עמודות עיקריות אם קיימות
        preferred_cols = AI_REPORT_SUPPLIERS_COLUMNS
        cols = [c for c in preferred_cols if c in df_comp.columns] + [c for c in df_comp.columns if
                                                                      c not in preferred_cols]
        if not df_comp.empty:
            df_comp = df_comp[cols]

            # עיצוב: מחיר בפורמט מטבע, הדגשת המינימום בעמודת המחיר
            styled = (
                df_comp.style
                .format({"מחיר כולל": fmt_money})
                .highlight_min(subset=["מחיר כולל"], color=HIGHLIGHT_MIN_COLOR)
            )
            st.dataframe(styled, width=UI_WIDTH_STRETCH)

            # מטריקות מהירות (אם יש לפחות שתי שורות)
            if {"מחיר כולל", "ספק"}.issubset(df_comp.columns):
                cheapest_row = df_comp.loc[df_comp["מחיר כולל"].idxmin()]
                cheapest_name = cheapest_row["ספק"]
                cheapest_price = cheapest_row["מחיר כולל"]
                st.caption(AI_REPORT_QUICK_SUMMARY_TITLE)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric(AI_REPORT_CHEAPEST_SUPPLIER_LABEL, cheapest_name)
                with c2:
                    st.metric(AI_REPORT_LOWEST_PRICE_LABEL, fmt_money(cheapest_price))
                with c3:
                    st.metric(AI_REPORT_SUPPLIERS_COUNT_LABEL, len(df_comp))
        else:
            st.info(AI_REPORT_NO_COMPARISON_INFO)

    # ----- ניתוח מחירים -----
    with st.expander(AI_REPORT_PRICE_ANALYSIS_EXPANDER_TITLE, expanded=True):
        price_analysis = ai_recom.get("ניתוח-מחירים", {})
        cheapest = price_analysis.get("הזולה_ביותר", DATE_FALLBACK_EM_DASH)
        gaps = price_analysis.get("פערים_באחוזים_לעומת_הזולה", [])
        df_gaps = as_df(gaps)

        st.write(AI_REPORT_CHEAPEST_SUPPLIER_TEMPLATE.format(supplier=cheapest))
        if not df_gaps.empty:
            if "פער_%" in df_gaps.columns:
                df_gaps["פער_%"] = df_gaps["פער_%"].apply(fmt_pct)
            st.dataframe(df_gaps, width=UI_WIDTH_STRETCH)
        else:
            st.info(AI_REPORT_NO_PRICE_GAPS_INFO)

    # ----- המלצה -----
    with st.expander(AI_REPORT_RECOMMENDATION_EXPANDER_TITLE, expanded=True):
        reco = ai_recom.get("המלצה", {})
        df_reco = as_df(reco)

        # ניסוח תמציתי בראש
        supplier = reco.get("ספק_מומלץ")
        price = reco.get("מחיר_ספק_מומלץ")
        reasons = reco.get("נימוקים", [])

        if supplier:
            st.subheader(AI_REPORT_RECOMMENDED_SUPPLIER_TEMPLATE.format(supplier=supplier))
        if price is not None:
            st.caption(AI_REPORT_ESTIMATED_PRICE_TEMPLATE.format(price=fmt_money(price)))

        if reasons:
            st.markdown(AI_REPORT_KEY_REASONS_TITLE)
            st.markdown(
                "\n".join(
                    AI_REPORT_REASON_BULLET_TEMPLATE.format(reason=r)
                    for r in reasons
                )
            )

        # הצגה טבלאית (למי שרוצה לראות הכל כטבלה)
        if not df_reco.empty:
            # עיצוב המחיר אם קיים
            if "מחיר_ספק_מומלץ" in df_reco.columns:
                df_reco["מחיר_ספק_מומלץ"] = df_reco["מחיר_ספק_מומלץ"].apply(fmt_money)
            st.dataframe(df_reco, width=UI_WIDTH_STRETCH)


def show_download_as_excel(ai_recom: dict):
    # להמיר את כל ה-dict ל-DataFrame (שטוח ככל האפשר)
    df = pd.DataFrame([ai_recom])  # fallback אם יש בעיה

    excel_bytes = to_excel_download(df)

    st.download_button(
        label=AI_REPORT_DOWNLOAD_LABEL,
        data=excel_bytes,
        file_name=AI_REPORT_DOWNLOAD_FILENAME,
        mime=AI_REPORT_DOWNLOAD_MIME
    )


# -- Util helpers --
def get_label(key):
    return FIELD_LABELS.get(key, key)


def to_excel_download(df):
    # Function to convert dataframe to Excel bytes
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def fmt_money(x):
    try:
        return f"₪{x:,.0f}".replace(",", ",")
    except Exception:
        return x


def fmt_pct(x):
    try:
        return f"{float(x):.2f}%"
    except Exception:
        return x


def ensure_dict(obj):
    """מקבל dict או מחרוזת JSON ומחזיר dict תקין."""
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except json.JSONDecodeError:
            return {}
    return {}


def as_df(value):
    """ממיר לרשימה של רשומות -> DataFrame, או dict -> DataFrame שורה אחת."""
    if isinstance(value, list):
        return pd.DataFrame(value)
    if isinstance(value, dict):
        return pd.DataFrame([value])
    return pd.DataFrame()
