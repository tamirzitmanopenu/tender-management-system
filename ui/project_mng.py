import streamlit as st
from tools.helpers import business_category_selection
from settings.constants import SELECT_PROJECT
from tools.fetch_data import fetch_projects
from tools.helpers import project_del, project_files

st.header("פרויקטים")

with st.container(border=True):
    projects = fetch_projects()
    if projects:
        project_name = st.selectbox(SELECT_PROJECT, list(projects.keys()))
        project_id = projects.get(project_name)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("קבצי פרויקט", width="stretch"):
                project_files(project_id)
        with c2:
            if st.button("מחיקה", width="stretch"):
                project_del(project_id)
        if st.button(label="הקצאת קבלני משנה לפריוקט", width="stretch", type="primary"):
            business_category_selection(project_id)


    else:
        st.info("לא נמצאו פרויקטים במערכת")
