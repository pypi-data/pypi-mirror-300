import pytest
import pandas as pd
from python_analysis.statistics import correlation, t_test  # Import your t_test function

def test_correlation():
    df = pd.DataFrame({'A': [5, 8, 3], 'B': [4, 9, 6]})
    expected_corr = df['A'].corr(df['B'])
    assert correlation(df, 'A', 'B') == pytest.approx(expected_corr, rel=1e-2)

def test_t_test():
    sample1 = [1, 2, 3]
    sample2 = [4, 5, 6]
    t_stat, p_value = t_test(sample1, sample2)
    # You can assert the results of the t-test here based on what you expect
    assert p_value < 0.05  # Example: assuming p_value should be less than 0.05
