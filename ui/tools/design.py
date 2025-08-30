import streamlit as st


def set_rtl():
    st.markdown("""
    <style>
    body, html {
        direction: RTL;
        unicode-bidi: bidi-override;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

    # p, div, input, label, h1, h2, h3, h4, h5, h6 {
    #     direction: RTL;
    #     unicode-bidi: bidi-override;
    #     text-align: right;
    # }
