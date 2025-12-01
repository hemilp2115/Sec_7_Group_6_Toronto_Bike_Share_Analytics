import pandas as pd
from typing import Union
# IMPORT FIX: We now import core processing functions from the new file
from data_processor import load_data, clean_column_names, convert_dates 


# --- US-09: Analyze User Types ---
def get_user_type_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the count of trips by User Type (Annual Member vs Casual Member).
    
    Assumes US-02 (clean column names) has been run, ensuring the column 
    is correctly named 'user_type'.
    """
    # Use value_counts() for a Series of counts, dropping any null entries.
    user_counts = df['user_type'].value_counts(dropna=True)
    
    return user_counts

def create_duration_buckets(df: pd.DataFrame) -> pd.Series:
    """
    Categorizes trip durations (in seconds) into meaningful time buckets.
    """
    # Define bins based on common Toronto trip lengths (e.g., 0-10 min, 10-30 min)
    bins = [0, 600, 1800, df['trip_duration'].max() + 1] 
    labels = ['Short (0-10m)', 'Medium (10-30m)', 'Long (>30m)']
    
    # Use pd.cut to categorize the data, assumes trip_duration is clean and exists
    df['duration_bucket'] = pd.cut(
        df['trip_duration'], 
        bins=bins, 
        labels=labels, 
        right=False # Sets the interval to be inclusive of the left side
    )
    return df['duration_bucket'].value_counts()

# --- US-05: Daily Trip Counts (Placeholder) ---
def count_trips_by_day(df: pd.DataFrame) -> pd.Series:
    """
    Placeholder for US-05.
    Calculates the total number of trips for each date.
    """
    # We return an empty Series or None to ensure the test runs but fails the assertion
    return pd.Series(dtype='int')

if __name__ == '__main__':
    # This block demonstrates the functionality of the analysis module.
    
    # 1. Define the file path (use the actual file name from your project)
    FILEPATH = 'Bike share ridership 2024-08.csv.gz' 
    
    # 2. Load the data
    raw_data = load_data(FILEPATH)
    
    if not raw_data.empty:
        # 3. Apply the full processing pipeline (US-02 and US-03 from data_processor)
        processed_data = clean_column_names(raw_data.copy())
        processed_data = convert_dates(processed_data)
        
        print("\n--- Processed Data Head ---")
        print(processed_data.head())
        
        # 4. Run the US-09 analysis function
        distribution = get_user_type_distribution(processed_data)
        
        print("\n--- User Type Distribution (US-09) ---")
        print(distribution)
    else:
        print("Data loading failed. Check FILEPATH.")