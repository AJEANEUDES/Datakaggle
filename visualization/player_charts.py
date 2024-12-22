import matplotlib.pyplot as plt
import seaborn as sns
from visualization_utils import get_color_palette

# def plot_player_distribution_by_country(players_by_country, title="Players Distribution by Country"):
#     """Create a bar chart of player distribution by country"""
#     plt.figure(figsize=(12, 6))
#     palette = get_color_palette()
    
#     countries = list(players_by_country.keys())
#     values = list(players_by_country.values())
    
#     plt.bar(countries, values, color=palette[0])
#     plt.title(title)
#     plt.xticks(rotation=45)
#     plt.xlabel("Country")
#     plt.ylabel("Number of Players")
    
#     return plt.gcf()

def plot_player_distribution_by_country(players_by_country, title="Players Distribution by Country"):
    """Create a bar chart of player distribution by country"""
    plt.figure(figsize=(18, 10))  # Augmenter la taille du graphique
    palette = get_color_palette()
    
    # Trier les pays par nombre de joueurs (valeurs décroissantes)
    sorted_data = sorted(players_by_country.items(), key=lambda x: x[1], reverse=True)
    countries, values = zip(*sorted_data[:20])  # Limiter à 20 pays
    
    plt.bar(countries, values, color=palette[0])
    plt.title(title)
    plt.xticks(rotation=90)  # Rotation plus forte pour éviter les chevauchements
    plt.xlabel("Country")
    plt.ylabel("Number of Players")
    plt.tight_layout()  # Ajuster les marges pour éviter les coupures
    
    return plt.gcf()


def plot_player_engagement_histogram(interactions_df, title="Player Engagement Distribution"):
    """Create a histogram of player engagement"""
    plt.figure(figsize=(18, 10))
    palette = get_color_palette()
    
    plt.hist(interactions_df['sum'], bins=50, color=palette[0], alpha=0.7)
    plt.title(title)
    plt.xlabel("Number of Interactions")
    plt.ylabel("Frequency")
    
    return plt.gcf()