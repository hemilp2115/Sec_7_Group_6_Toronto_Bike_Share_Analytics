import streamlit as st
import pandas as pd
import altair as alt

# IMPORT FIX: Change the source of the core functions
from data_processor import load_data, clean_column_names, convert_dates 
# Import analysis functions that remain in analysis.py
from analysis import get_user_type_distribution, create_duration_buckets,get_avg_duration_by_hour,count_trips_by_day

# Define the file path
DATA_FILEPATH = 'Bike share ridership 2024-08.csv.gz' 

def main():
    st.set_page_config(layout="wide", page_title="Toronto Bike-Sharing Analytics")

    st.title("Toronto Bike-Sharing Analytics Dashboard (Sprint 1 Complete)")
    st.markdown("---")

    # 1. Load Data (US-01)
    raw_data = load_data(DATA_FILEPATH)

    if raw_data.empty:
        st.error("Error loading data. Check file path and data format.")
        return

    # 2. Complete Processing Pipeline (US-02 & US-03)
    data = clean_column_names(raw_data.copy())
    data = convert_dates(data) 
    
    # --- SPRINT 1 DELIVERABLES ---
    
    # US-08: KPI Metrics 
    col1, col2, col3 = st.columns(3)
    total_trips = len(data)
    avg_duration_str = get_avg_duration_by_hour(raw_data)
    
    with col1:
        st.metric("Total Trips Processed", f"{total_trips:,}")
    
    with col2:
        st.metric("Avg Trip Duration", avg_duration_str)
    
    with col3:
        # Calculate percentage for US-09 KPI
        user_distribution = get_user_type_distribution(data)
        member_percent = (user_distribution.get('Annual Member', 0) / user_distribution.sum()) * 100
        st.metric("Annual Member Ratio", f"{member_percent:.1f}%")

    st.markdown("---")
    
    # US-09: Display User Type Distribution
    st.subheader("User Type Distribution (US-09)")
    st.bar_chart(user_distribution)
    
    # --- US-14: Display Trip Duration Buckets ---
    st.subheader("Trip Duration Analysis (US-14)")
    duration_counts = create_duration_buckets(data)
    st.bar_chart(duration_counts)
    
    st.subheader("Processed Data Preview (First 5 Rows)")
    st.dataframe(data.head())

    st.subheader("User Type Distribution (US-11 Pie Chart)")

# Get data from existing function
    user_counts = get_user_type_distribution(data)

# Create a dataframe for the chart
    chart_data = pd.DataFrame({
    'User Type': user_counts.index,
    'Count': user_counts.values
    })

    # US-11 Display as a donut chart or pie chart
    st.altair_chart(
        alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="User Type", type="nominal"),
            tooltip=['User Type', 'Count']
        ),
        use_container_width=True
    )
    # US - 7
    st.markdown("---")
    st.subheader("Daily Trip Trends (US-07)")

    # 1. Get the data
    daily_counts = count_trips_by_day(data)

    # 2. Display Line Chart
    st.line_chart(daily_counts)


if __name__ == "__main__":
    main()