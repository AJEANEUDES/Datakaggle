import streamlit as st
from data_loader import load_datasets, prepare_interactions
from visualization_utils import create_pie_chart
from analysis.player_analysis import analyze_player_statistics, calculate_player_engagement
from analysis.course_analysis import analyze_course_difficulty, find_popular_course_patterns
from visualization.player_charts import plot_player_distribution_by_country, plot_player_engagement_histogram
from visualization.course_charts import plot_difficulty_success_rate, plot_style_popularity
import pandas as pd

def main():
    st.title("Analyse de Données de Performance dans les Jeux Vidéos")
    
    # Load data
    with st.spinner('Chargement des données...'):
        try:
            datasets = load_datasets()
            interactions = prepare_interactions(datasets)
            df_interactions = pd.DataFrame(interactions).transpose()
            df_interactions['sum'] = df_interactions.sum(axis=1)
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")
            return
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choisir une page",
        ["Vue d'ensemble", 
         "Analyse des Joueurs",
         "Analyse des Niveaux",
         "Statistiques d'Engagement",
         "Tendances et Patterns"]
    )
    
    if page == "Vue d'ensemble":
        st.header("Vue d'ensemble des données")
        for name, df in datasets.items():
            st.subheader(f"Dataset: {name}")
            st.write(f"Nombre d'enregistrements: {len(df)}")
            st.dataframe(df.head())
    
    elif page == "Analyse des Joueurs":
        st.header("Analyse des Joueurs")
        
        if 'players' not in datasets:
            st.warning("Les données des joueurs ne sont pas disponibles. Vérifiez que le fichier players.xls existe dans le dossier data/")
            return
            
        try:
            # Player statistics
            player_stats = analyze_player_statistics(datasets['players'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Nombre total de joueurs", player_stats['total_players'])
                # st.metric("Moyenne de niveaux par joueur", f"{player_stats['avg_courses_per_player']:.2f}")
            
            st.subheader("Distribution des Joueurs par Pays")
            fig = plot_player_distribution_by_country(player_stats['players_by_country'])
            st.pyplot(fig)
            
            st.subheader("Top Créateurs")
            st.dataframe(player_stats['top_creators'])
        except Exception as e:
            st.error(f"Erreur lors de l'analyse des données des joueurs: {str(e)}")
    
    elif page == "Analyse des Niveaux":
        st.header("Analyse des Niveaux")
        
        if 'courses' not in datasets:
            st.warning("Les données des niveaux ne sont pas disponibles. Vérifiez que le fichier courses.csv existe dans le dossier data/")
            return
            
        try:
            # Course analysis
            course_stats = analyze_course_difficulty(datasets['courses'])
            patterns = find_popular_course_patterns(datasets['courses'], df_interactions)
            
            st.subheader("Distribution des Difficultés")
            fig = create_pie_chart(
                list(course_stats['difficulty_distribution'].values()),
                list(course_stats['difficulty_distribution'].keys()),
                "Distribution des Difficultés"
            )
            st.pyplot(fig[0])
            
            st.subheader("Popularité par Style de Jeu")
            fig = plot_style_popularity(patterns['style_engagement'])
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erreur lors de l'analyse des niveaux: {str(e)}")
    
    elif page == "Statistiques d'Engagement":
        st.header("Statistiques d'Engagement")
        
        try:
            engagement_stats = calculate_player_engagement(
                datasets.get('players', pd.DataFrame()), 
                df_interactions
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Moyenne d'interactions par niveau", 
                         f"{engagement_stats['avg_interactions_per_course']:.2f}")
            with col2:
                st.metric("Médiane des interactions", 
                         f"{engagement_stats['median_interactions']:.2f}")
            with col3:
                st.metric("Total des interactions", 
                         f"{engagement_stats['total_interactions']:,}")
            
            st.subheader("Distribution de l'Engagement")
            fig = plot_player_engagement_histogram(df_interactions)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erreur lors de l'analyse de l'engagement: {str(e)}")
    
    elif page == "Tendances et Patterns":
        st.header("Tendances et Patterns")
        
        try:
            patterns = find_popular_course_patterns(datasets['courses'], df_interactions)
            
            st.subheader("Taux de Réussite par Niveau de Difficulté")
            fig = plot_difficulty_success_rate(patterns['difficulty_success_rate'])
            st.pyplot(fig)
            
            st.subheader("Popularité des Styles de Jeu")
            st.write("Moyenne des likes par style de jeu:")
            st.bar_chart(patterns['popular_styles'])
        except Exception as e:
            st.error(f"Erreur lors de l'analyse des tendances: {str(e)}")

if __name__ == "__main__":
    main()