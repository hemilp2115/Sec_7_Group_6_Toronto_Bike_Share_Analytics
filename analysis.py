import pandas as pd
from typing import Union

# --- US-01: Load Raw Dataset ---
def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads the bike share data from a given CSV file path.
    """
    try:
        # Load the CSV. Using utf-8 is a good robust choice for data loading.
        df = pd.read_csv(filepath, encoding='utf-8',compression='gzip')
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return pd.DataFrame()

# --- US-02: Clean Column Names https://tree.taiga.io/project/harshpatel15-sec_7_group_6_agile_final_project/task/15 (Himani and Harsh) ---
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts column names to snake_case and fixes known issues like double spaces.
    """
    
    # --- REFACTOR IMPROVEMENT: Using a dictionary comprehension ---
    
    # 1. Define the function to clean a single column string
    def clean_name(col):
        # Fix double spaces, lowercase, and replace single spaces with underscore
        return col.replace('  ', ' ').lower().replace(' ', '_')
    
    # 2. Use a dictionary comprehension to map old names to new names
    new_columns = {col: clean_name(col) for col in df.columns}
    
    # 3. Rename the columns
    return df.rename(columns=new_columns)

# --- US-03: Convert Date Columns (Placeholder for Member C) ---
def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts 'Start Time' and 'End Time' to datetime objects.
    Assumes US-02 (clean columns) has been run.
    """
    # The format is 'MM/DD/YYYY HH:MM'
    date_format = '%m/%d/%Y %H:%M'
    
    # Use errors='coerce' to turn invalid/missing dates into NaT
    df['start_time'] = pd.to_datetime(df['start_time'], format=date_format, errors='coerce')
    df['end_time'] = pd.to_datetime(df['end_time'], format=date_format, errors='coerce')
    
    return df


# --- US-09: Analyze User Types (Placeholder for Member A Day 2) ---
def get_user_type_distribution(df: pd.DataFrame) -> pd.Series:
    """Calculates the count of trips by User Type."""
    # Member A will implement the logic here
    return pd.Series() # Return a placeholder Series

if __name__ == '__main__' :
    
    bike_data = load_data('Bike share ridership 2024-08.csv.gz')
    print(bike_data.head())