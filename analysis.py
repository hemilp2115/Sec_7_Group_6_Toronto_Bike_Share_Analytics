import pandas as pd
# IMPORT FIX: We now import core processing functions from the new file
from data_processor import load_data, clean_column_names, convert_dates 
from typing import Union


# --- US-09: Analyze User Types (Placeholder for Member A Day 2) ---
def get_user_type_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the count of trips by User Type (Annual Member vs Casual Member).
    Assumes US-02 has been run and column is named 'user_type'.
    """
    # Use value_counts() for a Series of counts
    user_counts = df['user_type'].value_counts(dropna=True)
    
    return user_counts

if __name__ == '__main__' :
    
    filename = 'data/toronto_bike_share_data.csv.gz'

    bike_data = load_data(filename)
    print(bike_data.head())