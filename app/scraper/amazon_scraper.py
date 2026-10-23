from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import SEARCH_URL
from app.scraper.driver import creer_driver
from app.scraper.parsing import extraire_produits


class AmazonScraper:

    def scraper(self):
        driver = creer_driver()

        try:
            print("Ouverture de la page Amazon...")
            driver.get(SEARCH_URL)

            # Attendre le chargement de la page
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )

            print("Titre de la page :", driver.title)
            print("URL :", driver.current_url)

            # Attendre les blocs produits, si Amazon les affiche
            try:
                WebDriverWait(driver, 15).until(
                    lambda d: d.find_elements(
                        By.CSS_SELECTOR,
                        '[data-component-type="s-search-result"]'
                    )
                )
            except Exception:
                print(
                    "Attention : aucun bloc produit détecté "
                    "après 15 secondes."
                )

            return extraire_produits(driver)

        finally:
            driver.quit()

