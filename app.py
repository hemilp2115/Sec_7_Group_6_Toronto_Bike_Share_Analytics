import streamlit as st
import pandas as pd
# Import load_data from Member A's work
from analysis import load_data 
# NOTE: You will need to add clean_column_names, convert_dates later

# Define the file path (make sure the data file is in the root directory)
DATA_FILEPATH = 'Bike share ridership 2024-08.csv.gz' 

def main():
    st.set_page_config(layout="wide", page_title="Toronto Bike-Sharing Analytics")

    st.title("Toronto Bike-Sharing Analytics Dashboard")
    st.markdown("---")

    # 1. Load Data (US-01: Member A's work)
    data = load_data(DATA_FILEPATH)

    if data.empty:
        st.error("Error loading data. Check file path and data format.")
        return

    # --- US-08: KPI Metrics (Implementation) ---
    col1, col2, col3 = st.columns(3)
    
    # Calculate Total Trips using the loaded DataFrame
    total_trips = len(data) 
    
    with col1:
        st.metric("Total Trips in Dataset", f"{total_trips:,}")
    
    with col2:
        st.metric("Avg Trip Duration (Sec)", "TBD (Sprint 2)") # Placeholder
    
    with col3:
        st.metric("User Distribution", "TBD (Sprint 2)") # Placeholder

    st.markdown("---")
    st.subheader("Data Preview (Raw)")
    st.dataframe(data.head())


if __name__ == "__main__":
    main()