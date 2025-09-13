import json
from io import BytesIO
from datetime import datetime
from functools import wraps

import pandas as pd
import streamlit as st

from settings.constants import FIELD_LABELS, SELECT_BUSINESSES, ICON_SEND
from tools.fetch_data import fetch_business, fetch_categories, fetch_business_category, \
    fetch_business_category_selection, fetch_user_details, fetch_permissions
from tools.add_data import register_business_category_selection, register_business_category
from tools.auth import get_username, logout
from tools.api import delete, get, post

from settings.constants import NAV_PROJECTS

from settings.constants import PAGE_NEW, PAGE_MANAGE, NAV_BUSINESSES, NAV_CATEGORIES, NAV_OFFERS, ICON_NEW, \
    PAGE_REPORT, ICON_REPORTS, ICON_MANAGE


# -- Permission Management and Authorization --
def define_sidebar(user_permission):
    offer_page_path = "pages/offer_new.py"

    with st.sidebar:
        st.markdown("## Navigation")

        if user_permission == 'Admin':
            st.markdown(f"### {NAV_PROJECTS}")
            st.page_link("pages/project_new.py", label=PAGE_NEW, icon=ICON_NEW)
            st.page_link("pages/project_mng.py", label=PAGE_MANAGE, icon=ICON_MANAGE)

            st.markdown(f"### {NAV_BUSINESSES}")
            st.page_link("pages/business_new.py", label=PAGE_NEW, icon=ICON_NEW)
            st.page_link("pages/business_mng.py", label=PAGE_MANAGE, icon=ICON_MANAGE)

            st.markdown(f"### {NAV_CATEGORIES}")
            st.page_link("pages/category_new.py", label=PAGE_NEW, icon=ICON_NEW)
            st.page_link("pages/category_mng.py", label=PAGE_MANAGE, icon=ICON_MANAGE)

            st.markdown(f"### {NAV_OFFERS}")
            st.page_link(offer_page_path, label=PAGE_NEW, icon=ICON_NEW)
            st.page_link("pages/offer_reports.py", label=PAGE_REPORT, icon=ICON_REPORTS)
        else:
            st.markdown(f"### {NAV_OFFERS}")
            st.page_link(offer_page_path, label=PAGE_NEW, icon=ICON_NEW)
        # pages = {
        #     NAV_PROJECTS: [
        #         st.Page("project_new.py", title=PAGE_NEW, icon=ICON_NEW),
        #         st.Page("project_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
        #     ],
        #     NAV_BUSINESSES: [
        #         st.Page("business_new.py", title=PAGE_NEW, icon=ICON_NEW),
        #         st.Page("business_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
        #     ],
        #     NAV_CATEGORIES: [
        #         st.Page("category_new.py", title=PAGE_NEW, icon=ICON_NEW),
        #         st.Page("category_mng.py", title=PAGE_MANAGE, icon=ICON_MANAGE),
        #     ],
        #     NAV_OFFERS: [
        #         st.Page("offer_new.py", title=PAGE_NEW, icon=ICON_NEW),
        #         st.Page("offer_reports.py", title=PAGE_REPORT, icon=ICON_REPORTS),
        #     ],
        # }
        # pg = st.navigation(pages)
        # pg.run()

def get_user_permission_name(username: str) -> str:
    """
    מקבל שם משתמש ומחזיר את שם ההרשאה שלו מבסיס הנתונים
    """
    try:
        user_data = fetch_user_details(username)
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
        st.error(f"שגיאה בשליפת הרשאות המשתמש: {e}")
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
    current_perm_text = f" (הרשאה נוכחית: {current_permission})" if current_permission else ""

    st.error(
        f"🚫 **אין לך הרשאה לגשת לעמוד זה**\n\n"
        f"משתמש: {username}{current_perm_text}\n\n"
        f"הרשאות נדרשות: {', '.join(required_permissions)}"
    )

    st.info(
        "💡 **מה ניתן לעשות?**\n"
        "- פנה למנהל המערכת לעדכון הרשאות\n"
        "- חזור לעמוד הראשי\n"
        "- התנתק והתחבר עם משתמש אחר"
    )

    # # כפתורים לפעולות נוספות
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 חזור לעמוד הראשי", use_container_width=True):
            st.switch_page("streamlit_app.py")
    
    with col2:
        if st.button("🚪 התנתק", use_container_width=True):
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
                st.error("🔒 **נדרשת התחברות למערכת**")
                st.info("אנא התחבר כדי לגשת לתוכן זה")
                st.stop()
                return None

            # בדיקת הרשאות
            username = get_username()
            if not username:
                st.error("🚫 **שגיאה בזיהוי המשתמש**")
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
@st.dialog("הקצאת עסקים לקטגוריות")
def business_category_selection(project: dict):
    project_id = project.get("project_id")
    project_name = project.get("project_name")
    project_deadline = project.get("project_deadline", "טרם נקבע")

    all_business = fetch_business()
    categories = fetch_categories(project_id=project_id)
    if not categories:
        st.warning("לא נמצאו קטגוריות בפרויקט זה")
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
                selection_mode="multi",
            )
            st.pills(
                label="קבלני משנה שאינם רשומים בקטגוריה",
                options=not_in_category,
                key=f"{key}_non",
                format_func=lambda x: x["company_name"],
                help="אין אפשרות לבחור בקבלני משנה שאינם רשומים בקטגוריה - יש לרשום אותם בחלון ניהול קבלני משנה",
                disabled=True
            )

            if selected_businesses:
                st.session_state.business_selections[key] = selected_businesses

            st.divider()

        submitted = st.form_submit_button("הפצת מכרז", width="stretch", type="primary", icon=ICON_SEND)

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
            st.warning("לא נמצאו בחירות חדשות")
            return
        try:
            bcs_resp = register_business_category_selection(project_id, business_category_items)
            print(bcs_resp)

            # שליחת מיילים לאחר רישום מוצלח
            if bcs_resp and "created" in bcs_resp:
                selection_ids = [
                    item["selection_id"]
                    for item in bcs_resp["created"]
                    if "selection_id" in item
                ]

                if selection_ids:
                    try:
                        formatted_deadline = datetime.strptime(project_deadline, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except ValueError:
                        print("תאריך הדדליין של הפרויקט אינו בפורמט תקין (YYYY-MM-DD).")
                        formatted_deadline = "—"

                    email_data = {
                        "items": selection_ids,
                        "subject": "הזמנה להגשת הצעה למכרז",
                        "template_id": "request_offer",
                        "template_variables": {
                            "project_name": project_name,
                            "deadline": formatted_deadline,
                        }
                    }

                    email_resp = post("/send_emails/bulk", json=email_data)
                    if email_resp.ok:
                        if email_resp.json().get("invalid_items"):
                            st.warning("נרשמו בחירות אך חלק מההזמנות לא נשלחו")
                        st.success("נשלחו הזמנות בהצלחה")
                    else:
                        st.warning("נרשם בהצלחה אך שליחת המיילים נכשלה")

        except Exception as e:
            st.error(e)
            st.stop()


@st.dialog("מחיקה")
def project_del(proj_id):
    reason = st.text_input("כתוב את סיבת המחיקה")
    # Delete project
    if st.button("מחק", type='primary') and proj_id:
        del_resp = delete(f"/projects/{proj_id}")
        if del_resp.ok:
            st.success("הפרויקט נמחק")
        else:
            st.error("נכשלה מחיקת הפרויקט")
        st.rerun()


@st.dialog("קבצי פרויקט")
def project_files(proj_id: str):
    # Get project files data
    proj_resp = get(f"/files/{proj_id}")
    files = proj_resp.json()
    # Filter only files that contain both keys
    valid_files = [f for f in files if 'download_url' in f and 'file_type' in f]

    if not valid_files:
        st.warning("אין קבצים להצגה")
        return

    for file_data in valid_files:
        st.markdown(f" הורד קובץ {file_data['file_type']} [כאן]({file_data['download_url']}) ")


def show_ai_recom(ai_recom: dict):
    # show_download_as_excel(ai_recom)

    # ----- השוואת ספקים -----
    with st.expander("📊 השוואת ספקים", expanded=True):
        comp = ai_recom.get("השוואה", [])
        df_comp = as_df(comp)

        # סידור עמודות עיקריות אם קיימות
        preferred_cols = ["ספק", "מחיר כולל", "דירוג", "תקציר חוות דעת", "חוזקות", "חולשות"]
        cols = [c for c in preferred_cols if c in df_comp.columns] + [c for c in df_comp.columns if
                                                                      c not in preferred_cols]
        if not df_comp.empty:
            df_comp = df_comp[cols]

            # עיצוב: מחיר בפורמט מטבע, הדגשת המינימום בעמודת המחיר
            styled = (
                df_comp.style
                .format({"מחיר כולל": fmt_money})
                .highlight_min(subset=["מחיר כולל"], color="#d6f5d6")
            )
            st.dataframe(styled, width="stretch")

            # מטריקות מהירות (אם יש לפחות שתי שורות)
            if {"מחיר כולל", "ספק"}.issubset(df_comp.columns):
                cheapest_row = df_comp.loc[df_comp["מחיר כולל"].idxmin()]
                cheapest_name = cheapest_row["ספק"]
                cheapest_price = cheapest_row["מחיר כולל"]
                st.caption("⚡ תמצית מהירה")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("הספק הזול", cheapest_name)
                with c2:
                    st.metric("מחיר זול ביותר", fmt_money(cheapest_price))
                with c3:
                    st.metric("מס׳ ספקים", len(df_comp))
        else:
            st.info("לא נמצאו נתוני השוואה להצגה.")

    # ----- ניתוח מחירים -----
    with st.expander("💰 ניתוח מחירים", expanded=True):
        price_analysis = ai_recom.get("ניתוח-מחירים", {})
        cheapest = price_analysis.get("הזולה_ביותר", "—")
        gaps = price_analysis.get("פערים_באחוזים_לעומת_הזולה", [])
        df_gaps = as_df(gaps)

        st.write(f"הזולה ביותר: **{cheapest}**")
        if not df_gaps.empty:
            if "פער_%" in df_gaps.columns:
                df_gaps["פער_%"] = df_gaps["פער_%"].apply(fmt_pct)
            st.dataframe(df_gaps, width="stretch")
        else:
            st.info("לא נמצאו פערי מחירים להצגה.")

    # ----- המלצה -----
    with st.expander("⭐ המלצה", expanded=True):
        reco = ai_recom.get("המלצה", {})
        df_reco = as_df(reco)

        # ניסוח תמציתי בראש
        supplier = reco.get("ספק_מומלץ")
        price = reco.get("מחיר_ספק_מומלץ")
        reasons = reco.get("נימוקים", [])

        if supplier:
            st.subheader(f"✅ ספק מומלץ: **{supplier}**")
        if price is not None:
            st.caption(f"מחיר משוער: {fmt_money(price)}")

        if reasons:
            st.markdown("**נימוקים מרכזיים:**")
            st.markdown("\n".join([f"- {r}" for r in reasons]))

        # הצגה טבלאית (למי שרוצה לראות הכל כטבלה)
        if not df_reco.empty:
            # עיצוב המחיר אם קיים
            if "מחיר_ספק_מומלץ" in df_reco.columns:
                df_reco["מחיר_ספק_מומלץ"] = df_reco["מחיר_ספק_מומלץ"].apply(fmt_money)
            st.dataframe(df_reco, width="stretch")


def show_download_as_excel(ai_recom: dict):
    # להמיר את כל ה-dict ל-DataFrame (שטוח ככל האפשר)
    df = pd.DataFrame([ai_recom])  # fallback אם יש בעיה

    excel_bytes = to_excel_download(df)

    st.download_button(
        label="⬇️ הורדת ניתוח AI",
        data=excel_bytes,
        file_name="ai_recommendation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
