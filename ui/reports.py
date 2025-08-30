import streamlit as st
from tools.api import get

st.header("דוח השוואת קטגוריות")

project_id = st.text_input("מזהה פרויקט")
if st.button("שלוף השוואה") and project_id:
    resp = get(f"/projects/{project_id}/category-comparison")
    if resp.ok:
        data = resp.json().get('data')
        st.dataframe(data)
    else:
        st.error("שגיאה בהפקת הדוח")

    bc_id = st.text_input("מזהה קטגוריית ספק")
    if st.button("פרטים") and bc_id:
        det = get(f"/projects/{project_id}/category-comparison/details", json={"business_category_id": bc_id})
        if det.ok:
            st.json(det.json().get('data'))
        else:
            st.error("שגיאה בפרטי הדוח")
