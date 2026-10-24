from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import SEARCH_URL
from app.scraper.driver import creer_driver
from app.scraper.parsing import extraire_produits


class AmazonScraper:

    def scraper(self, recherche="ordinateur"):
        driver = creer_driver()

        try:
            print("\nDémarrage du scraping")


            base_url = SEARCH_URL.split("?")[0]
            url = f"{base_url}?{urlencode({'k': recherche})}"

            print(f" URL demandée : {url}")
            driver.get(url)

            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            print(f"📄 Titre de la page : {driver.title}")

            if "captcha" in driver.page_source.lower() or "sorry" in driver.title.lower():
                print("\nALERTE : Amazon a détecté un comportement automatisé (CAPTCHA ou blocage).")
                print("Astuce : Attendez 10 minutes, changez d'IP (VPN/4G), ou résolvez le CAPTCHA manuellement.")

                with open("page_amazon.html", "w", encoding="utf-8") as fichier:
                    fichier.write(driver.page_source)
                print(" Page de blocage sauvegardée dans 'page_amazon.html'")
                return []

            print("Chargement des résultats...")
            try:
                WebDriverWait(driver, 30).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, '[data-component-type="s-search-result"]')) > 0
                )
            except TimeoutException:
                print("\nDélai d'attente dépassé : Aucun produit trouvé après 30 secondes.")
                with open("page_amazon.html", "w", encoding="utf-8") as fichier:
                    fichier.write(driver.page_source)
                print("Page HTML sauvegardée dans 'page_amazon.html' pour analyse.")
                return []


            print("Extraction des données en cours")
            produits = extraire_produits(driver)

            print(f"\nSuccès ! Nombre de produits récupérés : {len(produits)}")
            return produits

        except Exception as erreur:
            print(f"\n Erreur critique pendant le scraping : {erreur}")
            return []

        finally:
            print("Fermeture du navigateur...")
            driver.quit()