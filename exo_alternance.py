import pandas as pd
import os
import matplotlib.pyplot as plt

chemin_data = '../exo_alternance/data'
chemin_population_csv = os.path.join(chemin_data, 'population-communes.csv')
chemin_fichier_json = os.path.join(chemin_data, 'coiffeurs.json')



if not os.path.exists(chemin_population_csv):
    print(f"Le fichier {chemin_population_csv} n'existe pas. Veuillez vérifier le chemin.")
    exit(1)


if not os.path.exists(chemin_fichier_json):
    print(f"Le fichier {chemin_fichier_json} n'existe pas. Veuillez vérifier le chemin.")
    exit(1)

# Ouvrir le fichier JSON et charger les données
with open(chemin_fichier_json, 'r') as fichier:
    json_data = pd.read_json(fichier)

# Extraire les 'features' des données JSON
features = json_data['data']['features']
# Convertir les données JSON en DataFrame pandas
coiffure_data = pd.json_normalize(features)
# Supprimer les colonnes inutiles
coiffure_data = coiffure_data.drop(columns=['type', 'geometry.type', 'geometry.coordinates'])
# Renommer les colonnes pour une meilleure lisibilité
coiffure_data.rename(columns={'properties.ville': 'Ville', 'properties.nom': 'Salon'}, inplace=True)
# Nettoyer les données de la colonne 'Ville'
coiffure_data['Ville'] = coiffure_data['Ville'].str.strip().str.lower()

# Charger les données de population depuis le fichier CSV en faisant attention aux noms des colonnes
population_data = pd.read_csv(chemin_population_csv, delimiter=';')
# Renommer les colonnes pour une meilleure lisibilité
population_data.rename(columns={'COM': 'Ville', 'PTOT': 'Population'}, inplace=True)
# Nettoyer les données de la colonne 'Ville'
population_data['Ville'] = population_data['Ville'].str.strip().str.lower()

# Calculer le nombre de salons par ville
nombre_salons_par_ville = coiffure_data['Ville'].value_counts().reset_index()
# Renommer les colonnes pour une meilleure lisibilité
nombre_salons_par_ville.columns = ['Ville', 'Nombre de Salons']

# Fusionner les données des salons avec les données de population
data_merged = pd.merge(nombre_salons_par_ville, population_data, on='Ville', how='inner')
data_merged = data_merged.sort_values(by='Population', ascending=False)
# data_merged = data_merged.drop_duplicates(subset='Ville')

# Ajouter une colonne pour le nombre moyen d'habitants par salon
data_merged['Habitants par Salon'] = (data_merged['Population'] / data_merged['Nombre de Salons']).round(0)

# Créer le répertoire de résultats si nécessaire
repertoire_resultats = '../exo_alternance/result'
os.makedirs(repertoire_resultats, exist_ok=True)

# Sauvegarder le nombre de salons par ville en CSV
nombre_salons_par_ville.to_csv(os.path.join(repertoire_resultats, 'nombre_salons_par_ville.csv'), index=False)

# Sauvegarder le nombre de salons et la population par ville en CSV
data_merged[['Ville', 'Nombre de Salons', 'Population']].to_csv(os.path.join(repertoire_resultats, 'salons_population_par_ville.csv'), index=False)

# Sauvegarder le nombre moyen d'habitants par salon par ville en CSV
data_merged = data_merged.sort_values(by='Habitants par Salon', ascending=False)

data_merged[['Ville', 'Nombre de Salons', 'Population', 'Habitants par Salon']].to_csv(os.path.join(repertoire_resultats, 'habitants_par_salon_par_ville.csv'), index=False)

# Sauvegarder la vue détaillée avec le nombre moyen d'habitants par salon en CSV
data_merged[['Ville','Habitants par Salon']].to_csv(os.path.join(repertoire_resultats, 'habitants_par_salon.csv'), index=False)
data_merged[['Ville','Habitants par Salon']].plot(kind='bar', x='Ville', y='Habitants par Salon', legend=True, title='Nombre moyen d\'habitants par salon par ville', figsize=(300, 15), fontsize=5)

# Sauvegarder le graphique en image
plt.savefig(os.path.join(repertoire_resultats, 'habitants_par_salon.png'))

# Afficher un message de succès lorsque tous les fichiers CSV ont été créés
print("Les fichiers CSV ont été créés avec succès.")