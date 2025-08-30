import streamlit as st
from tools.api import post, get

st.header("ניהול קבצים")

# Upload file
with st.form("upload_file"):
    project_id = st.text_input("מזהה פרויקט")
    file_type = st.selectbox("סוג קובץ", ["other", "boq"])
    uploaded = st.file_uploader("בחר קובץ")
    submit = st.form_submit_button("העלה")

if submit and uploaded:
    files = {"file": (uploaded.name, uploaded.getvalue())}
    data = {"project_id": project_id, "file_type": file_type}
    resp = post("/files", files=files, data=data)
    if resp.ok:
        info = resp.json()
        st.success(f"הועלה קובץ {info.get('file_id')}")
    else:
        st.error("נכשלה העלאת הקובץ")

# Process SKN
file_id = st.text_input("מזהה קובץ לעיבוד SKN")
if st.button("עבד SKN") and file_id:
    resp = post(f"/files/{file_id}/process-skn")
    if resp.ok:
        st.success("העיבוד בוצע")
    else:
        st.error("נכשל עיבוד הקובץ")
