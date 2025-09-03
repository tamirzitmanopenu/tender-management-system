import streamlit as st
from tools.api import get, delete
from tools.helpers import business_category_selection
from settings.constants import ICON_PROJECTS, SELECT_PROJECT
from tools.fetch_data import fetch_projects

st.set_page_config(
    page_icon=ICON_PROJECTS,
    # layout="wide",
)

st.header("ניהול פרויקטים")


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


with st.container(border=True):
    projects = fetch_projects()
    if projects:
        project_name = st.selectbox(SELECT_PROJECT, list(projects.keys()))
        project_id = projects.get(project_name)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("קבצי פרויקט", use_container_width=True):
                project_files(project_id)
        with c2:
            if st.button("מחיקה", use_container_width=True, type="primary"):
                project_del(project_id)
        with st.expander(label="בחירת ספקים לפריוקט"):
            business_category_selection(project_id)
    else:
        st.info("לא נמצאו פרויקטים במערכת")
