import matplotlib.pyplot as plt
import seaborn as sns
from visualization_utils import get_color_palette
import pandas as pd



def plot_correlation_matrix(correlation_matrix, title="Metric Correlations"):
    """Plot correlation matrix heatmap"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(pd.DataFrame(correlation_matrix), 
                annot=True, 
                cmap='coolwarm', 
                center=0,
                vmin=-1, 
                vmax=1)
    plt.title(title)
    return plt.gcf()

def plot_metric_scatter(data, x_metric, y_metric, title=None):
    """Create scatter plot for two metrics"""
    plt.figure(figsize=(10, 6))
    palette = get_color_palette()
    
    plt.scatter(data[x_metric], data[y_metric], 
               color=palette[0], alpha=0.5)
    plt.xlabel(x_metric)
    plt.ylabel(y_metric)
    
    if title:
        plt.title(title)
    
    return plt.gcf()