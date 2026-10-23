from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def creer_driver():
    options = Options()

    # le navigateur sera visible quand on fera le scraping
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver
