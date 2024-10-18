from time import sleep
import selenium
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
            options.add_argument("--enable-javascript")
            # Automatically download and set up the ChromeDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            for i in range(len(table)):
                pokemon_name = table[i][1].get()
                card_code = table[i][2].get()
                short_card_code = card_code[:3]
                price = self.query_website(pokemon_name, short_card_code, driver)
                print("price: " + price)


        def query_website(self, pokemon_name, short_card_code, driver):
            url = self.f._CARD_PRICE_URL + pokemon_name + "+" + short_card_code

            driver.get(url)
            driver.implicitly_wait(10)  
            print(driver.page_source)
            # Are we on the card page or on the search result page ?
            # <h1 class="H1_PageTitle page-header"> >> search page
            # <div class="page-title-container d-flex align-items-center text-break"> >> card page

            page = ""

            try:
                search_page_element = driver.find_elements("css selector", "h1.H1_PageTitle.page-header")
                print("search_page_element exists!")
                page = "search"
            except selenium.NoSuchElementException:
                print("search_page_element does not exist.")

            # if page == "":
            try:
                card_page_element = driver.find_elements("css selector", "div.page-title-container.d-flex.align-items-center.text-break")
                print("card_page_element exists!")

                page = "card"
            except selenium.NoSuchElementException:
                print("card_page_element does not exist.")


            if page == "":
                 print("Error getting page type")
                 return "error"
            else:
                print("page type: " + page)

            driver.save_screenshot('screenshot.png')

            return ""