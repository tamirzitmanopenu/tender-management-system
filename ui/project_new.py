import streamlit as st
from tools.api import post, get
from tools.fetch_data import fetch_business_category
from settings.constants import FIELD_LABELS

st.header("פרויקט חדש")
business_categories = fetch_business_category()
st.dataframe(business_categories)


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
    name = st.text_input("שם פרויקט", key='new_project_name')  # required
    deadline = st.date_input("תאריך יעד", key='new_deadline')   # required
    uploaded_skn = st.file_uploader("בחר קובץ כתב כמויות", type='skn', key='uploaded_skn')  # required
    uploaded_other = st.file_uploader("בחר קובץ נוסף", key='uploaded_other')
    file_type = st.text_input("סוג קובץ", key='file_type')

    submitted = st.form_submit_button(
        "שמור",
        on_click=validate_form,
        kwargs={'required_keys': ['new_project_name', 'new_deadline', 'uploaded_skn']}
    )

if submitted:
    # Show validation result after submission
    if st.session_state.get("error"):
        st.warning(st.session_state.error)
        st.stop()

    data = {"name": name, "deadline_date": str(deadline)}
    projects_resp = post("/projects", json=data)
    if projects_resp.ok:
        st.success(f"נוצר פרויקט {name}")
        project_id = projects_resp.json().get('project_id')
        if uploaded_skn:
            files = {"file": (uploaded_skn.name, uploaded_skn.getvalue())}
            data = {"project_id": project_id, "file_type": 'כתב כמויות'}
            skn_file_resp = post("/files", files=files, data=data)
            if skn_file_resp.ok:
                info = skn_file_resp.json()
                st.success(f"הועלה קובץ {uploaded_skn.name}")
                # Process SKN
                skn_file_id = info.get('file_id')
                with st.spinner():
                    process_skn_resp = post(f"/files/{skn_file_id}/process-skn")
                    if process_skn_resp.ok:
                        st.success("עיבוד כתב כמויות בוצע בהצלחה")
                    else:
                        st.error("נכשל עיבוד הקובץ")
            else:
                st.error("נכשלה העלאת הקובץ")
        if uploaded_other:
            files = {"file": (uploaded_other.name, uploaded_other.getvalue())}
            data = {"project_id": project_id, "file_type": file_type}
            resp = post("/files", files=files, data=data)
            if resp.ok:
                info = resp.json()
                st.success(f"הועלה קובץ {uploaded_other.name}")
            else:
                st.error("נכשלה העלאת הקובץ")
        ###
        # Business Category Selection:
        options = st.multiselect(
            "What are your favorite colors?",
            ["Green", "Yellow", "Red", "Blue"],
            default=["Yellow", "Red"],
        )
    else:
        st.error("נכשלה יצירת הפרויקט")
