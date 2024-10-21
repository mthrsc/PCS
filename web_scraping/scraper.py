from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from var.var import Finales
import tkinter as tk

class Scraper():
        def __init__(self, page2):
            self.page2 = page2
            self.f = Finales()
            
        def pre_query_website(self):
            table = self.page2.table

            while (self.page2.status == "reading" or self.page2.status == "") and not(self.page2.status == "Scan error") and self.page2.break_thread == False:
                 sleep(1)
            
            if "error" in self.page2.status or self.page2.break_thread == True:
                 return

            # Set up Chrome with Selenium
            options = Options()
            options.add_argument('--headless') 
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--enable-javascript")
            options.add_argument("--window-position=-1000,-1000")
            # Download the ChromeDriver if not present on machine
            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver = webdriver.Chrome(options=options)

            for i in range(len(table)):
                pokemon_name = table[i][1].get()
                card_code = table[i][2].get()
                text_box_to_update = table[i][3]

                if self.page2.break_thread == False:
                    if not(card_code == "No code detected"):
                        short_card_code = card_code[:3]
                        if short_card_code[0] == "0":
                            short_card_code = short_card_code[1:]
                    else:
                        short_card_code = ""

                    if self.page2.break_thread == False:
                        result_dict = self.query_website(pokemon_name, short_card_code, driver)
                        if result_dict == {} and self.page2.break_thread == True:
                            driver.quit()
                            return
                        elif result_dict == {}:
                            continue
                        self.update_table(text_box_to_update, result_dict)
                    else:
                        return
                else:
                    driver.quit()
                    return

            driver.quit()
            self.page2.status = "done"


        def query_website(self, pokemon_name, short_card_code, driver):
            url = self.f.CARD_PRICE_URL2 + pokemon_name + self.f.CARD_PRICE_URL2_END
            driver.get(url)

            try:
                element_present = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td.title a"))
                )
            except TimeoutException:
                print("Timed out waiting for page to load")
                return

            # Dictionnary Key: pokemon_name, value: price
            result_dict = {}
            rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-product]")
            for row in rows:
                if self.page2.break_thread == False:
                    # Load all titles of the page and extract its text value
                    title_element = row.find_element(By.CSS_SELECTOR, "td.title a")
                    title = title_element.text.strip()

                    # If we have a card code we filter out the titles that do not show the code 
                    if short_card_code:
                        if pokemon_name in title and short_card_code in title:
                            # Extract the used price
                            price_element = row.find_element(By.CSS_SELECTOR, "td.price.numeric.used_price .js-price")
                            used_price = price_element.text.strip()
                            result_dict[title] = used_price
                    # If we do not have a card code
                    else:
                        if pokemon_name in title:
                            price_element = row.find_element(By.CSS_SELECTOR, "td.price.numeric.used_price .js-price")
                            used_price = price_element.text.strip()
                            result_dict[title] = used_price
                else:
                    result_dict = {}
            return result_dict
        

        def update_table(self, text_box, prices):
            text_box.configure(state="normal")
            for key in prices:
                text_box.insert(tk.END, str(key) + "\n" + prices[key] + "\n\n")  
            text_box.configure(state="disabled")
