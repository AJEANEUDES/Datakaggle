import os
# Import des bibliothèques nécessaires pour la manipulation et l'analyse des données
import numpy as np
import pandas as pd

# Utilisé pour analyser les distributions de lois de puissance
from scipy import stats  # Fonctions statistiques de SciPy
import warnings  # Gère les avertissements de Python
warnings.simplefilter(action='ignore', category=RuntimeWarning)  
# Ignore les avertissements liés aux erreurs d'exécution

# Import des bibliothèques pour la visualisation des données
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import powerlaw

# %matplotlib 

# 1. Préparation des données

# Définit les chemins vers le dossier contenant les datasets et celui où les graphiques seront sauvegardés
dataset_folder = 'c:/Users/jcpro/OneDrive/Documents/Ma maitrise//analyse de donnees/superMario/1.Donnees de performance des joueurs/kaggle'
plot_folder = '/plot/'

# Chargement des différents fichiers CSV du dataset
courses = pd.read_csv(os.path.join(dataset_folder, 'courses.csv'), sep='\t', encoding='utf-8')
likes   = pd.read_csv(os.path.join(dataset_folder, 'likes.csv'), sep='\t', encoding='utf-8')
plays   = pd.read_csv(os.path.join(dataset_folder, 'plays.csv'), sep='\t', encoding='utf-8')
clears  = pd.read_csv(os.path.join(dataset_folder, 'clears.csv'), sep='\t', encoding='utf-8')
records = pd.read_csv(os.path.join(dataset_folder, 'records.csv'), sep='\t', encoding='utf-8')
players = pd.read_csv(os.path.join(dataset_folder, 'players.csv'), sep='\t', encoding='utf-8')

# Création d'une liste unique des identifiants de niveaux de jeu à partir du fichier 'courses'
ids = courses['id'].unique().tolist()

# Initialisation d'un dictionnaire pour stocker les interactions (likes, plays, clears, records) pour chaque niveau de jeu
interactions = {id:{'likes':0, 'plays':0, 'clears':0, 'records':0} for id in ids}

# Affiche le nombre d'enregistrements pour chaque fichier de données chargé
names = ['courses','likes','plays','clears','records']
for df_tmp, name in zip([courses,likes,plays,clears,records], names):
    print('%s:' % (name), len(df_tmp))  # Affiche le nom du fichier et le nombre de lignes dans ce fichier

# Affiche les premières lignes du dataset 'likes' pour vérification
likes.head()


# Compte le nombre de likes par niveau et met à jour le dictionnaire d'interactions
likes_per_course = likes['id'].value_counts().to_dict()
for id, values in likes_per_course.items():
    interactions[id]['likes'] = values

# Affiche les premières lignes du dataset 'plays' pour vérification
plays.head()

# Compte le nombre de plays par niveau et met à jour le dictionnaire d'interactions
plays_per_course = plays['id'].value_counts().to_dict()
for id, values in plays_per_course.items():
    interactions[id]['plays'] = values

# Affiche les premières lignes du dataset 'clears' pour vérification
clears.head()

# Compte le nombre de clears par niveau et met à jour le dictionnaire d'interactions
clears_per_course = clears['id'].value_counts().to_dict()
for id, values in clears_per_course.items():
    interactions[id]['clears'] = values

# Affiche les premières lignes du dataset 'records' pour vérification
records.head()

# Compte le nombre de records par niveau et met à jour le dictionnaire d'interactions
records_per_course = records['id'].value_counts().to_dict()
for id, values in records_per_course.items():
    interactions[id]['records'] = values

# Création d'une palette de couleurs pour les graphiques
palette = sns.color_palette('cubehelix', 4)
sns.palplot(palette)

# Fonction pour afficher les pourcentages et valeurs absolues dans les graphiques en camembert
def func(pct, allvals):
    absolute = float(pct/100.*np.sum(allvals))/1000.0
    return "{:.1f}%\n({:.1f}k)".format(pct, absolute)

# Initialisation des paramètres de police pour les graphiques
fontsize = 14

# Génération d'un graphique en camembert pour la difficulté des niveaux
labels = courses['difficulty'].unique().tolist()
values = [sum(courses['difficulty'] == label) for label in labels]
print(list(zip(labels, values)))
explode = [0.03] * len(values)

fig, ax = plt.subplots()
ax.pie(values, autopct=lambda pct: func(pct, values), pctdistance=0.45,
       colors=palette, explode=explode, labels=labels,
       textprops={'fontsize':fontsize,'weight':'bold'})
centre_circle = plt.Circle((0,0),0.75,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
ax.axis('equal')
plt.tight_layout()
plt.show()

# Génération d'un graphique en camembert pour le style de jeu des niveaux
labels = courses['gameStyle'].unique().tolist()
values = [sum(courses['gameStyle'] == label) for label in labels]
print(list(zip(labels, values)))
explode = [0.03] * len(values)

fig, ax = plt.subplots()
ax.pie(values, autopct=lambda pct: func(pct, values), pctdistance=0.45,
       colors=palette, explode=explode, labels=labels,
       textprops={'fontsize':fontsize,'weight':'bold'})
centre_circle = plt.Circle((0,0),0.75,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
ax.axis('equal')
plt.tight_layout()
plt.show()

# Compte et affiche le nombre de créateurs (makers) de niveaux
makers = courses['maker'].value_counts().to_dict()
print('number of makers: %d' % (len(makers)))

# Affiche le nombre de niveaux créés par les 25 principaux créateurs
top = 25
labels = list(makers.keys())[0:top]
x_axis = range(len(labels))
y_axis = list(makers.values())[0:top]

fig, ax = plt.subplots()
plt.bar(x_axis, y_axis, align='center', color=palette[0])
plt.xticks(x_axis, labels, rotation=90)
plt.title('Number of maps per Maker')
plt.show()

# Mise en forme du dataset des joueurs pour analyses supplémentaires
players = players.set_index('id')
players.head()

df_tmp = pd.DataFrame(makers, index=['courses']).transpose()
df_tmp = df_tmp.rename(columns={'index':'id'})
df_tmp = pd.concat([df_tmp, players], sort=True, axis=1)
df_tmp = df_tmp.dropna(subset=['courses']).sort_values(by=['courses'], ascending=False)
df_tmp.head()

# Comptage du nombre de niveaux créés par pays
countries = {flag:0 for flag in df_tmp['flag'].unique().tolist()}
for maker, row in df_tmp.iterrows():
    countries[row['flag']] += int(row['courses'])

# Génération d'un graphique en camembert pour la distribution des niveaux par pays
labels = list(countries.keys())
values = [countries[label] for label in labels]
print(countries)
explode = [0.03] * len(labels)

fig, ax = plt.subplots()
ax.pie(values, autopct=lambda pct: func(pct, values), pctdistance=0.45,
       colors=palette, explode=explode, labels=labels,
       textprops={'fontsize':fontsize,'weight':'bold'})
centre_circle = plt.Circle((0,0),0.75,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
ax.axis('equal')
plt.tight_layout()
plt.show()

# Tri des interactions par somme de toutes les interactions (likes, plays, clears, records) pour chaque niveau
df_tmp = pd.DataFrame(interactions).transpose()
df_tmp['sum'] = df_tmp['likes'] + df_tmp['plays'] + df_tmp['clears'] + df_tmp['records']
df_tmp = df_tmp.sort_values(by=['sum'], ascending=False)

# Limite pour afficher uniquement les 100 niveaux les plus populaires
limit = 100

# Récupération des données pour l'axe y des différents types d'interactions
axis_id = df_tmp.index.tolist()[0:limit]
axis_plays = df_tmp['plays'].tolist()[0:limit]
axis_clears = df_tmp['clears'].tolist()[0:limit]
axis_records = df_tmp['records'].tolist()[0:limit]
axis_likes = df_tmp['likes'].tolist()[0:limit]

# Création d'un graphique à barres empilées pour visualiser les interactions par niveau de jeu
fig, ax = plt.subplots()
bottom_records  = [axis_plays[i] + axis_clears[i] for i in range(0, limit)]
bottom_likes    = [bottom_records[i] + axis_records[i] for i in range(0, limit)]

# Barres pour chaque type d'interaction
p1 = plt.bar(range(0, limit), axis_plays, color=palette[0], label='Plays')
p2 = plt.bar(range(0, limit), axis_clears, bottom=axis_plays, color=palette[1], label='Clears')
p3 = plt.bar(range(0, limit), axis_records, bottom=bottom_records, color=palette[2], label='Records')
p4 = plt.bar(range(0, limit), axis_likes, bottom=bottom_likes, color=palette[3], label='Likes')

# Ajout des étiquettes et légende
plt.ylabel('Players Interactions', fontsize=fontsize)
plt.xlabel('Game Maps', fontsize=fontsize)
ax.legend(prop={'size':fontsize-2})

# Ajustement de la taille de la figure
fig.set_size_inches(6, 3, forward=True)
plt.xlim(-1, 100)
plt.show()




# Import des données de la colonne 'sum' du DataFrame 'df_tmp'
data = df_tmp['sum']

# Ajustement des données à une loi de puissance (power law), en spécifiant que les données sont discrètes.
fit = powerlaw.Fit(data, discrete=True, estimate_discrete=False)

# Création d'un graphique pour la fonction de densité de probabilité (PDF)
fig, ax = plt.subplots()
# Tracé des données empiriques
fig_powerlaw = fit.plot_pdf(linewidth=3, color=palette[0], label='Données empiriques')
# Ajustement d'une loi de puissance sur les données
fit.power_law.plot_pdf(ax=fig_powerlaw, color=palette[1], linestyle='--', label='Ajustement Power law')
# Ajustement d'une loi log-normale pour comparaison
fit.lognormal.plot_pdf(ax=fig_powerlaw, color=palette[2], linestyle='--', label='Ajustement Log-normal')

# Ajout de la légende avec une taille de police réduite
ax.legend(prop={'size':fontsize-2})

# Ajustement de la taille du graphique
fig.set_size_inches(6, 3, forward=True)
plt.show()  # Affichage du graphique PDF

# Création d'un graphique pour la fonction de distribution cumulative (CDF)
fig, ax = plt.subplots()
fig_powerlaw = fit.plot_cdf(linewidth=3, color=palette[0], label='Données empiriques')
fit.power_law.plot_cdf(ax=fig_powerlaw, color=palette[1], linestyle='--', label='Ajustement Power law')
fit.lognormal.plot_cdf(ax=fig_powerlaw, color=palette[2], linestyle='--', label='Ajustement Log-normal')

# Ajout de la légende
ax.legend(prop={'size':fontsize-2})
fig.set_size_inches(6, 3, forward=True)
plt.show()  # Affichage du graphique CDF

# Création d'un graphique pour la fonction de distribution cumulative complémentaire (CCDF)
fig, ax = plt.subplots()
fig_powerlaw = fit.plot_ccdf(linewidth=3, color=palette[0], label='Données empiriques')
fit.power_law.plot_ccdf(ax=fig_powerlaw, color=palette[1], linestyle='--', label='Ajustement Power law')
fit.lognormal.plot_ccdf(ax=fig_powerlaw, color=palette[2], linestyle='--', label='Ajustement Log-normal')

# Ajout de la légende
ax.legend(prop={'size':fontsize-2})
fig.set_size_inches(6, 3, forward=True)
plt.show()  # Affichage du graphique CCDF

# Liste des distributions cumulatives (CDF) à tester avec le test de Kolmogorov-Smirnov
cdfs = [
    "norm", "alpha", "anglit", "arcsine", "beta", "betaprime", "bradford", "burr", 
    "cauchy", "chi", "chi2", "cosine", "dgamma", "dweibull", "erlang", "expon", 
    "exponweib", "exponpow", "fatiguelife", "foldcauchy", "f", "fisk", "foldnorm", 
    "gamma", "genexpon", "genextreme", "gengamma", "genlogistic", "genpareto", 
    "genhalflogistic", "gilbrat", "gompertz", "gumbel_l", "gumbel_r", "halfcauchy", 
    "halflogistic", "halfnorm", "hypsecant", "invgamma", "invweibull", "johnsonsb", 
    "johnsonsu", "laplace", "logistic", "loggamma", "loglaplace", "lognorm", 
    "lomax", "maxwell", "mielke", "nakagami", "pareto", "powerlaw", "powerlognorm", 
    "powernorm", "rdist", "reciprocal", "rayleigh", "rice", "recipinvgauss", 
    "semicircular", "t", "triang", "truncexpon", "truncnorm", "uniform", "vonmises", 
    "wald", "weibull_min", "weibull_max", "wrapcauchy"
]

# Boucle pour tester chaque distribution avec le test de Kolmogorov-Smirnov (KS)
for cdf in cdfs:
    # Ajustement des paramètres de chaque distribution sur les données
    parameters = eval("stats."+cdf+".fit(data)")
    
    # Application du test de Kolmogorov-Smirnov pour vérifier si les données suivent cette distribution
    D, p = stats.kstest(data, cdf, args=parameters)
    
    # Affichage des résultats du test (p-value et statistique D)
    print('p = %.25f, D = %.4f (%s)' % (p, D, cdf))

# Test de Kolmogorov-Smirnov (KS) :

# Ce test compare la distribution empirique des données avec une distribution théorique pour voir si elles sont similaires.
# Ici, la boucle itère sur une liste de distributions théoriques, ajuste chacune d’elles aux données, puis applique le test KS pour vérifier la similarité.
# Diagrammes PDF, CDF et CCDF :

# PDF : Représente la probabilité de chaque valeur spécifique dans les données.
# CDF : Représente la probabilité cumulative jusqu’à une valeur donnée.
# CCDF : Complément de la CDF, représentant la probabilité qu'une valeur soit plus grande qu'un certain seuil.
# Variables fig et ax :

# Ces objets sont utilisés pour la création et la personnalisation des graphiques.
# fig_powerlaw est l'axe principal pour chaque graphique, où les différentes distributions sont tracées.






















