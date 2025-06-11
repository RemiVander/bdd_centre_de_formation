import os
from sqlmodel import create_engine

# Répertoire où les données seront stockées.
# Ce chemin est construit en utilisant le répertoire du fichier courant.
data_dir = os.path.join(os.path.dirname(__file__), "data")

# Crée le répertoire de données s'il n'existe pas déjà.
os.makedirs(data_dir, exist_ok=True)

# Chemin complet vers le fichier de base de données SQLite.
db_path = os.path.join(data_dir, "centre_de_formation.db")

# URL de connexion à la base de données SQLite.
DATABASE_URL = f"sqlite:///{db_path}"

# Crée un moteur de base de données SQLModel pour interagir avec la base de données.
# Le paramètre `echo=True` permet d'afficher les requêtes SQL exécutées, utile pour le débogage.
engine = create_engine(DATABASE_URL, echo=True)
