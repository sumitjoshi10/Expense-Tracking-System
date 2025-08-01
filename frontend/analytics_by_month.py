import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"  # Adjust this URL based on your FastAPI server

def analytics_by_month_tab():
    response = requests.get(f"{API_URL}/analytics/month")
    if response.status_code == 200:
        response = response.json()
        data = {
            "Month": [item["month"] for item in response],
            "Total Amount": [item["total_amount"] for item in response]
        }
        df_sorted = pd.DataFrame(data)
        # df_sorted = df.sort_values(by="Month")

        st.title("Expense Summary By Month")
        st.bar_chart(df_sorted.set_index("Month")["Total Amount"], width=0, height=0, use_container_width=True)

        df_sorted["Total Amount"] = df_sorted["Total Amount"].map("{:.2f}".format)
        st.table(df_sorted)
    else:
        st.error("Failed to fetch analytics data")

