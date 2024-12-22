import matplotlib.pyplot as plt
import seaborn as sns
from visualization_utils import get_color_palette
import numpy as np



def plot_feature_importance(model, feature_names, title="Feature Importance"):
    """Plot feature importance from the prediction model"""
    plt.figure(figsize=(10, 6))
    palette = get_color_palette()
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.bar(range(len(importances)), importances[indices], color=palette[0])
    plt.title(title)
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
    plt.xlabel("Features")
    plt.ylabel("Importance")
    
    return plt.gcf()

def plot_prediction_accuracy(actual, predicted, title="Prediction Accuracy"):
    """Plot actual vs predicted values"""
    plt.figure(figsize=(10, 10))
    palette = get_color_palette()
    
    plt.scatter(actual, predicted, color=palette[0], alpha=0.5)
    plt.plot([min(actual), max(actual)], [min(actual), max(actual)], '--', color=palette[1])
    plt.title(title)
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    
    return plt.gcf()