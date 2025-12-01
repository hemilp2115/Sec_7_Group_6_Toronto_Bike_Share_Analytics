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

def get_avg_duration_by_hour(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the average trip duration for each hour of the day.
    """
    # Create a copy to avoid SettingWithCopyWarning on the original dataframe
    df_temp = df.copy()
    
    # Extract the hour (0-23) from the 'start_time' column
    df_temp['hour'] = df_temp['start_time'].dt.hour
    
    # Group by the hour and calculate the mean of 'trip_duration'
    avg_duration = df_temp.groupby('hour')['trip_duration'].mean()
    
    return avg_duration

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

        trip_duration_buckets = get_avg_duration_by_hour(processed_data)

        print("\n--- Peak hour analysis (US-05) ---")
        print(trip_duration_buckets)
    else:
        print("Data loading failed. Check FILEPATH.")