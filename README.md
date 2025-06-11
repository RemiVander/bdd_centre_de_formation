# Contexte du projet

Vous êtes Data Engineer au sein d’un centre de formation (CF-Tech) qui dispense des cours et ateliers sur les technologies numériques. Jusqu’à présent, les informations concernant les sessions, les salles, les formateurs et les apprenants étaient gérées à la main, au moyen de fichiers Excel et d’un ERP vieillissant. La direction souhaite passer à une solution plus robuste : une base de données relationnelle pilotée par un ORM (SQLAlchemy/SQLModel) avec migrations (Alembic) et validation stricte des données (Pydantic).

L’objectif est d’avoir un système centralisé capable de :

- Gérer l’ensemble des utilisateurs de la plateforme (apprenants, formateurs, staff pédagogique, administrateurs).
- Suivre les sessions de formation (planning, salle, formateur, capacité).
- Enregistrer les inscriptions des apprenants aux sessions et leur historique d’avancement.
- Assurer la qualité des données à l’insertion (emails valides, dates cohérentes, plage d’âge, unicité des comptes, etc.).
- Faire évoluer le schéma au fil des besoins (ajout de nouveaux rôles, champs, etc.) sans interrompre l’exploitation.

## Description

Ce projet est une application web développée avec Flask et SQLModel pour gérer les cours, les salles, les enseignants et les inscriptions des étudiants dans un centre de formation. L'application permet aux étudiants de s'inscrire à des cours et aux enseignants de gérer leurs sessions.

## Fonctionnalités

- Affichage des cours disponibles
- Inscription des étudiants aux cours
- Gestion des sessions par les enseignants
- Visualisation des salles et des capacités

## Structure du Projet
```
bdd_centre_de_formatop,/
├── alembic/                # Contient les fichiers de configuration et les scripts de migration pour la base de données.
│   ├── versions/               # Contient les fichiers de migration de la base de données.
│   ├── env.py                  # Configuration de l'environnement Alembic.
│   ├── script.py.mako          # Template pour les scripts de migration.                
├── app/
│   ├── data/               # Contient le fichier de la base de données SQLite.
│   ├── models/             # Contient les modèles de données SQLModel.
│       ├── admin.py            # Modèle pour les administrateurs.
│       ├── class_session.py    # Modèle pour les sessions de cours.
│       ├── equipments.py       # Modèle pour les équipements
│       ├── registration.py     # Modèle pour les inscriptions.
│       ├── room.py             # Modèle pour les salles.
│       ├── student.py          # Modèle pour les étudiants.
│       ├── teacher.py          # Modèle pour les enseignants.
│       └── user.py             # Contient les routes principales de l'application.
├── routes/                 # Définit les routes et les vues de l'application.
│       └── routes.py           # Modèle pour les utilisateurs.
├── script_populate/        # Contient un script pour peupler la base de données avec des données initiales.
├── static/                 # Contient les fichiers statiques (CSS,images).
│   ├── assets/                 # Contient les ressources statiques supplémentaires.
│   ├── css/                    # Contient les fichiers CSS pour le style de l'application.
├── templates/              # Contient les fichiers de template HTML.
│   ├── available_course.html   # Page pour afficher les cours disponibles.
│   ├── calendar.html           # Page pour afficher le calendrier des cours
│   ├── create_session.html     # Page pour créer une nouvelle session de cours. 
│   ├── error_user_exists.html  # Page d'erreur pour les utilisateurs existants.
│   ├── home.html               # Page d'accueil de l'application.
│   ├── login.html              # Page de connexion. 
    ├── register_student.html   # Page d'inscription pour les étudiants.
│   ├── register_teacher.html   # Page d'inscription pour les enseignants.
│   ├── success_session.html    # Page de succès pour la création de session.
│   ├── success.html            # Page de succès générale.  
├── README.md               # Ce fichier
└── LICENSE                 # Licence MIT
```

## Prérequis

- Python 3.8 ou supérieur
- pip (Python Package Installer)

## Installation

1. Clonez le dépôt sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/centre-de-formation.git
