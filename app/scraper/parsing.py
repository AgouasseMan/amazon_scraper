import re
import time
from urllib.parse import urljoin

from selenium.webdriver.common.by import By

from app.models.produit import Produit

# Blocs de résultats : sélecteur principal + solution de secours
SELECTEUR_BLOCS = (
    'div[data-component-type="s-search-result"], '
    'div.s-main-slot div[data-asin]:not([data-asin=""])'
)


def est_bloque(driver):
    """True seulement si Amazon affiche vraiment une page de blocage/CAPTCHA."""
    titre = driver.title.lower()
    url = driver.current_url.lower()

    return (
        "robot check" in titre
        or "sorry" in titre
        or "désolé" in titre
        or "validatecaptcha" in url
        or len(driver.find_elements(
            By.CSS_SELECTOR, "form[action*='validateCaptcha']")) > 0
    )


def texte(element):
    """Texte d'un élément, même s'il n'est pas visible à l'écran."""
    return (element.get_attribute("textContent") or "").strip()


def convertir_prix(valeur):
    """'1 299,99 €' -> 1299.99 (format amazon.fr)."""
    if not valeur:
        return None

    valeur = re.sub(r"[^\d,\.]", "", valeur)  # enlève €, espaces, espaces insécables

    if "," in valeur:
        valeur = valeur.replace(".", "").replace(",", ".")

    try:
        return float(valeur)
    except ValueError:
        return None


def convertir_note(valeur):
    """'4,3 sur 5 étoiles' -> 4.3"""
    if not valeur:
        return None

    try:
        return float(valeur.split()[0].replace(",", "."))
    except (ValueError, IndexError):
        return None


def extraire_nom(bloc):
    for h2 in bloc.find_elements(By.CSS_SELECTOR, "h2"):
        label = (h2.get_attribute("aria-label") or "").strip()
        if len(label) > 5:
            return label

    for selecteur in ("h2 span", "h2", "span.a-size-medium", "span.a-size-base-plus"):
        for element in bloc.find_elements(By.CSS_SELECTOR, selecteur):
            nom = texte(element)
            if len(nom) > 5:
                return nom
    return ""


def extraire_lien(bloc, base_url):
    # Le plus fiable : l'identifiant ASIN du produit
    asin = (bloc.get_attribute("data-asin") or "").strip()
    if asin:
        return urljoin(base_url, f"/dp/{asin}")

    for selecteur in ("h2 a", "a:has(h2)", "a.a-link-normal[href*='/dp/']"):
        elements = bloc.find_elements(By.CSS_SELECTOR, selecteur)
        if elements:
            href = elements[0].get_attribute("href")
            if href:
                return urljoin(base_url, href)
    return ""


def extraire_prix(bloc):
    for selecteur in (".a-price .a-offscreen", "span.a-offscreen", ".a-price-whole"):
        for element in bloc.find_elements(By.CSS_SELECTOR, selecteur):
            prix = convertir_prix(texte(element))
            if prix:
                return prix
    return None


def extraire_note(bloc):
    for selecteur in ("span.a-icon-alt", "[aria-label*='sur 5']"):
        for element in bloc.find_elements(By.CSS_SELECTOR, selecteur):
            note = convertir_note(
                texte(element) or element.get_attribute("aria-label")
            )
            if note:
                return note
    return None


def extraire_produits(driver, max_produits=20):
    produits = []

    print("\nChargement des produits...")
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1.5)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    blocs = driver.find_elements(By.CSS_SELECTOR, SELECTEUR_BLOCS)
    print(f"Nombre de blocs trouvés : {len(blocs)}")

    ignores_nom = 0
    ignores_lien = 0

    for bloc in blocs:
        if len(produits) >= max_produits:
            break

        try:
            nom = extraire_nom(bloc)
            if not nom:
                ignores_nom += 1
                continue

            lien = extraire_lien(bloc, driver.current_url)
            if not lien:
                ignores_lien += 1
                continue

            produit = Produit(
                nom=nom,
                prix=extraire_prix(bloc),
                note=extraire_note(bloc),
                lien=lien,
            )
            produits.append(produit)

            print(f"✓ {nom[:50]}... | {produit.prix} € | {produit.note}/5")

        except Exception as erreur:
            print(f"✗ Produit ignoré : {erreur}")

    print(
        f"\nTotal extraits : {len(produits)} "
        f"(blocs sans nom : {ignores_nom}, sans lien : {ignores_lien})"
    )
    return produits