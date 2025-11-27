import streamlit as st
import pandas as pd
# Import all final completed functions
from analysis import load_data, clean_column_names, convert_dates, get_user_type_distribution

# Define the file path
DATA_FILEPATH = 'Bike share ridership 2024-08.csv.gz' 

# The main function to run the Streamlit app
def main():
    st.set_page_config(layout="wide", page_title="Toronto Bike-Sharing Analytics")

    st.title("🚴 Toronto Bike-Sharing Analytics Dashboard (Sprint 1 Complete)")
    st.markdown("---")

    # 1. Load Data (US-01)
    raw_data = load_data(DATA_FILEPATH)

    if raw_data.empty:
        st.error("Error loading data. Check file path and data format.")
        return

    # 2. Complete Processing Pipeline (US-02 & US-03)
    # The pipeline is fully executed here, preparing the data for analysis
    data = clean_column_names(raw_data.copy())
    data = convert_dates(data) 
    
    # --- SPRINT 1 DELIVERABLES ---
    
    # US-08: KPI Metrics (Updated to use clean data length)
    col1, col2, col3 = st.columns(3)
    total_trips = len(data)
    
    with col1:
        st.metric("Total Trips Processed", f"{total_trips:,}")
    
    with col2:
        st.metric("Avg Trip Duration", "TBD (Sprint 2 Analytics)") 
    
    with col3:
        # Calculate percentage for US-09 KPI
        user_distribution = get_user_type_distribution(data)
        member_percent = (user_distribution.get('annual_member', 0) / user_distribution.sum()) * 100
        st.metric("Annual Member Ratio", f"{member_percent:.1f}%")

    st.markdown("---")
    
    # US-09: Display User Type Distribution
    st.subheader("User Type Distribution (US-09)")
    st.bar_chart(user_distribution)
    
    st.subheader("Processed Data Preview (First 5 Rows)")
    st.dataframe(data.head())


if __name__ == "__main__":
    main()

