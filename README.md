**AMAZON WEB SCRAPING EN PYTHON AVEC SELENIUM**

J'ai conçu une application console capable de rechercher des produits et de 
ramener le nom, le prix, la note et le lien du produit. Les données sont récupérés 
sur le site web d'amazon.

**Technologies utilisées**

La technologie utilisée est python, selenium, SQLite et CSV.
Python pour le langage de programmation, selenium pour automatiser le navigateur
Chrome, SQLite pour la conservation des données récupérées puis sont exporter en 
format CSV

**Fonctionnalités**

- Ouvrir une page de recherche Amazon avec Chrome grâce à Selenium.
-  d'extraire le nom, le prix, la note et le lien des produits affichés.
- Enregistrer les produits dans une base de données SQLite locale.
- Afficher les produits enregistrés dans le terminal.
- Rechercher un produit par une partie de son nom.
- Exporter les données vers un fichier CSV.
- Afficher des statistiques simples sur les produits et les prix disponibles.

**Role des principaux fichiers**
- main.py : Point d'entrée : affiche le menu et traite le choix de l'utilisateur.
- config.py : Centralise les chemins de fichiers et l'URL de recherche.
- app/models/produit.py : Définit le modèle Produit.
- app/models/depot.py : Crée la table SQLite et lit/enregistre les produits.
- app/scraper/driver.py : Configure et démarre Chrome.
- app/scraper/parsing.py : Repère les éléments HTML et extrait les données.
- app/scraper/amazon_scraper.py : Coordonne l'ouverture de la page et l'extraction.
- app/controllers/scraping_controller.py : Relie le menu aux fonctions de scraping, stockage et export.
- app/views/console_view.py : Affiche le menu et les messages dans le terminal.
- app/views/export_view.py : Exporte les produits au format CSV.
- requirements.txt : Liste les dépendances externes du projet.

**Installation**
1. _**Vérifier Python et Chrome**_

Installer Python et Google Chrome si nécessaire. Dans un terminal, vérifier Python :

python --version

Sous certains systèmes, la commande peut être :

python3 --version

2. **_Ouvrir le dossier du projet_**

Dans VS Code, ouvrir le dossier principal amazon_scraper, celui qui contient main.py et config.py.

3. **_Créer un environnement virtuel (recommandé)_**

Sous Windows :

python -m venv .venv
.venv\Scripts\Activate.ps1

Si l'activation PowerShell est bloquée, sélectionner l'interpréteur Python de .venv dans VS Code avec la commande Python: Select Interpreter. Il est également possible d'exécuter directement l'interpréteur de l'environnement virtuel.

4. **_Installer les dépendances_**

Le fichier requirements.txt doit contenir :

selenium>=4.20.0

**_Installer les dépendances :_**

python -m pip install -r requirements.txt

Les versions récentes de Selenium disposent de Selenium Manager pour gérer le pilote du navigateur dans les configurations compatibles. Chrome doit être installé.

Configuration

Dans config.py, l'URL de recherche est définie par la variable SEARCH_URL. Exemple :

SEARCH_URL = "https://www.amazon.com/s?k=ordinateur"

Le chemin de la base de données et celui du CSV sont également configurés dans ce fichier. La structure attendue pour le CSV est :

data/tech/information/data.csv

Le code d'export crée automatiquement les dossiers manquants.

Lancer l'application

Depuis le dossier principal du projet, exécuter :

python main.py


**_Utilisation du menu_**

- Lancer le scraping : ouvre Chrome, visite l'URL configurée et tente d'extraire les résultats accessibles. Les produits trouvés sont enregistrés dans SQLite.
- Afficher les produits récupérés : affiche les produits déjà enregistrés dans la base.
- Rechercher un produit : demande un mot-clé et cherche ce texte dans les noms enregistrés.
- Consulter la base SQLite : dans la version initiale, cette option peut afficher la même liste que l'option 2.
- Exporter les produits en CSV : crée ou remplace data/tech/information/data.csv.
- Afficher les statistiques : affiche le nombre de produits et, si des prix sont disponibles, le prix minimum, le prix maximum et le prix moyen.
- Quitter : termine l'application et ferme la connexion à la base.








