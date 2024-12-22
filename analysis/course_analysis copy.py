import pandas as pd
import numpy as np

def analyze_course_difficulty(courses_df):
    """Analyze course difficulty distribution and patterns"""
    difficulty_stats = {
        'difficulty_distribution': courses_df['difficulty'].value_counts().to_dict(),
        'avg_difficulty': courses_df['difficulty'].mean(),
        'difficulty_by_style': courses_df.groupby('gameStyle')['difficulty'].mean().to_dict(),
    }
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