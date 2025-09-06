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

      /* FIXED: Regular Buttons RTL with proper alignment */
      [data-testid="stButton"] > button {
        direction: rtl !important;
        text-align: right !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
        flex-direction: row-reverse !important;
        padding: 0.375rem 0.75rem !important;
        min-height: 38px !important;
        box-sizing: border-box !important;
      }

      /* FIXED: Form Submit Buttons - specific targeting */
      [data-testid="stFormSubmitButton"] button {
        direction: rtl !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-direction: row-reverse !important;
        gap: 0.25rem !important;
        padding: 0.375rem 0.75rem !important;
      }

      /* Fix Form Submit Button icon positioning */
      [data-testid="stFormSubmitButton"] button > span[data-testid="stIconMaterial"] {
        order: 2 !important;
        margin-left: 0.25rem !important;
        margin-right: 0 !important;
        flex-shrink: 0 !important;
      }

      /* Fix Form Submit Button text positioning */
      [data-testid="stFormSubmitButton"] button > div[data-testid="stMarkdownContainer"] {
        order: 1 !important;
        margin-right: 0 !important;
        margin-left: 0 !important;
        text-align: right !important;
      }

      /* Ensure form submit button text is properly aligned */
      [data-testid="stFormSubmitButton"] button p {
        margin: 0 !important;
        text-align: right !important;
        direction: rtl !important;
      }

      /* Handle regular button icons */
      [data-testid="stButton"] .material-icons,
      [data-testid="stButton"] [class^="material-icons"],
      [data-testid="stButton"] svg {
        direction: ltr !important;
        unicode-bidi: isolate !important;
        flex-shrink: 0 !important;
        margin: 0 !important;
      }

      /* Handle regular button text */
      [data-testid="stButton"] > button span,
      [data-testid="stButton"] > button p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
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