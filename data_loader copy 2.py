"""
Data loading and preparation utilities
"""

import pandas as pd
import os
from config import DATA_DIR, DATA_FILES

# Column name mappings for different files
COLUMN_MAPPINGS = {
    'id': ['id', 'course_id', 'courseId', 'ID', 'Id'],
    'likes': ['likes', 'like_count', 'likeCount', 'Likes'],
    'plays': ['plays', 'play_count', 'playCount', 'Plays'],
    'clears': ['clears', 'clear_count', 'clearCount', 'Clears'],
    'records': ['records', 'record_count', 'recordCount', 'Records']
}

def get_column_name(df, column_type):
    """Find the actual column name in the dataframe"""
    possible_names = COLUMN_MAPPINGS.get(column_type, [])
    for name in possible_names:
        if name in df.columns:
            return name
    raise KeyError(f"No matching column found for {column_type}. Available columns: {', '.join(df.columns)}")

def load_file(file_path, file_format):
    """Load a single file based on its format"""
    try:
        if file_format == 'csv':
            return pd.read_csv(file_path, sep='\t', encoding='utf-8')
        elif file_format == 'excel':
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def load_datasets():
    """Load all datasets from the data directory"""
    datasets = {}
    
    for key, file_info in DATA_FILES.items():
        file_path = os.path.join(DATA_DIR, file_info['name'])
        df = load_file(file_path, file_info['format'])
        if df is not None:
            datasets[key] = df
            
    return datasets

def prepare_interactions(datasets):
    """Prepare interaction data for analysis"""
    if not all(key in datasets for key in ['courses', 'likes', 'plays', 'clears', 'records']):
        raise ValueError("Missing required datasets for interaction analysis")
    
    # Get course IDs using the correct column name
    course_id_col = get_column_name(datasets['courses'], 'id')
    ids = datasets['courses'][course_id_col].unique().tolist()
    
    # Initialize interaction dictionary
    interactions = {id: {'likes': 0, 'plays': 0, 'clears': 0, 'records': 0} for id in ids}
    
    # Count interactions for each type
    for interaction_type in ['likes', 'plays', 'clears', 'records']:
        try:
            df = datasets[interaction_type]
            id_col = get_column_name(df, 'id')
            counts = df[id_col].value_counts().to_dict()
            for id, count in counts.items():
                if id in interactions:
                    interactions[id][interaction_type] = count
        except KeyError as e:
            print(f"Warning: Could not process {interaction_type} data - {str(e)}")
            continue
                
    return interactions