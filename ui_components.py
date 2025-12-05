import streamlit as st
import pandas as pd
import altair as alt

def render_kpi_row(total_trips, avg_duration_str, member_percent):
    """Renders the top row of KPI metrics."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Trips", f"{total_trips:,}")
    with col2:
        st.metric("Avg Trip Duration", avg_duration_str)
    with col3:
        st.metric("Annual Member Ratio", f"{member_percent:.1f}%")

def render_daily_trends(daily_counts):
    """Renders the daily trend line chart."""
    st.subheader("Daily Trip Trends (US-07)")
    st.line_chart(daily_counts, height=350)

def render_user_distribution(user_dist):
    """Renders the user type donut chart."""
    st.subheader("User Distribution (US-11)")
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

def render_duration_buckets(duration_counts):
    """Renders the trip duration bar chart."""
    st.subheader("Trip Duration Buckets (US-14)")
    st.bar_chart(duration_counts, height=350)

def render_peak_hours(peak_hour_data):
    """Renders the peak hour bar chart."""
    st.subheader("Peak Hour Avg Duration (US-10)")
    st.bar_chart(peak_hour_data, height=350)

def render_top_stations(top_stations):
    """Renders the top stations dataframe."""
    st.subheader("Top 5 Start Stations (US-06)")
    st.dataframe(top_stations, use_container_width=True, hide_index=True)

def render_data_preview(df):
    """Renders the raw data preview."""
    st.subheader("Filtered Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
