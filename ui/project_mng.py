import streamlit as st
from tools.api import get, delete
from tools.helpers import show_category_selection
from settings.constants import ICON_PROJECTS

st.set_page_config(
    page_icon=ICON_PROJECTS,
    layout="wide",
)

st.header("ניהול פרויקטים")

projects = None

# List projects
resp = get("/projects")
if resp.ok:
    projects = resp.json()
    if projects:
        st.dataframe(projects)
    else:
        st.info("אין פרויקטים")
else:
    st.error("שגיאה בקריאת פרויקטים")


@st.dialog("נהל פרויקט")
def project_mng(project):
    project_id = project['project_id']
    with st.expander(label="הקצאת ספקים"):
        show_category_selection(project_id)

    # Get project files data
    st.title("קבצי פרויקט")
    proj_resp = get(f"/files/{project_id}")
    file_data = proj_resp.json()
    if file_data:
        if 'download_url' in file_data and 'file_type' in file_data:
            st.markdown(f" הורד קובץ {file_data['file_type']} [כאן]({file_data['download_url']}) ")
    else:
        st.info("אין קבצים להצגה")

    st.divider()
    st.title("מחיקה")
    reason = st.text_input("כתוב את סיבת המחיקה")
    # Delete project
    if st.button(f" מחק את: {project['name']}") and project_id:
        del_resp = delete(f"/projects/{project_id}")
        if del_resp.ok:
            st.success("הפרויקט נמחק")
        else:
            st.error("נכשלה מחיקת הפרויקט")
        st.rerun()


if projects is not None:
    st.write("בחר פרויקט")
    for proj in projects:
        if st.button(proj['name']):
            project_mng(proj)
