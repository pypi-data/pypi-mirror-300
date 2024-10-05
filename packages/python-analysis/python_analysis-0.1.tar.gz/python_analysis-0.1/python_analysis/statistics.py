from scipy import stats

def correlation(df, col1, col2):
    """Compute correlation between two columns."""
    return df[col1].corr(df[col2])

def t_test(sample1, sample2):
    """Perform independent t-test between two samples."""
    t_stat, p_value = stats.ttest_ind(sample1, sample2)
    return t_stat, p_value
