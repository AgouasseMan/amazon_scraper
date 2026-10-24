from urllib.parse import urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import SEARCH_URL
from app.scraper.driver import creer_driver
from app.scraper.parsing import extraire_produits


class AmazonScraper:

    def scraper(self, recherche="ordinateur"):
        driver = creer_driver()

        try:
            print("\nDémarrage du scraping...")

            # Construire l'URL de recherche
            base_url = SEARCH_URL.split("?")[0]
            url = f"{base_url}?{urlencode({'k': recherche})}"

            print("URL demandée :", url)

            driver.get(url)

            # Attendre la fin du chargement initial
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )

            print("Titre de la page :", driver.title)
            print("URL actuelle :", driver.current_url)

            # Vérifier si des résultats apparaissent
            try:
                WebDriverWait(driver, 15).until(
                    lambda d: d.find_elements(
                        By.CSS_SELECTOR,
                        '[data-component-type="s-search-result"]'
                    )
                )
            except Exception:
                print("\nAucun résultat détecté.")
                print("Vérifie la page affichée dans Chrome.")

                with open(
                    "page_amazon.html",
                    "w",
                    encoding="utf-8"
                ) as fichier:
                    fichier.write(driver.page_source)

                print("HTML enregistré dans page_amazon.html")
                return []

            # Extraire les produits
            produits = extraire_produits(driver)

            print(
                f"\nNombre de produits récupérés : {len(produits)}"
            )

            return produits

        except Exception as erreur:
            print("Erreur pendant le scraping :", erreur)
            return []

        finally:
            driver.quit()


