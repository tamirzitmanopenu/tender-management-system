import streamlit as st

from tools.api import post
from settings.constants import (
    OFFER_HEADER,
    SELECT_PROJECT,
    OFFER_SELECT_CATEGORY,
    OFFER_SUBMIT_BTN,
    OFFER_SUBMIT_SUCCESS,
    OFFER_SUBMIT_ERROR,
)
from tools.fetch_data import fetch_projects, fetch_categories, fetch_tasks

st.header(OFFER_HEADER)

projects = fetch_projects()
project_name = st.selectbox(SELECT_PROJECT, list(projects.keys()))
project_id = projects.get(project_name)

categories = fetch_categories(project_id=project_id)
category_name = st.selectbox(OFFER_SELECT_CATEGORY, list(categories.keys()))
category_id = categories.get(category_name)
st.caption(f"מציג: {category_name}")

tasks = fetch_tasks(project_id, category_id) if project_id and category_id else []
if not tasks:
    st.info("לא נמצאו משימות בקטגוריה זו")
    st.stop()
with st.container(border=True):
    # Function to update total price
    def update_price(t_id, p):
        st.session_state.prices[t_id] = p


    total_sum = 0.0
    # Display tasks and prices
    for task in tasks:
        with st.container():
            col1, col2 = st.columns([3, 1])

            task_id = task['project_task_id']
            current_price = st.session_state.prices.get(task_id, 0.0)
            quantity = task.get('quantity', 0)

            with col1:
                st.markdown(f"**{task['description']}**")
                st.caption(f"יחידת מידה: {task['unit']}")
                st.caption(f"כמות: {quantity}")

            with col2:
                unit_price = st.number_input(
                    "מחיר ליחידה",
                    min_value=0.0,
                    step=5.0,
                    value=current_price,
                    key=f"task_{task_id}",
                    on_change=update_price,
                    args=(task_id, current_price)
                )
                st.session_state.prices[task_id] = unit_price
                total_price = unit_price * quantity
                st.write(f"סה\"כ: ₪{total_price:,.2f}")
                total_sum += total_price

            st.divider()

    st.markdown(f"### סה\"כ הצעת מחיר: ₪{total_sum:,.2f}")

    # Submit form
    submitted = st.button(OFFER_SUBMIT_BTN)
    prices = st.session_state.prices

if submitted:
    items = [
        {"project_task_id": str(task_id), "price_offer": price}
        for task_id, price in prices.items()
    ]
    data = {
        "project_id": str(project_id),
        "business_category_id": str(category_id),
        "items": items,
    }
    resp = post("/offers", json=data)
    if resp.ok:
        st.success(OFFER_SUBMIT_SUCCESS)
    else:
        st.error(OFFER_SUBMIT_ERROR)
