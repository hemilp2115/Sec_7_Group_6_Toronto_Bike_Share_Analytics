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

# The rest of the file (US-02, US-03) remains as the initial placeholders
# for Member B and Member C to implement their TDD phases.

if __name__ == '__main__' :
    
    bike_data = load_data('Bike share ridership 2024-08.csv.gz')
    print(bike_data.head())