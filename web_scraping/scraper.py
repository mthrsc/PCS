from var.var import Finales
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Scraper():
    def __init__(self):
        self.f = Finales()


    def query_website(self, pokemon_name, card_code):
        short_card_code = card_code[:3]
        url = self.f.SCRAP_ADDRESS + pokemon_name + "+" + short_card_code

        rs = requests.get(url)

        print(rs.content)

        if rs.status_code == 200:
            # Parse the page content
            soup = BeautifulSoup(rs.content, 'html.parser')

            # Are we on the card page or on the search result page ?
            # <h1 class="H1_PageTitle page-header"> >> search page
            # <div class="page-title-container d-flex align-items-center text-break"> >> card page

            detect_card_page = soup.find_all('div', class_='page-title-container d-flex align-items-center text-break')
            detect_search_page = soup.find_all('h1', class_='H1_PageTitle page-header')
            if len(detect_card_page) > 0:
                # We are on a card page
                price_list = []
                finished = False

                divs = soup.find_all('div', class_='col-offer col-auto')

                for div in divs:
                    raw_price = soup.find('span', class_="color-primary small text-end text-nowrap fw-bold ")
                    print(raw_price)

            elif len(detect_search_page) > 0:
                # We are on search result page
                ...
            else:
                #error
                print("Parsing error")