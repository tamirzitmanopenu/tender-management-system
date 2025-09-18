import streamlit as st

from settings.constants import RTL_STYLE


def set_rtl():
    st.markdown(RTL_STYLE, unsafe_allow_html=True)
