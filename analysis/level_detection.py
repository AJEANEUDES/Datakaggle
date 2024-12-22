import numpy as np
import pandas as pd

def detect_problematic_levels(courses_df, interactions_df, thresholds=None):
    """Detect potentially problematic levels based on various metrics"""
    if thresholds is None:
        thresholds = {
            'clear_rate_min': 0.05,
            'like_ratio_min': 0.2,
            'play_count_min': 100
        }
    
    # Calculate metrics
    metrics = pd.DataFrame()
    metrics['clear_rate'] = interactions_df['clears'] / interactions_df['plays']
    metrics['like_ratio'] = interactions_df['likes'] / interactions_df['plays']
    metrics['play_count'] = interactions_df['plays']
    
    # Identify problematic levels
    problems = {
        'low_clear_rate': metrics[metrics['clear_rate'] < thresholds['clear_rate_min']].index.tolist(),
        'low_satisfaction': metrics[metrics['like_ratio'] < thresholds['like_ratio_min']].index.tolist(),
        'low_engagement': metrics[metrics['play_count'] < thresholds['play_count_min']].index.tolist()
    }
    
    return problems

def analyze_level_balance(courses_df, interactions_df):
    """Analyze level balance and identify potential design issues"""
    balance_metrics = pd.DataFrame()
    
    # Calculate balance metrics
    balance_metrics['completion_time_variance'] = interactions_df.groupby('id')['time'].agg('std')
    balance_metrics['clear_rate'] = interactions_df.groupby('id').agg({
        'clears': 'sum',
        'plays': 'sum'
    }).apply(lambda x: x['clears'] / x['plays'], axis=1)
    
    # Identify balance issues
    balance_issues = {
        'high_variance': balance_metrics[balance_metrics['completion_time_variance'] > 
                                       balance_metrics['completion_time_variance'].quantile(0.95)].index.tolist(),
        'very_low_clear_rate': balance_metrics[balance_metrics['clear_rate'] < 0.01].index.tolist(),
        'very_high_clear_rate': balance_metrics[balance_metrics['clear_rate'] > 0.99].index.tolist()
    }
    
    return balance_issues