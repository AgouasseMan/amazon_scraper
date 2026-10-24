import time
from urllib.parse import urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config import SEARCH_URL, BASE_DIR
from app.scraper.driver import creer_driver
from app.scraper.parsing import extraire_produits, est_bloque, SELECTEUR_BLOCS


class AmazonScraper:

    def scraper(self, recherche="ordinateur"):
        driver = creer_driver()

        try:
            base_url = SEARCH_URL.split("?")[0]
            url = f"{base_url}?{urlencode({'k': recherche})}"

            print(f"URL demandée : {url}")
            driver.get(url)

            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            print(f"Titre de la page : {driver.title}")

            self._accepter_cookies(driver)

            # Blocage réel : on laisse 2 minutes pour résoudre le CAPTCHA à la main
            if est_bloque(driver):
                if not self._attendre_resolution_manuelle(driver):
                    self._sauvegarder_debug(driver)
                    return []

            print("Chargement des résultats...")
            try:
                WebDriverWait(driver, 30).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, SELECTEUR_BLOCS)) > 0
                )
            except TimeoutException:
                print("\nAucun produit trouvé après 30 secondes.")
                self._sauvegarder_debug(driver)
                return []

            produits = extraire_produits(driver)

            if not produits:
                print("\nDes blocs existent mais aucun produit n'a pu être lu.")
                self._sauvegarder_debug(driver)

            return produits

        except Exception as erreur:
            print(f"\nErreur critique pendant le scraping : {erreur}")
            return []

        finally:
            print("Fermeture du navigateur...")
            driver.quit()

    @staticmethod
    def _accepter_cookies(driver):
        """Clique sur 'Accepter' si la bannière de cookies d'Amazon apparaît."""
        try:
            boutons = driver.find_elements(By.CSS_SELECTOR, "#sp-cc-accept")
            if boutons:
                boutons[0].click()
                print("Bannière de cookies acceptée.")
                time.sleep(1)
        except Exception:
            pass

    @staticmethod
    def _attendre_resolution_manuelle(driver, delai=120):
        print("\nAmazon affiche une page de vérification (CAPTCHA).")
        print(f"Résous-la dans la fenêtre Chrome : j'attends {delai} secondes...")

        debut = time.time()
        while time.time() - debut < delai:
            time.sleep(3)
            if not est_bloque(driver):
                print("Vérification passée, on continue.")
                return True

        print("Délai dépassé : le CAPTCHA n'a pas été résolu.")
        return False

    @staticmethod
    def _sauvegarder_debug(driver):
        """Sauvegarde la page et une capture d'écran pour comprendre le problème."""
        html = BASE_DIR / "page_amazon.html"
        png = BASE_DIR / "page_amazon.png"

        with open(html, "w", encoding="utf-8") as fichier:
            fichier.write(driver.page_source)
        try:
            driver.save_screenshot(str(png))
        except Exception:
            pass

        print(f"Page sauvegardée : {html}")
        print(f"Capture d'écran  : {png}")