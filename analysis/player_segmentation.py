from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

def create_player_profiles(players_df, interactions_df):
    """Create player profiles based on their behavior"""
    profiles = pd.DataFrame()
    
    # Aggregate interactions by player
    player_stats = interactions_df.groupby('player').agg({
        'plays': 'sum',
        'clears': 'sum',
        'likes': 'sum'
    })
    
    # Calculate derived metrics
    profiles['clear_rate'] = player_stats['clears'] / player_stats['plays']
    profiles['like_rate'] = player_stats['likes'] / player_stats['plays']
    profiles['activity_level'] = player_stats['plays']
    
    return profiles

def segment_players(profiles, n_segments=4):
    """Segment players using clustering"""
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(profiles)
    
    kmeans = KMeans(n_clusters=n_segments, random_state=42)
    segments = kmeans.fit_predict(scaled_features)
    
    # Analyze segment characteristics
    segment_profiles = {}
    for i in range(n_segments):
        segment_data = profiles[segments == i]
        segment_profiles[f'segment_{i}'] = {
            'size': len(segment_data),
            'avg_clear_rate': segment_data['clear_rate'].mean(),
            'avg_like_rate': segment_data['like_rate'].mean(),
            'avg_activity': segment_data['activity_level'].mean()
        }
    
    return segment_profiles