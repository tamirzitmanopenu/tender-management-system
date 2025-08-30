import streamlit as st
from tools.api import get

st.header("ניהול ספקים")

resp = get("/businesses")
if resp.ok:
    suppliers = resp.json()
    if suppliers:
        st.dataframe(suppliers)
    else:
        st.info("אין ספקים")
else:
    st.error("שגיאה בשליפת ספקים")
