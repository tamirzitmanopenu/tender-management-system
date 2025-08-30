import streamlit as st
from tools.api import get, delete

st.header("ניהול פרויקטים")

# List projects
resp = get("/projects")
if resp.ok:
    projects = resp.json()
    if projects:
        st.table(projects)
    else:
        st.info("אין פרויקטים")
else:
    st.error("שגיאה בקריאת פרויקטים")

# Delete project
project_id = st.text_input("מזהה פרויקט למחיקה")
if st.button("מחק") and project_id:
    del_resp = delete(f"/projects/{project_id}")
    if del_resp.ok:
        st.success("הפרויקט נמחק")
    else:
        st.error("נכשלה מחיקת הפרויקט")
