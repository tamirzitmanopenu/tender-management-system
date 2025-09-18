import streamlit as st

from tools.api import post
from settings.constants import (
    ICON_SEND,
    OFFER_CATEGORY_DISPLAY_CAPTION,
    OFFER_HEADER,
    OFFER_MIN_UNIT_PRICE,
    OFFER_NO_BUSINESS_CATEGORY_ERROR,
    OFFER_NO_PROJECTS_WARNING,
    OFFER_NO_TASKS_INFO,
    OFFER_QUANTITY_CAPTION_TEMPLATE,
    OFFER_SELECT_CATEGORY,
    OFFER_SUBMIT_BTN,
    OFFER_SUBMIT_ERROR,
    OFFER_SUBMIT_SUCCESS,
    OFFER_TASK_TOTAL_TEMPLATE,
    OFFER_TOTAL_SUM_TEMPLATE,
    OFFER_UNIT_CAPTION_TEMPLATE,
    OFFER_UNIT_PRICE_LABEL,
    OFFER_UNIT_PRICE_STEP,
    SELECT_PROJECT,
)
from tools.fetch_data import fetch_business_category, fetch_projects, fetch_categories, fetch_tasks, fetch_user_details
from tools.auth import get_username

from tools.helpers import require_permission


@require_permission('Admin', 'Supplier')
def offer_new():
    st.header(OFFER_HEADER)
    username = get_username()
    user_details = fetch_user_details(username)
    if user_details['user_type'] == 'supplier':
        projects: list[dict] = fetch_projects(username)
    else:
        projects: list[dict] = fetch_projects()

    if not projects:
        st.warning(OFFER_NO_PROJECTS_WARNING)
        st.stop()

    project_map = {p['name']: p for p in projects}

    project_name = st.selectbox(SELECT_PROJECT, [p['name'] for p in projects])
    project_id = project_map[project_name]['project_id']

    categories = fetch_categories(project_id=project_id, user=username)
    category_name = st.selectbox(OFFER_SELECT_CATEGORY, list(categories.keys()))
    category_id = categories.get(category_name)
    st.caption(OFFER_CATEGORY_DISPLAY_CAPTION.format(category_name=category_name))

    tasks = fetch_tasks(project_id, category_id) if project_id and category_id else []
    if not tasks:
        st.info(OFFER_NO_TASKS_INFO)
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
                    st.caption(f"{task['sub_category']}")
                    st.markdown(f"**{task['description']}**")

                    st.caption(OFFER_UNIT_CAPTION_TEMPLATE.format(unit=task['unit']))
                    st.caption(OFFER_QUANTITY_CAPTION_TEMPLATE.format(quantity=quantity))

                with col2:
                    unit_price = st.number_input(
                        OFFER_UNIT_PRICE_LABEL,
                        min_value=OFFER_MIN_UNIT_PRICE,
                        step=OFFER_UNIT_PRICE_STEP,
                        value=current_price,
                        key=f"task_{task_id}",
                        on_change=update_price,
                        args=(task_id, current_price)
                    )
                    st.session_state.prices[task_id] = unit_price
                    total_price = unit_price * quantity
                    st.write(OFFER_TASK_TOTAL_TEMPLATE.format(value=total_price))
                    total_sum += total_price

                st.divider()

        st.markdown(OFFER_TOTAL_SUM_TEMPLATE.format(value=total_sum))

        # Submit form
        submitted = st.button(OFFER_SUBMIT_BTN, icon=ICON_SEND)
        prices = st.session_state.prices

    if submitted:
        items = [
            {"project_task_id": str(task_id), "price_offer": price}
            for task_id, price in prices.items()
        ]
        business_id = user_details.get('business_id')
        business_categories: list[dict] = fetch_business_category(category_id=category_id, business_id=business_id)
        if not business_categories:
            st.error(OFFER_NO_BUSINESS_CATEGORY_ERROR)
            st.stop()
        business_category_id = business_categories[0].get('business_category_id') if business_categories else None
        data = {
            "project_id": str(project_id),
            "business_category_id": str(business_category_id),
            "items": items,
        }
        resp = post("/offers", json=data)
        if resp.ok:
            st.success(OFFER_SUBMIT_SUCCESS)
        else:
            st.error(OFFER_SUBMIT_ERROR)
            print(f"resp.json(): {resp.json()}")


offer_new()
