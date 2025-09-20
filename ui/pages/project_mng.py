import streamlit as st
from tools.helpers import business_category_selection
from settings.constants import (
    BUTTON_TYPE_PRIMARY,
    ICON_ASSIGN,
    ICON_DELETE,
    ICON_EDIT,
    ICON_FILES,
    NAV_PROJECTS,
    PROJECT_ASSIGN_BUSINESS_BTN,
    PROJECT_DEADLINE_NOT_SET,
    PROJECT_DELETE_BTN,
    PROJECT_EDIT_BTN,
    PROJECT_FILES_BTN,
    PROJECTS_EMPTY_INFO,
    SELECT_PROJECT,
    UI_WIDTH_STRETCH,
)
from tools.fetch_data import fetch_projects
from tools.helpers import project_del, project_files, project_edit

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
            project_deadline = project_map[project_name].get('deadline_date', PROJECT_DEADLINE_NOT_SET)
            
            # כפתורי פעולות בשלוש עמודות
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(PROJECT_FILES_BTN, icon=ICON_FILES, width=UI_WIDTH_STRETCH):
                    project_files(project_id)
            with c2:
                if st.button(PROJECT_EDIT_BTN, icon=ICON_EDIT, width=UI_WIDTH_STRETCH):
                    project_edit(project_map[project_name])
            with c3:
                if st.button(PROJECT_DELETE_BTN, icon=ICON_DELETE, width=UI_WIDTH_STRETCH):
                    project_del(project_id)
            if st.button(
                PROJECT_ASSIGN_BUSINESS_BTN,
                width=UI_WIDTH_STRETCH,
                type=BUTTON_TYPE_PRIMARY,
                icon=ICON_ASSIGN,
            ):
                business_category_selection(project={"project_id": project_id, "project_name": project_name,
                                                     "project_deadline": project_deadline})


        else:
            st.info(PROJECTS_EMPTY_INFO)


project_mng()
