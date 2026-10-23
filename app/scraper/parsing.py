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
        # Exemple : "4.5 out of 5 stars"
        return float(texte.split()[0].replace(",", "."))
    except (ValueError, IndexError):
        return None


def extraire_produits(driver):
    produits = []

    # Vérifier que la page contient des résultats Amazon
    blocs = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-component-type="s-search-result"]'
    )

    print(f"\nNombre de blocs trouvés : {len(blocs)}")

    if not blocs:
        print("Aucun bloc produit détecté.")
        print("Titre de la page :", driver.title)
        print("URL actuelle :", driver.current_url)

        # Sauvegarder le HTML pour faciliter le diagnostic
        with open("page_amazon.html", "w", encoding="utf-8") as fichier:
            fichier.write(driver.page_source)

        print("Le HTML de la page a été enregistré dans page_amazon.html")
        return produits

    for bloc in blocs:
        try:
            element_nom = bloc.find_element(By.CSS_SELECTOR, "h2 a")
            nom = element_nom.text.strip()

            lien = element_nom.get_attribute("href")
            if lien:
                lien = urljoin(driver.current_url, lien)

            try:
                element_prix = bloc.find_element(
                    By.CSS_SELECTOR,
                    ".a-price .a-offscreen"
                )
                prix = convertir_prix(
                    element_prix.get_attribute("textContent")
                )
            except Exception:
                prix = None

            try:
                element_note = bloc.find_element(
                    By.CSS_SELECTOR,
                    "span.a-icon-alt"
                )
                note = convertir_note(
                    element_note.get_attribute("textContent")
                )
            except Exception:
                note = None

            if nom and lien:
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

        except Exception as erreur:
            print("Erreur lors de l'extraction d'un produit :", erreur)

    print(f"\nTotal des produits extraits : {len(produits)}")

    return produits


