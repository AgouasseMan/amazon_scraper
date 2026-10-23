
from pathlib import Path

# Dossier principal du projet
BASE_DIR = Path(__file__).resolve().parent

# Base de données SQLite
DATABASE_PATH = BASE_DIR / "amazon.db"

# Fichier CSV demandé
CSV_PATH = (
    BASE_DIR
    / "data"
    / "tech"
    / "information"
    / "data.csv"
)

# Dossier des exports supplémentaires
EXPORT_DIR = BASE_DIR / "exports"

# Recherche à effectuer
SEARCH_URL = "https://www.amazon.com/s?k=ordinateur"

