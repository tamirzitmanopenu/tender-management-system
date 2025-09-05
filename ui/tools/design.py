import streamlit as st


def set_rtl():
    st.markdown("""
    <style>
      /* Apply global RTL */
      html, body {
        direction: rtl;
        unicode-bidi: isolate;
      }

      /* Force charts and visualizations to LTR */
      .stPlotlyChart, .stVegaLiteChart, .vega-embed, .js-plotly-plot {
        direction: ltr !important;
        text-align: left !important;
      }

      /* Sidebar RTL */
      [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
      }

      /* Fix for collapsed navigation pane - prevent content overflow */
      [data-testid="stSidebar"][aria-expanded="false"] {
        width: 0 !important;
        min-width: 0 !important;
        overflow: hidden !important;
      }

      [data-testid="stSidebar"][aria-expanded="false"] > div {
        display: none !important;
      }

      /* Fix collapse/expand arrow direction for RTL */
      [data-testid="collapsedControl"] svg,
      [data-testid="baseButton-header"] svg,
      button[kind="header"] svg {
        transform: scaleX(-1) !important;
      }

      /* Ensure sidebar toggle button is positioned correctly */
      [data-testid="collapsedControl"] {
        right: auto !important;
        left: 1rem !important;
      }

      /* Common form elements and labels */
      label, input, textarea, select, .stTextInput input, .stTextArea textarea, .stSelectbox, .stRadio {
        direction: rtl;
        text-align: right;
      }

      /* Markdown text containers */
      .markdown-text-container {
        text-align: right;
      }

      /* Checkbox labels */
      .stCheckbox > label {
        direction: rtl;
        text-align: right;
      }

      /* Buttons: RTL text, LTR icon */
      [data-testid="stButton"] > button {
        direction: rtl;
        unicode-bidi: isolate-override;
        display: inline-flex;
        align-items: center;
        gap: .4rem;
      }

      [data-testid="stButton"] .material-icons,
      [data-testid="stButton"] [class^="material-icons"] {
        direction: ltr !important;
        unicode-bidi: isolate !important;
      }

      /* Expander spacing fix - target the actual HTML structure */
      .stExpander summary .st-emotion-cache-c36nl0 {
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        flex-direction: row !important;
      }

      /* Target the icon container specifically */
      .stExpander summary [data-testid="stIconMaterial"] {
        margin-left: 0.5rem !important;
        margin-right: 0 !important;
      }

      /* Target the markdown container in expander */
      .stExpander summary [data-testid="stMarkdownContainer"] {
        margin-right: 0.5rem !important;
        margin-left: 0 !important;
      }

    </style>
    """, unsafe_allow_html=True)