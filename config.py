"""
Configuration settings for the application
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Visualization settings
FONTSIZE = 14
PALETTE_NAME = 'cubehelix'
PALETTE_SIZE = 4

# Data files configuration with format specification
DATA_FILES = {
    'courses': {'name': 'courses.csv', 'format': 'csv'},
    'likes': {'name': 'likes.csv', 'format': 'csv'},
    'plays': {'name': 'plays_part*.csv', 'format': 'csv', 'split': True},  # Indique un fichier divisé
    'clears': {'name': 'clears_part*.csv', 'format': 'csv', 'split': True},  # Indique un fichier divisé
    'records': {'name': 'records.csv', 'format': 'csv'},
    'players': {'name': 'players.csv', 'format': 'csv'}
}