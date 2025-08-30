import streamlit as st


def set_rtl():
    st.markdown(
        """
    <style>
    body, html {
        direction: RTL;
        unicode-bidi: bidi-override;
        text-align: right;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
