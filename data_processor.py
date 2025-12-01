import pandas as pd
from typing import Union
import streamlit as st

# --- US-01: Load Raw Dataset ---
@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads the bike share data from a given CSV file path.
    """
    try:
        # Uses compression='gzip' to correctly read the .csv.gz file.
        df = pd.read_csv(filepath, encoding='utf-8', compression='gzip')
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return pd.DataFrame()


# --- US-02: Clean Column Names ---
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts column names to snake_case and fixes known issues (e.g., double spaces).
    """
    # Helper function to clean a single column string
    def clean_name(col: str) -> str:
        # 1. Replace multiple spaces with one space (handles the 'Trip  Duration' issue)
        cleaned_col = col.replace('  ', ' ')
        # 2. Convert to lowercase and replace spaces with underscores (snake_case)
        return cleaned_col.lower().replace(' ', '_')
    
    # Use a dictionary comprehension for clear mapping of old names to new names
    new_columns = {col: clean_name(col) for col in df.columns}
    
    # Rename the columns and return the DataFrame
    return df.rename(columns=new_columns)


# --- US-03: Convert Date Columns ---
def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts specified time columns to datetime objects using a standard format.
    """
    # Local constants for clarity
    DATE_COLUMNS = ['start_time', 'end_time']
    DATE_FORMAT = '%m/%d/%Y %H:%M'
    
    # Use .copy() to prevent SettingWithCopyWarning
    processed_df = df.copy() 
    
    for col in DATE_COLUMNS:
        processed_df[col] = pd.to_datetime(
            processed_df[col], 
            format=DATE_FORMAT, 
            errors='coerce'  # Converts unparseable dates to NaT
        )
        
    return processed_df

# US-04:filter invalid trips 
def filter_invalid_trips(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters out trips with unrealistic durations to ensure analysis quality.
    
    Criteria:
    - Removes trips shorter than 60 seconds (1 minute).
    - Removes trips longer than 10,800 seconds (3 hours).
    """
    # Define constants to avoid 'magic numbers'
    MIN_DURATION_SECONDS = 60
    MAX_DURATION_SECONDS = 10800 # 3 hours
    
    # Use boolean indexing to filter the data
    # We use .copy() to ensure we return a new DataFrame, preventing SettingWithCopyWarning
    valid_trips = df[
        (df['trip_duration'] >= MIN_DURATION_SECONDS) & 
        (df['trip_duration'] <= MAX_DURATION_SECONDS)
    ].copy()
    
    return valid_trips
