import datetime
import pymysql.cursors
import pymongo
import os
from dotenv import load_dotenv
from typing import Any


# Fonction pour exécuter une requête SQL et récupérer les résultats
def query(sql_query: str) -> tuple[dict[str, Any], ...]:
    cursor = sql_connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


# Fonction pour insérer des documents dans une collection MongoDB
def mongo_insert(collection: str, documents: list[dict[str, Any]]) -> None:
    mongo_collection = mongo_db[collection]
    mongo_collection.insert_many(documents)


# Connexion à la base de données SQL
load_dotenv()
sql_connection = pymysql.connect(
    host=str(os.getenv('HOST')),
    user=str(os.getenv('USER')),
    password=str(os.getenv('PASS')),
    database=str(os.getenv('DB'))
)

# Connexion à la base de données MongoDB
mongo_client = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_client['USRS60']


# ================================== LIVRES ===================================

# Requête SQL pour récupérer les données des tables associées aux livres
sql_query = """
    SELECT livre.livre_id, livre.nom AS livre_nom, livre.synopsis,
           auteur.auteur_id, auteur.prenom AS auteur_prenom, auteur.nom AS auteur_nom,
           genre.genre_id, genre.libelle AS genre_libelle
    FROM livre
    LEFT JOIN livre_auteur ON livre.livre_id = livre_auteur.livre_id
    LEFT JOIN auteur ON livre_auteur.auteur_id = auteur.auteur_id
    LEFT JOIN livre_genre ON livre.livre_id = livre_genre.livre_id
    LEFT JOIN genre ON livre_genre.genre_id = genre.genre_id
"""

rows = query(sql_query)

# Dictionnaires temporaires pour stocker les auteurs et les genres sans doublon
auteurs_dict = {}
genres_dict = {}

# Liste pour stocker les documents de livre uniques
livres_list = []

# Transformation des données
for row in rows:
    livre_id = row['livre_id']
    # Créer un nouveau document de livre s'il n'existe pas déjà
    livre = next((livre for livre in livres_list if livre['livre_id'] == livre_id), None)
    if not livre:
        livre = {
            "livre_id": livre_id,
            "nom": row['livre_nom'],
            "auteurs": [],
            "genres": []
        }
        if row['synopsis'] is not None:
            livre['synopsis'] = row['synopsis']
        livres_list.append(livre)

    # Ajouter l'auteur au document de livre s'il n'existe pas déjà et s'il n'est pas null
    if row['auteur_id'] is not None:
        auteur_id = row['auteur_id']
        if auteur_id not in auteurs_dict:
            auteurs_dict[auteur_id] = {
                "auteur_id": auteur_id,
                "prenom": row['auteur_prenom'] if row['auteur_prenom'] is not None else "",
                "nom": row['auteur_nom'] if row['auteur_nom'] is not None else ""
            }
        livre['auteurs'].append(auteurs_dict[auteur_id])

    # Ajouter le genre au document de livre s'il n'existe pas déjà et s'il n'est pas null
    if row['genre_id'] is not None:
        genre_id = row['genre_id']
        if genre_id not in genres_dict:
            genres_dict[genre_id] = {
                "genre_id": genre_id,
                "libelle": row['genre_libelle'] if row['genre_libelle'] is not None else ""
            }
        livre['genres'].append(genres_dict[genre_id])


# Insérer les documents de livre dans MongoDB
mongo_insert('livres', livres_list)


# =============================== EXEMPLAIRES ================================

# Requête SQL pour récupérer les données de la table "exemplaire"
sql_query = """
    SELECT * FROM exemplaire
"""

rows = query(sql_query)

# Liste pour stocker les documents d'exemplaire
exemplaire_list = []

# Transformation des données de la table "exemplaire"
for row in rows:
    exemplaire = {
        "exemplaire_id": row['exemplaire_id'],
        "livre_id": row['livre_id'],
        "etat": row['etat'],
        "date_achat": datetime.datetime.combine(row['date_achat'], datetime.time(0, 0)) if row['date_achat'] else None,
        "editeur_id": row['editeur_id']
    }
    exemplaire_list.append(exemplaire)

# Insérer les documents d'exemplaire dans MongoDB
mongo_insert('exemplaires', exemplaire_list)


# ================================== ABONNES ==================================

# Requête SQL pour récupérer les données de la table "abonne"
sql_query = """
    SELECT * FROM abonne
"""

rows = query(sql_query)

# Dictionnaire pour stocker les abonnés sans redondance
abonnes_dict = {}

# Transformation des données de la table "abonne"
for row in rows:
    abonne_id = row['abonne_id']
    # Vérifie si l'abonné existe déjà dans le dictionnaire
    if abonne_id not in abonnes_dict:
        abonnes_dict[abonne_id] = {
            "abonne_id": abonne_id,
            "prenom": row['prenom'],
            "nom": row['nom'],
            "adresse": row['adresse'],
            "telephone": row['telephone'],
            "date_adhesion": datetime.datetime.combine(row['date_adhesion'], datetime.time(0, 0)) if row['date_adhesion'] else None,
            "date_naissance": datetime.datetime.combine(row['date_naissance'], datetime.time(0, 0)) if row['date_naissance'] else None,
            "categorie_professionnelle_id": row['categorie_professionnelle_id'],
            "demandes": [],
            "emprunts": []
        }

# Requête SQL pour récupérer les données de la table "demande_livre"
sql_query = """
    SELECT * FROM demande_livre
"""

rows = query(sql_query)

# Transformation des données de la table "demande_livre"
for row in rows:
    abonne_id = row['abonne_id']
    # Ajoute la demande au bon abonné dans le dictionnaire
    if abonne_id in abonnes_dict:
        abonnes_dict[abonne_id]["demandes"].append({
            "livre_id": row['livre_id'],
            "date": datetime.datetime.combine(row['date'], datetime.time(0, 0))
        })

# Requête SQL pour récupérer les données de la table "exemplaire_emprunt"
sql_query = """
    SELECT * FROM exemplaire_emprunt
"""

rows = query(sql_query)

# Transformation des données de la table "exemplaire_emprunt"
for row in rows:
    abonne_id = row['abonne_id']
    date_fin: datetime.datetime | None = None
    if row['date_fin'] is not None:
        date_fin = datetime.datetime.combine(row['date_fin'], datetime.time(0, 0))
    # Ajoute l'emprunt au bon abonné dans le dictionnaire
    if abonne_id in abonnes_dict:
        abonnes_dict[abonne_id]["emprunts"].append({
            "emprunt_id": row['emprunt_id'],
            "date_debut": datetime.datetime.combine(row['date_debut'], datetime.time(0, 0)),
            "date_fin": date_fin,
            "exemplaire_id": row['exemplaire_id']
        })

# Liste des documents d'abonné
abonnes_list = list(abonnes_dict.values())

# Insérer les documents d'abonné dans MongoDB
mongo_insert('abonnes', abonnes_list)


# ========================== FERMETURE DES CONNEXIONS =========================

sql_connection.close()
mongo_client.close()
