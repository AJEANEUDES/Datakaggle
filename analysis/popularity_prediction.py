import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


def prepare_features(course_df, interactions_df):
    """Prepare features for popularity prediction"""
    features = pd.DataFrame()
    features['difficulty'] = pd.Categorical(course_df['difficulty']).codes
    features['gameStyle'] = pd.Categorical(course_df['gameStyle']).codes
    
    # Add interaction-based features
    features['clear_rate'] = interactions_df['clears'] / interactions_df['plays']
    features['like_rate'] = interactions_df['likes'] / interactions_df['plays']
    
    return features

def train_popularity_model(features, target='plays'):
    """Train a model to predict course popularity"""
    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    y = target
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, scaler

def predict_popularity(model, scaler, new_features):
    """Predict popularity for new courses"""
    X_new = scaler.transform(new_features)
    predictions = model.predict(X_new)
    return predictions