import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

from data_loader import load_datasets, prepare_interactions
from visualization_utils import create_pie_chart, get_color_palette
from statistical_analysis import fit_power_law, test_distributions
import matplotlib.pyplot as plt
import pandas as pd

def main():
    # Load data
    datasets = load_datasets()
    interactions = prepare_interactions(datasets)
    
    # Basic analysis of difficulty distribution
    difficulty_labels = datasets['courses']['difficulty'].unique().tolist()
    difficulty_values = [sum(datasets['courses']['difficulty'] == label) for label in difficulty_labels]
    fig, ax = create_pie_chart(difficulty_values, difficulty_labels, "Difficulty Distribution")
    plt.show()
    
    # Create interaction analysis DataFrame
    df_interactions = pd.DataFrame(interactions).transpose()
    df_interactions['sum'] = df_interactions.sum(axis=1)
    df_interactions = df_interactions.sort_values(by=['sum'], ascending=False)
    
    # Perform statistical analysis
    power_law_fit = fit_power_law(df_interactions['sum'])
    distribution_tests = test_distributions(df_interactions['sum'])
    
    # Display results
    print("\nTop 10 most interactive levels:")
    print(df_interactions.head(10))
    
    print("\nDistribution test results:")
    for result in distribution_tests:
        print(f"Distribution: {result['distribution']}")
        print(f"p-value: {result['p_value']:.6f}")
        print(f"D-statistic: {result['D_statistic']:.6f}")
        print("-" * 50)

if __name__ == "__main__":
    main()