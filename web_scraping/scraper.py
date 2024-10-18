from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from var.var import Finales

class Scraper():
        def __init__(self, page2):
            self.page2 = page2
            self.f = Finales()
            
        def pre_query_website(self):
            table = self.page2.table

            while self.page2.status == "scanning" and not(self.page2.status == "Scan error"):
                 sleep(1)
            
            if "error" in self.page2.status:
                 return


            # Set up Chrome with Selenium
            options = Options()
            options.add_argument('--headless')  # Run in headless mode if you don't want to see the browser UI
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Automatically download and set up the ChromeDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            for i in range(len(table)):
                pokemon_name = table[i][1].get()
                card_code = table[i][2].get()
                short_card_code = card_code[:3]
                price = self.query_website(pokemon_name, short_card_code, driver)
                print("Finished")


        def query_website(self, pokemon_name, short_card_code, driver):
            url = self.f._CARD_PRICE_URL + pokemon_name + "+" + short_card_code

            driver.get(url)

            return ""