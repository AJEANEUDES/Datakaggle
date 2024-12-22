import pandas as pd
import numpy as np
from collections import defaultdict

def analyze_creator_patterns(courses_df):
    """Analyze patterns in level creation"""
    creator_patterns = defaultdict(lambda: defaultdict(int))
    
    for _, course in courses_df.iterrows():
        creator_patterns[course['maker']]['difficulty_preference'][course['difficulty']] += 1
        creator_patterns[course['maker']]['style_preference'][course['gameStyle']] += 1
    
    # Convert to regular dict for serialization
    return {maker: dict(patterns) for maker, patterns in creator_patterns.items()}

def identify_creator_evolution(courses_df):
    """Analyze how creators evolve over time"""
    courses_df = courses_df.sort_values('upload_date')
    creator_evolution = {}
    
    for maker in courses_df['maker'].unique():
        maker_courses = courses_df[courses_df['maker'] == maker]
        
        evolution = {
            'difficulty_progression': maker_courses.groupby('upload_date')['difficulty'].mean(),
            'style_changes': maker_courses.groupby('upload_date')['gameStyle'].value_counts(),
            'creation_frequency': maker_courses.groupby('upload_date').size()
        }
        
        creator_evolution[maker] = evolution
    
    return creator_evolution