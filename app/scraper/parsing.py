from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from app.models.produit import Produit
import re
import time


def convertir_prix(texte):
    if not texte:
        return None

    texte = texte.replace("\xa0", "").replace(" ", "")
    texte = texte.replace("€", "").replace("$", "").replace("£", "")

    if "," in texte and "." in texte:
        if texte.rfind(",") > texte.rfind("."):
            texte = texte.replace(".", "").replace(",", ".")
        else:
            texte = texte.replace(",", "")
    elif "," in texte:
        texte = texte.replace(",", ".")

    texte = re.sub(r"[^0-9.]", "", texte)

    try:
        return float(texte)
    except ValueError:
        return None


def convertir_note(texte):
    if not texte:
        return None

    correspondance = re.search(r"(\d+(?:[,.]\d+)?)", texte)

    if correspondance:
        try:
            return float(correspondance.group(1).replace(",", "."))
        except ValueError:
            return None

    return None


def verifier_blocage(driver):
    titre = driver.title.lower()
    page_source = driver.page_source.lower()

    if (
        "captcha" in titre
        or "captcha" in page_source
        or "robot check" in titre
        or "validatecaptcha" in page_source
    ):
        print("Attention : Amazon affiche une page de vérification.")
        return True

    return False


def extraire_produits(driver, max_produits=20):
    produits = []

    if verifier_blocage(driver):
        return produits

    print("\nChargement des produits...")

    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1)

    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)

    blocs = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-component-type="s-search-result"]'
    )

    print(f"Nombre de blocs trouvés : {len(blocs)}")

    for bloc in blocs:
        if len(produits) >= max_produits:
            break

        try:
            # Récupération du nom et du lien
            liens = bloc.find_elements(
                By.CSS_SELECTOR,
                "h2 a"
            )

            nom = ""
            lien = ""

            for element in liens:
                nom = element.text.strip()

                if not nom:
                    nom = (
                        element.get_attribute("aria-label") or ""
                    ).strip()

                if not nom:
                    spans = element.find_elements(
                        By.CSS_SELECTOR,
                        "span"
                    )

                    for span in spans:
                        nom = span.text.strip()
                        if nom:
                            break

                href = element.get_attribute("href")

                if href:
                    lien = urljoin(driver.current_url, href)

                if nom and lien:
                    break

            if not nom or not lien:
                print("Produit ignoré : nom ou lien introuvable.")
                continue

            # Récupération du prix
            prix = None

            elements_prix = bloc.find_elements(
                By.CSS_SELECTOR,
                ".a-price .a-offscreen"
            )

            for element in elements_prix:
                texte_prix = (
                    element.get_attribute("textContent") or ""
                ).strip()

                prix = convertir_prix(texte_prix)

                if prix is not None:
                    break

            # Récupération de la note
            note = None

            elements_notes = bloc.find_elements(
                By.CSS_SELECTOR,
                "span.a-icon-alt"
            )

            for element in elements_notes:
                texte_note = (
                    element.get_attribute("textContent") or ""
                ).strip()

                note = convertir_note(texte_note)

                if note is not None:
                    break

            produit = Produit(
                nom=nom,
                prix=prix,
                note=note,
                lien=lien
            )

            produits.append(produit)

            print(f"\nProduit : {nom[:70]}")
            print(f"Prix    : {prix} €")
            print(f"Note    : {note}/5")
            print(f"Lien    : {lien[:100]}")

        except Exception as erreur:
            print(f"Erreur pendant l'extraction : {erreur}")

    print(f"\nTotal des produits extraits : {len(produits)}")

    return produits


