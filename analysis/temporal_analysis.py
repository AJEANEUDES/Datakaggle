import pandas as pd
import numpy as np
from datetime import datetime

def analyze_time_patterns(plays_df):
    """Analyze temporal patterns in gameplay data"""
    # Convert timestamp to datetime
    plays_df['datetime'] = pd.to_datetime(plays_df['timestamp'])
    
    patterns = {
        'hourly_distribution': plays_df['datetime'].dt.hour.value_counts().sort_index().to_dict(),
        'daily_distribution': plays_df['datetime'].dt.dayofweek.value_counts().sort_index().to_dict(),
        'monthly_distribution': plays_df['datetime'].dt.month.value_counts().sort_index().to_dict()
    }
    return patterns

def calculate_engagement_trends(plays_df, window='7D'):
    """Calculate engagement trends over time"""
    plays_df['datetime'] = pd.to_datetime(plays_df['timestamp'])
    daily_plays = plays_df.set_index('datetime').resample(window).size()
    
    trends = {
        'trend_values': daily_plays.to_dict(),
        'average_daily_plays': daily_plays.mean(),
        'peak_play_date': daily_plays.idxmax(),
        'peak_play_count': daily_plays.max()
    }
    return trends