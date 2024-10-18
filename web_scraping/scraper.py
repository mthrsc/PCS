from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

            while self.page2.status == "reading" or self.page2.status == "" and not(self.page2.status == "Scan error"):
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
            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver = webdriver.Chrome(options=options)

            for i in range(len(table)):
                print("i: ", i)
                pokemon_name = table[i][1].get()
                card_code = table[i][2].get()
                text_box_to_update = table[i][3]
                short_card_code = card_code[:3]
                if short_card_code[0] == "0":
                    short_card_code = short_card_code[1:]

                result_dict = self.query_website(pokemon_name, short_card_code, driver)
                print("result_dict: ", result_dict)
                self.update_table(text_box_to_update, result_dict)

            driver.quit()
            self.page2.status = "done"


        def query_website(self, pokemon_name, short_card_code, driver):
            url = self.f.CARD_PRICE_URL2 + pokemon_name + self.f.CARD_PRICE_URL2_END
            driver.get(url)
            driver.minimize_window()
            driver.set_window_position(-10000, 0)  # Move the window out of the visible screen area

            try:
                element_present = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td.title a"))
                )
            except TimeoutException:
                print("Timed out waiting for page to load")
                return
            
            result_dict = {}
            rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-product]")
            for row in rows:
                # Extract the title
                title_element = row.find_element(By.CSS_SELECTOR, "td.title a")
                title = title_element.text.strip()  
                if pokemon_name in title and short_card_code in title:
                    print(title)
            
                    # Extract the used price
                    price_element = row.find_element(By.CSS_SELECTOR, "td.price.numeric.used_price .js-price")
                    used_price = price_element.text.strip()  # Get the text and strip any whitespace

                    # Store the title and used price in the dictionary
                    result_dict[title] = used_price


            return result_dict
        
        def update_table(self, text_box, prices):
            text_box.configure(state="normal")
            print("prices: ", prices)
            for key in prices:
                print("key: ", key)
                message = str(key) + ": " + prices[key]
                text_box.insert(tk.END, str(key) + "\n" + prices[key] + "\n\n")  
                # text_box.config(text=message)  
                # entry.insert(0, message)  # Insert the new text
                # entry.insert(0, "\n")

            text_box.configure(state="disabled")  # Optionally set it back to disabled
