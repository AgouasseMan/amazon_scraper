from app.controllers.scraping_controller import ScrapingController
from app.views.console_view import afficher_menu, afficher_message


def main():
    controller = ScrapingController()

    try:
        while True:
            choix = afficher_menu()

            if choix == "1":
                controller.lancer_scraping()

            elif choix == "2":
                controller.afficher_produits_enregistres()

            elif choix == "3":
                controller.rechercher_produit()

            elif choix == "4":
                controller.afficher_produits_enregistres()

            elif choix == "5":
                controller.exporter_produits()

            elif choix == "6":
                controller.afficher_statistiques()

            elif choix == "0":
                print("\nFermeture de l'application.")
                break

            else:
                afficher_message("Choix invalide. Réessaie.")

    except KeyboardInterrupt:
        print("\nInterruption du programme.")

    finally:
        controller.fermer()


if __name__ == "__main__":
    main()


