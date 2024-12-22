import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from config import FONTSIZE, PALETTE_NAME, PALETTE_SIZE

def get_color_palette():
    """Return the color palette for visualizations"""
    return sns.color_palette(PALETTE_NAME, PALETTE_SIZE)

def func(pct, allvals):
    """Format function for pie chart labels"""
    absolute = float(pct/100.*np.sum(allvals))/1000.0
    return "{:.1f}%\n({:.1f}k)".format(pct, absolute)

def create_pie_chart(values, labels, title=None):
    """Create a pie chart with a white center circle"""
    palette = get_color_palette()
    explode = [0.03] * len(values)
    
    fig, ax = plt.subplots()
    ax.pie(values, autopct=lambda pct: func(pct, values), 
           pctdistance=0.45, colors=palette, 
           explode=explode, labels=labels,
           textprops={'fontsize':FONTSIZE,'weight':'bold'})
    
    centre_circle = plt.Circle((0,0), 0.75, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    return fig, ax