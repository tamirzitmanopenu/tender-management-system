import streamlit as st
from tools.helpers import business_category_selection
from settings.constants import (
    NAV_PROJECTS,
    SELECT_PROJECT,
    PROJECT_FILES_BTN,
    PROJECT_DELETE_BTN,
    PROJECT_ASSIGN_BUSINESS_BTN,
    ICON_FILES,
    ICON_DELETE,
    ICON_ASSIGN,
)
from tools.fetch_data import fetch_projects
from tools.helpers import project_del, project_files

from tools.helpers import require_permission


@require_permission('Admin')
def project_mng():
    st.header(NAV_PROJECTS)

    with st.container(border=True):
        projects: list[dict] = fetch_projects()
        project_map = {p['name']: p for p in projects}
        if projects:
            project_name = st.selectbox(SELECT_PROJECT, [p['name'] for p in projects])
            project_id = project_map[project_name]['project_id']
            project_deadline = project_map[project_name].get('deadline_date', "טרם נקבע")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(PROJECT_FILES_BTN, icon=ICON_FILES, width="stretch"):
                    project_files(project_id)
            with c2:
                if st.button(PROJECT_DELETE_BTN, icon=ICON_DELETE, width="stretch"):
                    project_del(project_id)
            if st.button(PROJECT_ASSIGN_BUSINESS_BTN, width="stretch", type="primary", icon=ICON_ASSIGN):
                business_category_selection(project={"project_id": project_id, "project_name": project_name,
                                                     "project_deadline": project_deadline})


        else:
            st.info("לא נמצאו פרויקטים במערכת")


project_mng()
