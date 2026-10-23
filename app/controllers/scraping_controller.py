from app.scraper.amazon_scraper import AmazonScraper
from app.models.depot import Depot
from app.views.console_view import afficher_produits, afficher_message
from app.views.export_view import exporter_csv


class ScrapingController:

    def __init__(self):
        self.depot = Depot()

    def lancer_scraping(self):
        try:
            print("\nDémarrage du scraping...")

            scraper = AmazonScraper()
            produits = scraper.scraper()

            for produit in produits:
                self.depot.ajouter_produit(produit)

            afficher_message(
                f"{len(produits)} produit(s) récupéré(s)."
            )

            afficher_produits(produits)

        except Exception as erreur:
            afficher_message(f"Erreur pendant le scraping : {erreur}")

    def afficher_produits_enregistres(self):
        lignes = self.depot.obtenir_produits()

        if not lignes:
            afficher_message("La base de données est vide.")
            return

        print("\n========== PRODUITS ENREGISTRÉS ==========")

        for ligne in lignes:
            nom, prix, note, lien = ligne

            print(f"\nNom  : {nom}")
            print(f"Prix : {prix}")
            print(f"Note : {note}")
            print(f"Lien : {lien}")
            print("-" * 40)

    def rechercher_produit(self):
        recherche = input(
            "\nNom du produit à rechercher : "
        ).strip().lower()

        if not recherche:
            afficher_message("La recherche ne peut pas être vide.")
            return

        produits = self.depot.obtenir_produits()

        resultats = [
            produit for produit in produits
            if recherche in (produit[0] or "").lower()
        ]

        if resultats:
            for produit in resultats:
                print(f"\nNom   : {produit[0]}")
                print(f"Prix  : {produit[1]}")
                print(f"Note  : {produit[2]}")
                print(f"Lien  : {produit[3]}")
        else:
            afficher_message("Aucun produit correspondant.")

    def exporter_produits(self):
        lignes = self.depot.obtenir_produits()

        if not lignes:
            afficher_message("Aucune donnée à exporter.")
            return

        from app.models.produit import Produit

        produits = [
            Produit(
                nom=ligne[0],
                prix=ligne[1],
                note=ligne[2],
                lien=ligne[3],
            )
            for ligne in lignes
        ]

        exporter_csv(produits)

    def afficher_statistiques(self):
        lignes = self.depot.obtenir_produits()

        total = len(lignes)

        prix_valides = [
            ligne[1]
            for ligne in lignes
            if ligne[1] is not None
        ]

        print("\n========== STATISTIQUES ==========")
        print(f"Nombre total de produits : {total}")

        if prix_valides:
            print(f"Prix minimum : {min(prix_valides)}")
            print(f"Prix maximum : {max(prix_valides)}")
            print(f"Prix moyen   : {sum(prix_valides) / len(prix_valides):.2f}")
        else:
            print("Aucun prix disponible.")

    def fermer(self):
        self.depot.fermer()


