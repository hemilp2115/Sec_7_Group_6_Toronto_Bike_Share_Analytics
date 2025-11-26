import pandas as pd
import pytest
# Ensure you import the placeholder function from analysis.py
from analysis import clean_column_names 

# Fixture to create a raw DataFrame for testing. 
# This simulates the real data's messy column names.
@pytest.fixture
def raw_df():
    """Returns a DataFrame with uncleaned column names for testing."""
    data = {'Trip Id': [1], 
            'Trip  Duration': [600], # Note the double space!
            'Start Station Id': [7000],
            'User Type': ['Annual Member']}
    # Use index=False to keep the test data clean
    return pd.DataFrame(data)

# --- US-02 TDD: RED Phase ---
def test_us02_clean_column_names_fails(raw_df):
    """
    Tests that column names are converted to snake_case and fixes issues.
    This test MUST FAIL initially (RED).
    """
    # 1. ACT: Call the placeholder function (it currently does nothing)
    cleaned_df = clean_column_names(raw_df)
    
    # 2. ASSERT: Check for the expected cleaned column names
    # Note: We expect 'trip_duration' and 'start_station_id' to exist.
    assert 'trip_duration' in cleaned_df.columns
    assert 'start_station_id' in cleaned_df.columns
    
    # Run this test now by running 'pytest' in your terminal. It MUST FAIL