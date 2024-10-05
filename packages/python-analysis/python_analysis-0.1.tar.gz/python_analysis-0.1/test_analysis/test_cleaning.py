import pandas as pd
from python_analysis.cleaning import fill_missing, drop_duplicates

def test_fill_missing():
    df = pd.DataFrame({'A': [4, 8, None, 6]})
    result = fill_missing(df)
    # Check if there are no missing values left
    assert result.isnull().sum().sum() == 0, "There are still missing values in the DataFrame"

def test_drop_duplicates():
    df = pd.DataFrame({'A': [1, 2, 2, 4]})
    result = drop_duplicates(df)
    # Check if duplicates are removed
    assert result.shape[0] == 3 
