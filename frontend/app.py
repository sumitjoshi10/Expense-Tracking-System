import streamlit as st
from add_update import add_update_tab
from analytics_by_category import anaytics_by_category_tab
from analytics_by_month import analytics_by_month_tab


st.title("Expense Tracker")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics By Month"])

with tab1:
    add_update_tab()
  
with tab2:
    anaytics_by_category_tab()

with tab3:
    analytics_by_month_tab()