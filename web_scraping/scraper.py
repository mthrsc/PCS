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
            # We import and create page2 because we will need access to UI elements and break_thread flag
            self.page2 = page2
            # We import and create Finales for some static vars
            self.f = Finales()
            
        def pre_query_website(self):
            table = self.page2.table

            # Thread sleeps until the status on page2 has changed
            while (self.page2.status == "reading" or self.page2.status == "") and not(self.page2.status == "Scan error") and self.page2.break_thread == False:
                 sleep(1)
            
            # The method will stop of if needed
            if "error" in self.page2.status or self.page2.break_thread == True:
                 return

            # Creating the selenium driver using chrome
            options = Options()
            options.add_argument('--headless') 
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--enable-javascript")
            options.add_argument("--window-position=-1000,-1000")
            # Download the ChromeDriver if not present on machine
            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Or just use the one already present
            driver = webdriver.Chrome(options=options)

            for i in range(len(table)):
                # Get name and code from table text
                pokemon_name = table[i][1].get()
                card_code = table[i][2].get()
                # Text box to update
                text_box_to_update = table[i][3]

                # If pokemon name could not be found, there is no point going forward
                if pokemon_name == "Name error":
                    result_dict["Error"] = ""
                    self.update_table(text_box_to_update, result_dict)
                    return

                if self.page2.break_thread == False:
                    if not(card_code == "No code detected"):
                        # This website actually uses only the first 3 digits of the card code
                        short_card_code = card_code[:3]
                        # and zeros are removed
                        if short_card_code[0] == "0":
                            short_card_code = short_card_code[1:]
                    else:
                        short_card_code = ""

                    # Use name and code to parse data from website
                    if self.page2.break_thread == False:
                        result_dict = self.query_website(pokemon_name, short_card_code, driver)
                        if result_dict == {} and self.page2.break_thread == True:
                            # Here we need to kill the thread
                            driver.quit()
                            return
                        elif result_dict == {}:
                            # Here the parsing failed
                            result_dict["Error"] = ""
                            self.update_table(text_box_to_update, result_dict)
                        # here all went fine
                        self.update_table(text_box_to_update, result_dict)
                    else:
                        driver.quit()
                        return
                else:
                    driver.quit()
                    return

            # End of loop, quit drive and update status
            driver.quit()
            self.page2.status = "done"


        def query_website(self, pokemon_name, short_card_code, driver):
            # Build url
            url = self.f.CARD_PRICE_URL2 + pokemon_name + self.f.CARD_PRICE_URL2_END
            # Send driver to parse url html code
            driver.get(url)

            # Wait for page to load, return empty dict if timeout
            try:
                element_present = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "td.title a"))
                )
            except TimeoutException:
                return {}

            # Dictionnary Key: pokemon_name, value: price
            result_dict = {}
            rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-product]")
            for row in rows:
                if self.page2.break_thread == False:
                    # Load all titles of the page and extract their text value
                    title_element = row.find_element(By.CSS_SELECTOR, "td.title a")
                    title = title_element.text.strip()

                    # If we have a card code we filter out the prices that do not have the code 
                    if not(short_card_code == ""):
                        if pokemon_name in title and short_card_code in title:
                            # Extract the used price
                            price_element = row.find_element(By.CSS_SELECTOR, "td.price.numeric.used_price .js-price")
                            used_price = price_element.text.strip()
                            result_dict[title] = used_price
                    # If we do not have a card code, we use all prices that have the pokemon name
                    else:
                        if pokemon_name in title:
                            price_element = row.find_element(By.CSS_SELECTOR, "td.price.numeric.used_price .js-price")
                            used_price = price_element.text.strip()
                            result_dict[title] = used_price
                else:
                    result_dict = {}
            return result_dict
        
        # Update table 
        def update_table(self, text_box, prices):
            text_box.configure(state="normal")
            for key in prices:
                text_box.insert(tk.END, str(key) + "\n" + prices[key] + "\n\n")  
            text_box.configure(state="disabled")
