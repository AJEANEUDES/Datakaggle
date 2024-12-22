import pandas as pd
import numpy as np

def get_course_column_name(df):
    """Helper function to determine the correct column name for courses/maps"""
    # Afficher les colonnes disponibles
    print("Colonnes disponibles :", df.columns.tolist())
    
    column_variants = ['courses', 'maps', 'levels', 'course', 'map', 'level', 
                      'courses_created', 'maps_created', 'levels_created']
    
    for col in df.columns:
        if col.lower() in [variant.lower() for variant in column_variants]:
            # Vérifier si la colonne est numérique
            if pd.api.types.is_numeric_dtype(df[col]):
                return col
            else:
                print(f"Colonne {col} trouvée mais non numérique.")
    return None




# def analyze_player_statistics(players_df):
#     """Analyze player statistics and return insights"""
#     # Validation de base
#     if not isinstance(players_df, pd.DataFrame):
#         raise ValueError("Input must be a pandas DataFrame")
    
#     if players_df.empty:
#         raise ValueError("DataFrame is empty")
    
#     # Vérifier les colonnes disponibles
#     print("Colonnes disponibles :", players_df.columns.tolist())
    
#     # Trouver la colonne des niveaux
#     course_column = get_course_column_name(players_df)
#     print(f"Colonne identifiée pour les niveaux/courses : {course_column}")
    
#     stats = {
#         'total_players': len(players_df),
#         'players_by_country': players_df['flag'].value_counts().to_dict() if 'flag' in players_df.columns else {},
#     }
    
#     if course_column:
#         print(players_df[course_column].describe())  # Ajouter un résumé statistique pour debug
#         stats.update({
#             'avg_courses_per_player': players_df[course_column].mean(),
#             'top_creators': players_df.nlargest(10, course_column)[[col for col in ['name', course_column, 'flag'] if col in players_df.columns]],
#         })
#     else:
#         stats.update({
#             'avg_courses_per_player': 0,
#             'top_creators': pd.DataFrame(),
#         })
#         print("Aucune colonne valide pour les niveaux n'a été trouvée.")
    
#     return stats

def analyze_player_statistics(players_df):
    """Analyze player statistics and return insights"""
    # Validation de base
    if not isinstance(players_df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    if players_df.empty:
        raise ValueError("DataFrame is empty")
    
    # Vérifier les colonnes disponibles
    print("Colonnes disponibles :", players_df.columns.tolist())
    
    # Trouver la colonne des niveaux/courses
    course_column = get_course_column_name(players_df)
    print(f"Colonne identifiée pour les niveaux/courses : {course_column}")
    
    if course_column:
        # Vérifiez si la colonne contient des valeurs valides
        print(players_df[course_column].describe())  # Résumé statistique
        print(players_df[course_column].head(10))   # Exemple de valeurs
        
        # Vérifiez les valeurs nulles
        if players_df[course_column].isnull().all():
            print(f"Toutes les valeurs de la colonne '{course_column}' sont nulles.")
        elif (players_df[course_column] <= 0).all():
            print(f"Toutes les valeurs de la colonne '{course_column}' sont inférieures ou égales à zéro.")
    else:
        print("Aucune colonne valide pour les niveaux n'a été trouvée.")
    
    stats = {
        'total_players': len(players_df),
        'players_by_country': players_df['flag'].value_counts().to_dict() if 'flag' in players_df.columns else {},
    }
    
    # Si la colonne est valide, calculez les statistiques des créateurs
    if course_column:
        stats.update({
            'avg_courses_per_player': players_df[course_column].mean(),
            'top_creators': players_df.nlargest(10, course_column)[[col for col in ['name', course_column, 'flag'] if col in players_df.columns]],
        })
    else:
        stats.update({
            'avg_courses_per_player': 0,
            'top_creators': pd.DataFrame(),
        })
        print("Warning: No valid column for levels/courses found.")
    
    return stats


def calculate_player_engagement(players_df, interactions_df):
    """Calculate player engagement metrics"""
    if not isinstance(interactions_df, pd.DataFrame) or interactions_df.empty:
        return {
            'avg_interactions_per_course': 0,
            'median_interactions': 0,
            'total_interactions': 0,
        }
    
    engagement = {
        'avg_interactions_per_course': interactions_df['sum'].mean() if 'sum' in interactions_df.columns else 0,
        'median_interactions': interactions_df['sum'].median() if 'sum' in interactions_df.columns else 0,
        'total_interactions': interactions_df['sum'].sum() if 'sum' in interactions_df.columns else 0,
    }
    return engagement