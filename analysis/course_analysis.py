import pandas as pd
import numpy as np

def map_difficulty_to_numeric(difficulty):
    """Map difficulty strings to numeric values"""
    difficulty_map = {
        'easy': 1,
        'normal': 2,
        'expert': 3,
        'superExpert': 4
    }
    return difficulty_map.get(difficulty.lower(), 0)

def analyze_course_difficulty(courses_df):
    """Analyze course difficulty distribution and patterns"""
    # Create difficulty distribution without numeric conversion
    difficulty_stats = {
        'difficulty_distribution': courses_df['difficulty'].value_counts().to_dict(),
    }
    
    # Create a numeric difficulty column for calculations
    numeric_difficulty = courses_df['difficulty'].apply(map_difficulty_to_numeric)
    
    # Add numeric-based calculations
    difficulty_stats.update({
        'avg_difficulty': numeric_difficulty.mean(),
        'difficulty_by_style': courses_df.groupby('gameStyle').apply(
            lambda x: x['difficulty'].apply(map_difficulty_to_numeric).mean()
        ).to_dict(),
    })
    
    return difficulty_stats

def find_popular_course_patterns(courses_df, interactions_df):
    """Identify patterns in popular courses"""
    # Merge course data with interaction data
    merged_df = courses_df.merge(interactions_df, left_on='id', right_index=True)
    
    patterns = {
        'popular_styles': merged_df.groupby('gameStyle')['sum'].mean().sort_values(ascending=False).to_dict(),
        'difficulty_success_rate': merged_df.groupby('difficulty')['clears'].mean().to_dict(),
        'style_engagement': merged_df.groupby('gameStyle')['likes'].mean().sort_values(ascending=False).to_dict(),
    }
    return patterns