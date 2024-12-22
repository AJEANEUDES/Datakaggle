"""
Data loading and preparation utilities
"""

import pandas as pd
import os
import glob
from pathlib import Path
from config import DATA_DIR, DATA_FILES

def clean_column_names(df):
    """Clean column names by removing whitespace and special characters"""
    df.columns = df.columns.str.strip().str.split('\t').str[0]
    return df

# def load_split_files(file_info):
#     """Load and combine split files"""
#     base_name = Path(file_info['name']).stem.replace('*', '')
#     format_ext = '.' + file_info['format']
#     pattern = os.path.join(DATA_DIR, 'split', f'{base_name}*{format_ext}')
    
#     # Use glob to find all matching files
#     matching_files = glob.glob(pattern)
#     if not matching_files:
#         print(f"No matching files found for pattern: {pattern}")
#         return None
    
#     dfs = []
#     for file_path in matching_files:
#         try:
#             if format_ext.lower() in ['.xlsx', '.xls', '.xlsb']:
#                 df = pd.read_excel(file_path)
#             else:
#                 df = pd.read_csv(file_path)
#             dfs.append(df)
#         except Exception as e:
#             print(f"Error loading {file_path}: {str(e)}")
#             continue
    
#     return pd.concat(dfs, ignore_index=True) if dfs else None

def load_split_files(file_info):
    """Charger et combiner les fichiers divisés"""
    base_name = Path(file_info['name']).stem.replace('*', '')
    format_ext = '.' + file_info['format']
    pattern = os.path.join(DATA_DIR, 'split', f'{base_name}*{format_ext}')
    
    # Utiliser glob pour trouver tous les fichiers correspondants
    matching_files = glob.glob(pattern)
    if not matching_files:
        print(f"Aucun fichier trouvé pour le modèle : {pattern}")
        return None
    
    dfs = []
    for file_path in matching_files:
        try:
            df = pd.read_csv(file_path, sep='\t', encoding='utf-8')  # Ajustez le séparateur si nécessaire
            if 'id' not in df.columns:
                print(f"Avertissement : La colonne 'id' est manquante dans le fichier {file_path}")
                continue
            dfs.append(df)
        except Exception as e:
            print(f"Erreur de chargement de {file_path}: {str(e)}")
            continue
    
    if dfs:
        # Vérification de la présence de la colonne 'id' dans tous les DataFrames avant concaténation
        for i, df in enumerate(dfs):
            if 'id' not in df.columns:
                print(f"Avertissement : 'id' manquant dans le fichier {matching_files[i]}")
        return pd.concat(dfs, ignore_index=True)  # Fusionner les fichiers en un seul DataFrame
    else:
        print(f"Aucun fichier valide à fusionner pour {pattern}")
        return None


def load_file(file_info):
    """Load a single file or its split parts"""
    try:
        # Check if this is a split file
        if file_info.get('split', False):
            return load_split_files(file_info)
        
        # Regular file loading
        file_path = os.path.join(DATA_DIR, file_info['name'])
        if file_info['format'] == 'excel':
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
        return clean_column_names(df)
    except Exception as e:
        print(f"Error loading {file_info['name']}: {str(e)}")
        return None

def load_datasets():
    """Load all datasets from the data directory"""
    datasets = {}
    
    for key, file_info in DATA_FILES.items():
        df = load_file(file_info)
        if df is not None:
            datasets[key] = df
            print(f"Successfully loaded {key} dataset")
    
    return datasets

# def prepare_interactions(datasets):
#     """Prepare interaction data for analysis"""
#     required_datasets = ['courses', 'likes', 'plays', 'clears', 'records']
#     missing_datasets = [ds for ds in required_datasets if ds not in datasets]
    
#     if missing_datasets:
#         raise ValueError(f"Missing required datasets: {', '.join(missing_datasets)}")
    
#     # Get course IDs
#     ids = datasets['courses']['id'].unique().tolist()
    
#     # Initialize interaction dictionary
#     interactions = {id: {'likes': 0, 'plays': 0, 'clears': 0, 'records': 0} for id in ids}
    
#     # Count interactions for each type
#     for interaction_type in ['likes', 'plays', 'clears', 'records']:
#         try:
#             df = datasets[interaction_type]
#             counts = df['id'].value_counts().to_dict()
#             for id, count in counts.items():
#                 if id in interactions:
#                     interactions[id][interaction_type] = count
#         except KeyError as e:
#             print(f"Warning: Could not process {interaction_type} data - {str(e)}")
#             continue
                
#     return interactions

def prepare_interactions(datasets):
    """Préparer les données d'interaction pour l'analyse"""
    required_datasets = ['courses', 'likes', 'plays', 'clears', 'records']
    missing_datasets = [ds for ds in required_datasets if ds not in datasets]
    
    if missing_datasets:
        raise ValueError(f"Jeux de données manquants : {', '.join(missing_datasets)}")
    
    # Obtenir les ID des cours
    ids = datasets['courses']['id'].unique().tolist()
    
    # Initialiser le dictionnaire des interactions
    interactions = {id: {'likes': 0, 'plays': 0, 'clears': 0, 'records': 0} for id in ids}
    
    # Compter les interactions pour chaque type
    for interaction_type in ['likes', 'plays', 'clears', 'records']:
        try:
            df = datasets[interaction_type]
            if 'id' not in df.columns:
                print(f"Avertissement : Colonne 'id' manquante dans les données {interaction_type}")
                continue
            counts = df['id'].value_counts().to_dict()
            for id, count in counts.items():
                if id in interactions:
                    interactions[id][interaction_type] = count
        except KeyError as e:
            print(f"Avertissement : Impossible de traiter les données {interaction_type} - {str(e)}")
            continue
                
    return interactions
