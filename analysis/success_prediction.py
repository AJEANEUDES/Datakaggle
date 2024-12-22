from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd


def prepare_success_features(course_df, interactions_df):
    """Prepare features for success rate prediction"""
    features = pd.DataFrame()
    
    # Course characteristics
    features['difficulty_code'] = pd.Categorical(course_df['difficulty']).codes
    features['style_code'] = pd.Categorical(course_df['gameStyle']).codes
    
    # Interaction metrics
    features['play_count'] = interactions_df['plays']
    features['like_ratio'] = interactions_df['likes'] / interactions_df['plays']
    
    return features

def predict_success_rate(features, clear_rates, test_size=0.2):
    """Train and evaluate success rate prediction model"""
    X_train, X_test, y_train, y_test = train_test_split(
        features, clear_rates, test_size=test_size, random_state=42
    )
    
    model = GradientBoostingClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    return {
        'model': model,
        'accuracy': model.score(X_test, y_test),
        'feature_importance': dict(zip(features.columns, model.feature_importances_))
    }