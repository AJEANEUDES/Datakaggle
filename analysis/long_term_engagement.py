import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def analyze_player_retention(plays_df, window_days=30):
    """Analyze player retention over time"""
    plays_df['date'] = pd.to_datetime(plays_df['timestamp']).dt.date
    
    retention_data = {}
    for player in plays_df['player'].unique():
        player_plays = plays_df[plays_df['player'] == player]
        first_play = player_plays['date'].min()
        last_play = player_plays['date'].max()
        days_active = (last_play - first_play).days
        play_frequency = len(player_plays) / max(days_active, 1)
        
        retention_data[player] = {
            'days_active': days_active,
            'play_frequency': play_frequency,
            'total_plays': len(player_plays)
        }
    
    return pd.DataFrame(retention_data).T

def predict_future_engagement(player_history, features=['play_frequency', 'total_plays']):
    """Predict future player engagement based on historical data"""
    X = player_history[features]
    y = player_history['days_active']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return {
        'model': model,
        'feature_importance': dict(zip(features, model.feature_importances_))
    }