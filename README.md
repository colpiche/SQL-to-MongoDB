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


## MongoDB collections

### abonnes

```json
{
    "_id": {
        "$oid": "661e668c09f8dde980de5a9f"
    },
    "abonne_id": 11,
    "prenom": "Wendy",
    "nom": "Norris",
    "adresse": "Ap #101-4789 Conubia St.",
    "telephone": "02 80 95 83 51",
    "date_adhesion": {
        "$date": "2021-08-31T00:00:00.000Z"
    },
    "date_naissance": {
        "$date": "1986-10-25T00:00:00.000Z"
    },
    "categorie_professionnelle_id": 47,
    "demandes": [
        {
            "livre_id": 34,
            "date": {
                "$date": "2024-04-13T00:00:00.000Z"
            }
        }
    ],
    "emprunts": [
        {
            "emprunt_id": 1682,
            "date_debut": {
                "$date": "2022-04-21T00:00:00.000Z"
            },
            "date_fin": null,
            "exemplaire_id": 150
        },
        {
            "emprunt_id": 1934,
            "date_debut": {
                "$date": "2022-09-25T00:00:00.000Z"
            },
            "date_fin": {
                "$date": "2022-10-25T00:00:00.000Z"
            },
            "exemplaire_id": 135
        }
    ]
}
```

### exemplaires

```json
{
    "_id": {
        "$oid": "661e668c09f8dde980de59cd"
    },
    "exemplaire_id": 1,
    "livre_id": 4,
    "etat": "ACCEPTABLE",
    "date_achat": {
        "$date": "2019-01-25T00:00:00.000Z"
    },
    "editeur_id": 32
}
```

### livre

```json
{
    "_id": {
        "$oid": "661e42a190370a06f828278f"
    },
    "livre_id": 4,
    "nom": "lectus justo",
    "auteurs": [
        {
            "auteur_id": 72,
            "prenom": "Latifah",
            "nom": "Wilkinson"
        },
        {
            "auteur_id": 75,
            "prenom": "Hall",
            "nom": "Paul"
        },
        {
            "auteur_id": 86,
            "prenom": "Anjolie",
            "nom": "Weber"
        }
    ],
    "genres": [
        {
            "genre_id": 6,
            "libelle": "odio"
        },
        {
            "genre_id": 15,
            "libelle": "lacus."
        }
    ],
    "synopsis": "mi lacinia mattis. Integer eu lacus. Quisque imperdiet, erat nonummy ultricies ornare, elit elit fermentum risus, at fringilla purus mauris a nunc. In at pede. Cras vulputate velit eu sem. Pellentesque ut ipsum ac mi eleifend egestas. Sed pharetra, felis eget varius ultrices, mauris ipsum porta elit,"
}
```