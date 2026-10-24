from pathlib import Path

# Dossier principal du projet
BASE_DIR = Path(__file__).resolve().parent

# Base de données SQLite
DATABASE_PATH = BASE_DIR / "amazon.db"

# Fichier CSV demandé
CSV_PATH = BASE_DIR / "data" / "tech" / "information" / "data.csv"

# Dossier des exports supplémentaires
EXPORT_DIR = BASE_DIR / "exports"

# CORRECTION ICI : Utiliser amazon.fr pour une recherche en français
SEARCH_URL = "https://www.amazon.fr/s?k=ordinateur"

# Création automatique des dossiers s'ils n'existent pas
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)