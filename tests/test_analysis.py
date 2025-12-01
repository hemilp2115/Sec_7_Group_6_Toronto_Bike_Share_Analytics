import pandas as pd
import pytest
# --- NEW IMPORTS ---
from data_processor import clean_column_names, convert_dates 
from analysis import count_trips_by_day  # Keep analysis imports if needed for other tests

# Fixture to simulate the raw DataFrame structure
@pytest.fixture
def raw_df():
    """Returns a DataFrame with uncleaned column names and raw date strings."""
    data = {'Trip Id': [1, 2], 
            'Trip  Duration': [600, 1200], # US-02: Double space issue
            'Start Station Id': [7000, 7001], # US-02: Space issue
            'Start Time': ['08/01/2024 00:00', '08/02/2024 12:30'], # US-03: Raw date strings
            'End Time': ['08/01/2024 00:10', '08/02/2024 12:45'],
            'User Type': ['Annual Member', 'Casual Member']}
    return pd.DataFrame(data)

# --- US-02 (Verification Test) ---
# NOTE: This test should already pass after Member B's work is merged to main.
def test_us02_clean_column_names(raw_df):
    cleaned_df = clean_column_names(raw_df)
    assert 'trip_duration' in cleaned_df.columns
    assert 'start_station_id' in cleaned_df.columns
    assert 'Trip  Duration' not in cleaned_df.columns 

# --- US-03 TDD: RED Phase ---
def test_us03_convert_dates_fails(raw_df):
    """
    Tests that Start Time and End Time are correctly converted to datetime objects.
    This test MUST FAIL initially (RED) against the placeholder code.
    """
    # Run data through US-02 first
    cleaned_df = clean_column_names(raw_df)
    
    # 1. ACT: Call the function
    processed_df = convert_dates(cleaned_df)
    
    # 2. ASSERT: Check that the DataFrame column type is datetime64
    assert pd.api.types.is_datetime64_any_dtype(processed_df['start_time'])
    assert pd.api.types.is_datetime64_any_dtype(processed_df['end_time'])

# --- US-05 TDD: RED Phase ---
def test_count_trips_by_day_fails():
    """
    Tests that trips are correctly counted by date.
    MUST FAIL initially.
    """
    # Create a simple dataframe with timestamps spanning two days
    data = {'start_time': pd.to_datetime([
        '2024-08-01 08:00', '2024-08-01 09:00', # 2 trips on Aug 1
        '2024-08-02 10:00'                      # 1 trip on Aug 2
    ])}
    df = pd.DataFrame(data)
    
    # ACT
    result = count_trips_by_day(df)
    
    # ASSERT
    # Expecting a Series where index is date and value is count
    assert len(result) == 2
    assert result.loc['2024-08-01'] == 2
    assert result.loc['2024-08-02'] == 1