from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from app.models.produit import Produit
import time


def convertir_prix(texte):
    if not texte:
        return None

    # Gérer les prix en euros et dollars
    texte = texte.replace("$", "").replace("€", "").replace(",", ".").strip()

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


def verifier_blocage(driver):
    """Vérifie si Amazon a bloqué le scraping"""
    titre = driver.title.lower()
    page_source = driver.page_source.lower()

    if "sorry" in titre or "captcha" in page_source or "robot" in page_source:
        print("Amazon a détecté le scraping !")
        print("Attente de 5 secondes avant de continuer...")
        time.sleep(5)
        return True
    return False


def extraire_produits(driver, max_produits=20):
    produits = []

    # Vérifier si on est bloqué
    if verifier_blocage(driver):
        return produits

    print("\nChargement des produits...")
    for i in range(3):  # Scroll 3 fois
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1.5)  # Attendre le chargement

    # Revenir en haut
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    blocs = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-component-type="s-search-result"]'
    )

    print(f"Nombre de blocs trouvés : {len(blocs)}")

    for bloc in blocs[:max_produits]:
        try:
            # Chercher le titre
            elements_nom = bloc.find_elements(
                By.CSS_SELECTOR,
                "h2 a span, h2 span"
            )

            nom = ""
            for element in elements_nom:
                nom = element.text.strip()
                if nom and len(nom) > 5:
                    break

            if not nom:
                continue

            liens = bloc.find_elements(By.CSS_SELECTOR, "h2 a")
            lien = ""

            if liens:
                lien = liens[0].get_attribute("href") or ""
                if lien:
                    lien = urljoin(driver.current_url, lien)
                else:
                    continue
            else:
                continue

            # Extraire le prix
            prix = None
            selecteurs_prix = [
                ".a-price .a-offscreen",
                ".a-price-whole",
                "span.a-price span.a-offscreen"
            ]

            for selecteur in selecteurs_prix:
                try:
                    element_prix = bloc.find_element(By.CSS_SELECTOR, selecteur)
                    prix_texte = element_prix.get_attribute("textContent")
                    prix = convertir_prix(prix_texte)
                    if prix:
                        break
                except NoSuchElementException:
                    continue

            # Extraire la note
            note = None
            try:
                element_note = bloc.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
                note_texte = element_note.get_attribute("textContent")
                note = convertir_note(note_texte)
            except NoSuchElementException:
                pass

            produit = Produit(
                nom=nom,
                prix=prix,
                note=note,
                lien=lien
            )

            produits.append(produit)

            print(f"\n✓ Produit : {nom[:50]}...")
            print(f"  Prix    : {prix} €")
            print(f"  Note    : {note}/5")
            print(f"  Lien    : {lien[:60]}...")

        except Exception as erreur:
            print(f"✗ Produit ignoré : {erreur}")
            continue

    print(f"\nTotal des produits extraits : {len(produits)}")
    return produits