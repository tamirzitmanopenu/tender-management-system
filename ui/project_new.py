import streamlit as st
from tools.api import post, get

st.header("פרויקט חדש")

with st.form("add_project"):
    name = st.text_input("שם פרויקט")
    deadline = st.date_input("תאריך יעד")
    uploaded_skn = st.file_uploader("בחר קובץ כתב כמויות",type='skn')
    uploaded_other = st.file_uploader("בחר קובץ נוסף")
    file_type = st.text_input("סוג קובץ",)

    submitted = st.form_submit_button("שמור")

if submitted:
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
    else:
        st.error("נכשלה יצירת הפרויקט")


