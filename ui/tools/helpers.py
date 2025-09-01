import json
from io import BytesIO

import pandas as pd
import streamlit as st

from settings.constants import FIELD_LABELS, PROJECT_CATEGORY_SELECTION_TEXT
from tools.fetch_data import fetch_business, fetch_categories


# -- Streamlit related helpers --

def show_category_selection(project_id):
    # st.dataframe(business_categories)
    all_business = fetch_business()
    categories = fetch_categories(project_id=project_id)
    # business_categories = fetch_business_category()

    for category_name, category_id in categories.items():
        # business_categories = fetch_business_category(category_id=category_id)
        businesses_list = all_business
        # Business Category Selection:
        selected_businesses = st.multiselect(
            label=PROJECT_CATEGORY_SELECTION_TEXT.format(category_name=category_name),
            label_visibility="collapsed",
            options=businesses_list,
            key=f"category_selection_{category_id}",
            format_func=lambda x: x["company_name"],
            placeholder=PROJECT_CATEGORY_SELECTION_TEXT.format(category_name=category_name)
        )
        selected_ids = [b["business_id"] for b in selected_businesses]
        st.write("Selected business IDs:", selected_ids)

        # ################################################################################################
        # # Example data
        # businesses = [
        #     {"business_id": 1, "business_name": "Alpha Corp"},
        #     {"business_id": 2, "business_name": "Beta LLC"},
        #     {"business_id": 3, "business_name": "Gamma Inc"},
        # ]
        #
        # # Multiselect with format_func to display business_name
        # selected_businesses = st.multiselect(
        #     "Select businesses",
        #     options=businesses,
        #     format_func=lambda x: x["business_name"]
        # )
        #
        # # Extract the business_id values from the selected dictionaries
        # selected_ids = [b["business_id"] for b in selected_businesses]
        #
        # st.write("Selected business IDs:", selected_ids)
        # ################################################################################################


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
            st.dataframe(styled, use_container_width=True)

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
            st.dataframe(df_gaps, use_container_width=True)
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
            st.dataframe(df_reco, use_container_width=True)


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
