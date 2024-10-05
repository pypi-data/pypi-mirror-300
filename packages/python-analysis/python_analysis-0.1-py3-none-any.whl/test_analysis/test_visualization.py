import pandas as pd
from python_analysis.visualization import plot_histogram

def test_plot_histogram():
    df = pd.DataFrame({'A': [1, 2, 2, 4]})
    # Ideally, we would check if the plot was generated.
    # Here we just ensure no exceptions are raised.
    plot_histogram(df, 'A')
