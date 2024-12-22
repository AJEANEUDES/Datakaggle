import pandas as pd
import numpy as np

def analyze_player_statistics(players_df):
    """Analyze player statistics and return insights"""
    stats = {
        'total_players': len(players_df),
        'players_by_country': players_df['flag'].value_counts().to_dict(),
        'avg_courses_per_player': players_df['maps'].mean() if 'maps' in players_df.columns else players_df['courses'].mean() if 'courses' in players_df.columns else 0,
        'top_creators': players_df.nlargest(10, 'maps' if 'maps' in players_df.columns else 'courses')[['name', 'maps' if 'maps' in players_df.columns else 'courses', 'flag']],
    }
    return stats

def calculate_player_engagement(players_df, interactions_df):
    """Calculate player engagement metrics"""
    engagement = {
        'avg_interactions_per_course': interactions_df['sum'].mean(),
        'median_interactions': interactions_df['sum'].median(),
        'total_interactions': interactions_df['sum'].sum(),
    }
    return engagement