
import sqlite3

from config import DATABASE_PATH
from app.models.produit import Produit


class Depot:

    def __init__(self):
        self.connexion = sqlite3.connect(DATABASE_PATH)
        self.creer_table()

    def creer_table(self):
        requete = """
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL,
            note REAL,
            lien TEXT UNIQUE
        )
        """

        with self.connexion:
            self.connexion.execute(requete)

    def ajouter_produit(self, produit: Produit):
        requete = """
        INSERT OR IGNORE INTO produits
        (nom, prix, note, lien)
        VALUES (?, ?, ?, ?)
        """

        with self.connexion:
            self.connexion.execute(
                requete,
                (
                    produit.nom,
                    produit.prix,
                    produit.note,
                    produit.lien,
                ),
            )

    def obtenir_produits(self):
        requete = """
        SELECT nom, prix, note, lien
        FROM produits
        ORDER BY id DESC
        """

        curseur = self.connexion.execute(requete)

        return curseur.fetchall()

    def fermer(self):
        self.connexion.close()

