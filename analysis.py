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

# --- US-02: Clean Column Names (Placeholder for Member B) ---
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Converts column names to snake_case and fixes known issues."""
    # Member B will implement the logic here
    return df 

# --- US-03: Convert Date Columns (Placeholder for Member C) ---
def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Converts 'Start Time' and 'End Time' to datetime objects."""
    # Member C will implement the logic here
    return df

# --- US-09: Analyze User Types (Placeholder for Member A Day 2) ---
def get_user_type_distribution(df: pd.DataFrame) -> pd.Series:
    """Calculates the count of trips by User Type."""
    # Member A will implement the logic here
    return pd.Series() # Return a placeholder Series

if __name__ == '__main__' :
    
    bike_data = load_data('Bike share ridership 2024-08.csv.gz')
    print(bike_data.head())