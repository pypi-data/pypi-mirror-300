import matplotlib.pyplot as plt

def plot_histogram(data, column):
    """Generate a histogram for a specified column in the dataset."""
    plt.hist(data[column], bins=20, color='green', edgecolor='black')
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

def plot_scatter(data, col1, col2):
    """Generate a scatter plot between two columns."""
    plt.scatter(data[x], data[y], color='green')
    plt.title(f'Scatter plot between {x} and {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()
