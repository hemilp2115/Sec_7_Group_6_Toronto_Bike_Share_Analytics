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


if __name__ == '__main__':
    # This block demonstrates the functionality of the analysis module.
    
    # 1. Define the file path (use the actual file name from your project)
    FILEPATH = 'Bike share ridership 2024-08.csv' 
    
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