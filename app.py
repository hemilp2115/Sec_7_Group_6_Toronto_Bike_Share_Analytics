import streamlit as st
import pandas as pd

# Import Core Logic
from data_processor import load_data, clean_column_names, convert_dates
from analysis import (
    get_user_type_distribution,
    create_duration_buckets,
    count_trips_by_day,
    get_avg_duration_by_hour,
    get_top_start_stations
)
# Import UI Components (The New Refactor)
import ui_components as ui

DATA_FILEPATH = 'Bike share ridership 2024-08.csv.gz'

def main():
    st.set_page_config(layout="wide", page_title="Toronto Bike-Sharing Analytics", page_icon="")

    # --- 1. Load & Process ---
    raw_data = load_data(DATA_FILEPATH)
    if raw_data.empty:
        st.error("Error loading data.")
        return

    clean_data = clean_column_names(raw_data.copy())
    processed_data = convert_dates(clean_data)

    # --- 2. Filters ---
    st.sidebar.header("Dashboard Filters")
    if 'user_type' in processed_data.columns:
        user_types = processed_data['user_type'].unique().tolist()
        selected_users = st.sidebar.multiselect("Select User Type", user_types, default=user_types)
    else:
        selected_users = []

    if not selected_users:
        st.sidebar.warning("Select at least one User Type.")
        filtered_data = processed_data.copy()
    else:
        filtered_data = processed_data[processed_data['user_type'].isin(selected_users)]

    # --- 3. Calculations ---
    # Perform all calculations upfront (Controller Logic)
    total_trips = len(filtered_data)
    
    avg_dur = 0
    if total_trips > 0 and 'trip_duration' in filtered_data.columns:
        avg_dur = filtered_data['trip_duration'].mean()
    avg_duration_str = f"{avg_dur / 60:.1f} min" if total_trips > 0 else "0 min"

    member_pct = 0
    if total_trips > 0 and 'user_type' in filtered_data.columns:
        m_count = filtered_data[filtered_data['user_type'].astype(str).str.contains('Annual', case=False)].shape[0]
        member_pct = (m_count / total_trips) * 100

    # Analytics results
    daily_counts = count_trips_by_day(filtered_data)
    user_dist = get_user_type_distribution(filtered_data)
    dur_buckets = create_duration_buckets(filtered_data)
    peak_hours = get_avg_duration_by_hour(filtered_data)
    top_stations = get_top_start_stations(filtered_data, n=5)

    # --- 4. Render UI (View Logic) ---
    st.title("Toronto Bike-Sharing Analytics", text_alignment='center')

    st.markdown("---")

    # Row 1: KPIs
    ui.render_kpi_row(total_trips, avg_duration_str, member_pct)
    st.markdown("---")

    # Row 2: Trends & Users
    row2_1, row2_2 = st.columns((2, 1))
    with row2_1:
        ui.render_daily_trends(daily_counts)
    with row2_2:
        ui.render_user_distribution(user_dist)
    st.markdown("---")

    # Row 3: Duration & Peak Hours
    row3_1, row3_2 = st.columns(2)
    with row3_1:
        ui.render_duration_buckets(dur_buckets)
    with row3_2:
        ui.render_peak_hours(peak_hours)
    st.markdown("---")

    # Row 4: Stations & Preview
    row4_1, row4_2 = st.columns((1, 2))
    with row4_1:
        ui.render_top_stations(top_stations)
    with row4_2:
        ui.render_data_preview(filtered_data)

if __name__ == "__main__":
    main()
