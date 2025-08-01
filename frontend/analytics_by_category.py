import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"  # Adjust this URL based on your FastAPI server

def anaytics_by_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))
        
    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics/category", json=payload)
        
        if response.status_code == 200:
            response = response.json()
            data = {
                "category": list(response.keys()),
                "total_amount": [item["total_amount"] for item in response.values()],
                "percentage": [item["percentage"] for item in response.values()]
            }
            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by="total_amount", ascending=False)
            
            
            st.title("Expense Breakdown By Category")
            st.bar_chart(df_sorted.set_index("category")["percentage"], width=0, height=0, use_container_width=True)
            
            df_sorted["total_amount"] = df_sorted["total_amount"].map("{:.2f}".format)
            df_sorted["percentage"] = df_sorted["percentage"].map("{:.2f}".format)
            st.table(df_sorted)
        
        else:
            st.error("Failed to fetch analytics data")
        