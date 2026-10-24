from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import BASE_DIR


def creer_driver():
    options = Options()

    # Navigateur visible (le headless est plus souvent bloqué par Amazon)
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1366,900")

    # Langue française
    options.add_argument("--lang=fr-FR")
    options.add_experimental_option(
        "prefs", {"intl.accept_languages": "fr-FR,fr"}
    )

    # Réduit les signaux d'automatisation les plus évidents
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Profil Chrome dédié : garde les cookies entre deux lancements
    # (si tu résous un CAPTCHA une fois, Amazon s'en souvient)
    options.add_argument(f"--user-data-dir={BASE_DIR / 'chrome_profile'}")

    # PAS de user-agent forcé : celui de ton vrai Chrome est le plus crédible
    return webdriver.Chrome(options=options)