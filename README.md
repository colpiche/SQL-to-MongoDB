# SQL-to-MongoDB
Tiny Python script to transfer SQL tables to MongoDB collections

## SQL Tables

### abonne

| Column                           | Type         |
|----------------------------------|--------------|
| **_abonne_id_**                  | int AI PK    |
| prenom                           | varchar(50)  |
| nom                              | varchar(100) |
| adresse                          | varchar(255) |
| telephone                        | varchar(15)  |
| date_adhesion                    | date         |
| date_naissance                   | date         |
| **categorie_professionnelle_id** | int          |

### auteur

| Column          | Type         |
|-----------------|--------------|
| **_auteur_id_** | int AI PK    |
| prenom          | varchar(50)  |
| nom             | varchar(100) |

### demande_livre

| Column          | Type   |
|-----------------|--------|
| **_abonne_id_** | int PK |
| **_livre_id_**  | int PK |
| date            | date   |

### exemplaire

| Column              | Type        |
|---------------------|-------------|
| **_exemplaire_id_** | int AI PK   |
| etat                | varchar(42) |
| date_achat          | date        |
| **livre_id**        | int         |
| **editeur_id**      | int         |

### exemplaire_emprunt

| Column            | Type      |
|-------------------|-----------|
| **_emprunt_id_**  | int AI PK |
| date_debut        | date      |
| date_fin          | date      |
| **abonne_id**     | int       |
| **exemplaire_id** | int       |

### genre

| Column         | Type        |
|----------------|-------------|
| **_genre_id_** | int AI PK   |
| libelle        | varchar(50) |

### livre

| Column         | Type         |
|----------------|--------------|
| **_livre_id_** | int AI PK    |
| nom            | varchar(255) |
| synopsis       | longtext     |

### livre_auteur

| Column         | Type   |
|----------------|--------|
| **_livre_id_** | int PK |
| auteur_id      | int PK |

### livre_genre

| Column         | Type   |
|----------------|--------|
| **_livre_id_** | int PK |
| genre_id       | int PK |
