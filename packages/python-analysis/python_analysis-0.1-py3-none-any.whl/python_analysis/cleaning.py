import pandas as pd

def fill_missing(df, method='mean'):
    """Fill missing values using the specified method."""
    if method == 'mean':
        return df.fillna(df.mean())
    elif method == 'median':
        return df.fillna(df.median())
    elif method == 'mode':
        return df.fillna(df.mode().iloc[0])
    else:
        raise ValueError("Method must be 'mean', 'median', or 'mode'")

def drop_duplicates(df):
    """Drop duplicate rows from the DataFrame."""
    return df.drop_duplicates()

