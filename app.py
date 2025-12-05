import streamlit as st
import pandas as pd
import altair as alt

# Import core processing functions
from data_processor import load_data, clean_column_names, convert_dates

# Import ALL analysis functions 
from analysis import (
    get_user_type_distribution, 
    create_duration_buckets, 
    count_trips_by_day, 
    get_avg_duration_by_hour, 
    get_top_start_stations 
)

# Define the file path
DATA_FILEPATH = 'Bike share ridership 2024-08.csv.gz' 

def main():
    # Page Config
    st.set_page_config(layout="wide", page_title="Toronto Bike-Sharing Analytics", page_icon="") # Removed emoji

    # --- 1. Load & Process Data ---
    raw_data = load_data(DATA_FILEPATH)

    if raw_data.empty:
        st.error("Error loading data. Check file path and data format.")
        return

    # Clean and Convert
    clean_data = clean_column_names(raw_data.copy())
    processed_data = convert_dates(clean_data) 

    # --- 2. SIDEBAR FILTERS (US-12) ---
    st.sidebar.header("Dashboard Filters") # Removed emoji
    
    # User Type Filter
    if 'user_type' in processed_data.columns:
        user_types = processed_data['user_type'].unique().tolist()
        selected_user_types = st.sidebar.multiselect(
            "Select User Type",
            options=user_types,
            default=user_types
        )
    else:
        selected_user_types = []

    # Apply Filter logic
    if not selected_user_types:
        st.sidebar.warning("Please select at least one User Type.")
        filtered_data = processed_data.copy()
    else:
        filtered_data = processed_data[processed_data['user_type'].isin(selected_user_types)]

    # --- 3. DASHBOARD MAIN AREA ---
    st.title("Toronto Bike-Sharing Analytics", text_alignment='center') # Removed emoji
    st.markdown("---")

    # --- ROW 1: KPI METRICS ---
    col1, col2, col3 = st.columns(3)
    
    total_trips = len(filtered_data)
    
    # FIX: Calculate Average Trip Duration (Dynamic)
    if total_trips > 0 and 'trip_duration' in filtered_data.columns:
        avg_duration_secs = filtered_data['trip_duration'].mean()
        avg_duration_str = f"{avg_duration_secs / 60:.1f} min"
    else:
        avg_duration_str = "0 min"

    # Calculate Member Ratio
    if total_trips > 0 and 'user_type' in filtered_data.columns:
        # Check for 'Annual Member' (adjust string if your data uses different casing)
        member_count = filtered_data[filtered_data['user_type'].astype(str).str.contains('Annual', case=False)].shape[0]
        member_percent = (member_count / total_trips) * 100
    else:
        member_percent = 0

    with col1:
        st.metric("Total Trips", f"{total_trips:,}")
    
    with col2:
        st.metric("Avg Trip Duration", avg_duration_str) 
    
    with col3:
        st.metric("Annual Member Ratio", f"{member_percent:.1f}%")

    st.markdown("---")

    # --- ROW 2: Daily Trend & User Dist ---
    row2_col1, row2_col2 = st.columns((2, 1)) 
    
    with row2_col1:
        st.subheader("Daily Trip Trends (US-07)") # Removed emoji
        daily_counts = count_trips_by_day(filtered_data)
        st.line_chart(daily_counts, height=350)
        
    with row2_col2:
        st.subheader("User Distribution (US-11)") # Removed emoji
        user_dist = get_user_type_distribution(filtered_data)
        
        if not user_dist.empty:
            chart_df = pd.DataFrame({'Type': user_dist.index, 'Count': user_dist.values})
            donut_chart = alt.Chart(chart_df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Type", type="nominal"),
                tooltip=['Type', 'Count']
            )
            st.altair_chart(donut_chart, use_container_width=True)
        else:
            st.info("No data for chart.")

    st.markdown("---")

    # --- ROW 3: Trip Duration & Peak Hours ---
    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:
        st.subheader("Trip Duration Buckets (US-14)") # Removed emoji
        duration_counts = create_duration_buckets(filtered_data)
        st.bar_chart(duration_counts, height=350)
        
    with row3_col2:
        st.subheader("Peak Hour Avg Duration (US-10)") # Removed emoji
        peak_hour_data = get_avg_duration_by_hour(filtered_data)
        st.bar_chart(peak_hour_data, height=350)

    st.markdown("---")

    # --- ROW 4: Top Stations & Data Table ---
    row4_col1, row4_col2 = st.columns((1, 2))
    
    with row4_col1:
        st.subheader("Top 5 Start Stations") # Removed emoji
        top_stations = get_top_start_stations(filtered_data, n=5)
        st.dataframe(top_stations, use_container_width=True, hide_index=True)
        
    with row4_col2:
        st.subheader("Filtered Data Preview") # Removed emoji
        st.dataframe(filtered_data.head(10), use_container_width=True)

if __name__ == "__main__":
    main()