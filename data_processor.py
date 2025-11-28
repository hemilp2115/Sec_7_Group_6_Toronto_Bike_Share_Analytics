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
    Converts specified time columns to datetime objects using a standard format.
    """
    # Define the columns and format clearly as constants
    DATE_COLUMNS = ['start_time', 'end_time']
    DATE_FORMAT = '%m/%d/%Y %H:%M'
 
    # Use .copy() to prevent SettingWithCopyWarning if downstream changes occur
    processed_df = df.copy() 
    
    for col in DATE_COLUMNS:
        # Process each column cleanly
        processed_df[col] = pd.to_datetime(
            processed_df[col], 
            format=DATE_FORMAT, 
            errors='coerce' # Converts unparseable dates to NaT
        )
        
    return processed_df
