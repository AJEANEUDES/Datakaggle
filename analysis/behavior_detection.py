import pandas as pd
import numpy as np
from scipy import stats

def detect_unusual_patterns(interactions_df, z_score_threshold=2):
    """Detect unusual patterns in player behavior"""
    metrics = ['plays', 'clears', 'likes', 'records']
    unusual_patterns = {}
    
    for metric in metrics:
        z_scores = np.abs(stats.zscore(interactions_df[metric]))
        unusual_patterns[metric] = interactions_df[z_scores > z_score_threshold].index.tolist()
    
    return unusual_patterns

def analyze_player_consistency(plays_df):
    """Analyze consistency in player behavior"""
    player_stats = plays_df.groupby('player').agg({
        'clear_time': ['mean', 'std', 'count'],
        'attempts': ['mean', 'std']
    })
    
    consistency_metrics = {
        'time_consistency': 1 - (player_stats['clear_time']['std'] / player_stats['clear_time']['mean']),
        'attempt_consistency': 1 - (player_stats['attempts']['std'] / player_stats['attempts']['mean'])
    }
    
    return consistency_metrics