import pandas as pd
import numpy as np
from scipy import stats

def calculate_metric_correlations(interactions_df):
    """Calculate correlations between different interaction metrics"""
    # Calculate correlation matrix
    correlation_matrix = interactions_df[['plays', 'clears', 'likes', 'records']].corr()
    
    # Calculate statistical significance
    p_values = pd.DataFrame(np.zeros_like(correlation_matrix), 
                          columns=correlation_matrix.columns,
                          index=correlation_matrix.index)
    
    for i in correlation_matrix.columns:
        for j in correlation_matrix.index:
            if i != j:
                stat, p = stats.pearsonr(interactions_df[i], interactions_df[j])
                p_values.loc[i,j] = p
    
    return {
        'correlation_matrix': correlation_matrix.to_dict(),
        'p_values': p_values.to_dict(),
        'strongest_correlation': {
            'metrics': max([(i,j) for i in correlation_matrix.columns 
                          for j in correlation_matrix.index if i < j],
                          key=lambda x: abs(correlation_matrix.loc[x[0], x[1]])),
            'value': correlation_matrix.max().max()
        }
    }