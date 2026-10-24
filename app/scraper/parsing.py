from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from app.models.produit import Produit


def convertir_prix(texte):
    if not texte:
        return None

    texte = texte.replace("$", "").replace(",", "").strip()

    try:
        return float(texte)
    except ValueError:
        return None


def convertir_note(texte):
    if not texte:
        return None

    try:
        return float(texte.split()[0].replace(",", "."))
    except (ValueError, IndexError):
        return None


def extraire_produits(driver):
    produits = []

    blocs = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-component-type="s-search-result"]'
    )

    print(f"\nNombre de blocs trouvés : {len(blocs)}")

    for bloc in blocs:
        try:
            # Chercher le titre avec plusieurs sélecteurs possibles
            elements_nom = bloc.find_elements(
                By.CSS_SELECTOR,
                "h2 a, h2 span"
            )

            nom = ""

            for element in elements_nom:
                nom = element.text.strip()
                if nom:
                    break

            if not nom:
                continue

            # Chercher le lien du produit
            liens = bloc.find_elements(
                By.CSS_SELECTOR,
                "h2 a"
            )

            lien = ""

            if liens:
                lien = liens[0].get_attribute("href") or ""

            if lien:
                lien = urljoin(driver.current_url, lien)
            else:
                continue

            # Extraire le prix
            elements_prix = bloc.find_elements(
                By.CSS_SELECTOR,
                ".a-price .a-offscreen"
            )

            prix = None

            if elements_prix:
                prix = convertir_prix(
                    elements_prix[0].get_attribute("textContent")
                )

            # Extraire la note
            elements_note = bloc.find_elements(
                By.CSS_SELECTOR,
                "span.a-icon-alt"
            )

            note = None

            if elements_note:
                note = convertir_note(
                    elements_note[0].get_attribute("textContent")
                )

            produit = Produit(
                nom=nom,
                prix=prix,
                note=note,
                lien=lien
            )

            produits.append(produit)

            print(f"\nProduit : {nom}")
            print(f"Prix    : {prix}")
            print(f"Note    : {note}")
            print(f"Lien    : {lien}")

        except Exception as erreur:
            print("Produit ignoré :", erreur)

    print(f"\nTotal des produits extraits : {len(produits)}")

    return produits



