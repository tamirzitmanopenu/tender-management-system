import streamlit as st


def set_rtl():
    st.markdown("""
    <style>
      /* App layout RTL */
      body, html { direction: rtl; unicode-bidi: plaintext; }

      /* Charts must stay LTR so axes don't shift */
      .stVegaLiteChart, .vega-embed, .stPlotlyChart, .js-plotly-plot {
        direction: ltr !important;
        text-align: left !important;
      }
    </style>
    """, unsafe_allow_html=True)
