import matplotlib.pyplot as plt
import seaborn as sns
from visualization_utils import get_color_palette

def plot_hourly_distribution(hourly_dist, title="Hourly Play Distribution"):
    """Plot hourly distribution of gameplay"""
    plt.figure(figsize=(12, 6))
    palette = get_color_palette()
    
    hours = list(range(24))
    values = [hourly_dist.get(hour, 0) for hour in hours]
    
    plt.bar(hours, values, color=palette[0])
    plt.title(title)
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Plays")
    plt.xticks(hours)
    
    return plt.gcf()

def plot_engagement_trend(trend_values, title="Engagement Trend Over Time"):
    """Plot engagement trends over time"""
    plt.figure(figsize=(15, 6))
    palette = get_color_palette()
    
    dates = list(trend_values.keys())
    values = list(trend_values.values())
    
    plt.plot(dates, values, color=palette[0])
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Number of Plays")
    plt.xticks(rotation=45)
    
    return plt.gcf()