from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def create_level_features(course_df, interactions_df):
    """Create feature matrix for level recommendations"""
    features = pd.DataFrame()
    
    # Normalize interaction metrics
    for metric in ['plays', 'clears', 'likes']:
        features[metric] = interactions_df[metric] / interactions_df[metric].max()
    
    # Add course features
    features['difficulty'] = pd.Categorical(course_df['difficulty']).codes / 4  # Normalize to 0-1
    features['gameStyle'] = pd.Categorical(course_df['gameStyle']).codes / len(course_df['gameStyle'].unique())
    
    return features

def find_similar_levels(level_id, features_df, n_recommendations=5):
    """Find similar levels based on features"""
    similarities = cosine_similarity(features_df)
    level_idx = features_df.index.get_loc(level_id)
    
    # Get similar levels indices
    similar_indices = similarities[level_idx].argsort()[::-1][1:n_recommendations+1]
    
    return features_df.index[similar_indices].tolist()