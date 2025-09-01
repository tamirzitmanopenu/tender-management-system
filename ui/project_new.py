import streamlit as st
from tools.api import post
from settings.constants import FIELD_LABELS, PROJECT_REQUIRED_FORM_KEYS, PROJECT_SKN_PROCESS_TEXT, \
    PROJECT_CREATION_SUCCESS_TEXT, PROJECT_SKN_UPLOAD_SUCCESS_TEXT, PROJECT_SKN_PROCESS_SUCCESS_TEXT, \
    PROJECT_SKN_PROCESS_FAILURE_TEXT, PROJECT_SKN_UPLOAD_FAILURE_TEXT, PROJECT_FILE_TYPE_SKN, \
    PROJECT_CREATION_FAILURE_TEXT, PROJECT_OTHER_UPLOAD_SUCCESS_TEXT, PROJECT_OTHER_UPLOAD_FAILURE_TEXT, ICON_PROJECTS
from tools.helpers import get_label

st.set_page_config(
    page_icon=ICON_PROJECTS
)

st.header("פרויקט חדש")


def validate_form(required_keys=None):
    if required_keys is None:
        required_keys = []

    errors = []
    for key in required_keys:
        value = st.session_state.get(key)
        label = FIELD_LABELS.get(key, key)  # ברירת מחדל לשם הטכני אם אין תרגום
        if isinstance(value, str) and not value.strip():
            errors.append(f"השדה '{label}' חסר")
        elif value is None:
            errors.append(f"השדה '{label}' חסר")

    if errors:
        st.session_state.error = " , ".join(errors)
    else:
        st.session_state.error = ""


with st.form("add_project"):
    name = st.text_input(get_label('new_project_name'), key='new_project_name')  # required
    deadline = st.date_input(get_label('new_deadline'), key='new_deadline')  # required
    uploaded_skn = st.file_uploader(get_label('uploaded_skn'), type='skn', key='uploaded_skn')  # required
    uploaded_other = st.file_uploader(get_label('uploaded_other'), key='uploaded_other')
    file_type = st.text_input(get_label('file_type'), key='file_type')

    submitted = st.form_submit_button(
        "שמור",
        on_click=validate_form,
        kwargs={'required_keys': PROJECT_REQUIRED_FORM_KEYS}
    )

if submitted:
    if st.session_state.get('error'):
        st.warning(st.session_state['error'])
        st.stop()

    data = {"name": name, "deadline_date": str(deadline)}
    projects_resp = post("/projects", json=data)
    if projects_resp.ok:
        st.success(PROJECT_CREATION_SUCCESS_TEXT.format(name=name))
    else:
        st.error(PROJECT_CREATION_FAILURE_TEXT)
        st.stop()

    project_id = projects_resp.json().get('project_id')

    if uploaded_skn:
        files = {"file": (uploaded_skn.name, uploaded_skn.getvalue())}
        data = {"project_id": project_id, "file_type": PROJECT_FILE_TYPE_SKN}
        skn_file_resp = post("/files", files=files, data=data)

        if skn_file_resp.ok:
            info = skn_file_resp.json()
            st.success(PROJECT_SKN_UPLOAD_SUCCESS_TEXT.format(filename=uploaded_skn.name))

            skn_file_id = info.get('file_id')
            with st.spinner(PROJECT_SKN_PROCESS_TEXT):
                process_skn_resp = post(f"/files/{skn_file_id}/process-skn")
                if process_skn_resp.ok:
                    st.success(PROJECT_SKN_PROCESS_SUCCESS_TEXT)
                else:
                    st.error(PROJECT_SKN_PROCESS_FAILURE_TEXT)
                    st.stop()
        else:
            st.error(PROJECT_SKN_UPLOAD_FAILURE_TEXT)
            st.stop()

    if uploaded_other:
        files = {"file": (uploaded_other.name, uploaded_other.getvalue())}
        data = {"project_id": project_id, "file_type": file_type}
        resp = post("/files", files=files, data=data)

        if resp.ok:
            info = resp.json()
            st.success(PROJECT_OTHER_UPLOAD_SUCCESS_TEXT.format(filename=uploaded_other.name))
        else:
            st.error(PROJECT_OTHER_UPLOAD_FAILURE_TEXT)
