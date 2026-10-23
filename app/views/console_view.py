def afficher_menu():
    print("\n" + "=" * 50)
    print("MENU AMAZON SCRAPING")
    print("=" * 50)

    print("1. lancer le scraping")
    print("2. Afficher les produits récupérés")
    print("3. Rechercher un produit")
    print("4. Consulter la base SQLite")
    print("5. Exporter les produits en CSV")
    print("6. Afficher les statistiques")
    print("0. Quitter")

    print("=" * 50)

    return input("Votre choix : ").strip()


def afficher_produits(produits):
    if not produits:
        print("Aucun produit trouvé")
        return

    print("\nPRODUITS TROUVES \n")

    for i, produit in enumerate(produits, start=1):

        print(f"Produit n {i}")
        print(f"Nom du produit {produit.nom}")
        print(f"Prix du produit {produit.prix}")
        print(f"Note du produit {produit.note}")
        print(f"Lien du produit {produit.lien}")
        print("." * 50)

def afficher_message(message):
    print(f"\n{message}")
