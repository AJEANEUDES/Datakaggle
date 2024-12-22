import matplotlib.pyplot as plt
import seaborn as sns
from visualization_utils import get_color_palette

def plot_difficulty_success_rate(difficulty_success_rate, title="Success Rate by Difficulty"):
    """Create a bar chart of success rates by difficulty"""
    plt.figure(figsize=(10, 6))
    palette = get_color_palette()
    
    difficulties = list(difficulty_success_rate.keys())
    rates = list(difficulty_success_rate.values())
    
    plt.bar(difficulties, rates, color=palette[0])
    plt.title(title)
    plt.xlabel("Difficulty Level")
    plt.ylabel("Average Clear Rate")
    
    return plt.gcf()

def plot_style_popularity(style_engagement, title="Game Style Popularity"):
    """Create a horizontal bar chart of game style popularity"""
    plt.figure(figsize=(12, 6))
    palette = get_color_palette()
    
    styles = list(style_engagement.keys())
    engagement = list(style_engagement.values())
    
    plt.barh(styles, engagement, color=palette[0])
    plt.title(title)
    plt.xlabel("Average Likes")
    plt.ylabel("Game Style")
    
    return plt.gcf()