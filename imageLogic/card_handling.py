from io import BytesIO
from .image_modification import Image_modification
from var.var import Finales
import requests
import threading
import re

class Card_handling():
    def __init__(self, page2):
        # imod will prepare the image for the OCR API
        self.imod = Image_modification()
        # Final vars
        self.f = Finales()
        # Page 2 for access to break_thread flag and UI
        self.page2 = page2

    def pre_process_card(self, card_list):
        for idx, file_path in enumerate(card_list):
            # Using thread since each request has its own card to analyse and will update its own part of the table,
            # so no worries about thread safety (That I can think of)
            if self.page2.break_thread == False:
                t = threading.Thread(target = lambda: self.process_card(file_path, idx, self.page2.table), name = "card_process")
                t.start()

    def process_card(self, file_path, idx, table):
        # Resize card to reach 1024kb, the maximum size of the OCR api
        img = self.imod.reach_1024(file_path, self.page2)
        buffer = BytesIO()
        img.save(buffer, 'jpeg')
        buffer.seek(0)

        if self.page2.break_thread == False:
            # Build RQ for OCR api

            # Since we are sending a string of bits, we need to tell the api what type of file it is
            file_ext = self.get_file_type(file_path)

            # API key in the header
            headers = {"apikey": self.f.OCR_API_KEY}

            # Different option related to the API
            data = {
                "filetype": file_ext,
                "isOverlayRequired": "true",
                "detectOrientation": "true",
                "OCREngine": "2"
            }
            # Send RQ
            rs = requests.post(self.f.OCR_RQ_URL, headers=headers, files={'file': buffer}, data=data)

            # The response is a Json format, we need to tell pythn that
            rs = rs.json()

        # Extract name and update table
        if self.page2.break_thread == False:
            pokemon_name = self.get_card_name(rs)
            self.update_table(pokemon_name, idx, table, "name")

        # Extract code and update table
        if self.page2.break_thread == False:
            card_code = self.get_card_code(rs)
            self.update_table(card_code, idx, table, "code")

        # In case both the name and code could not be extracted we print the response for debug
        if not(pokemon_name) and not(card_code):
            print(rs)

    def get_file_type(self, file_path):
        ext = file_path.rsplit(".",1)[-1]
        return ext

    def update_table(self, value, idx, table, update_type):
        if update_type == "name":
            column = 1
            error_message = "Name error"
        elif update_type == "code":
            column = 2
            error_message = "No code detected"

        # Find entry to update in list of lists
        entry = table[idx][column]
        # Enable entry for writing
        entry.configure(state="normal")

        # If we try to pass a value that could not be extracted, we write a error message instead
        try:
            entry.insert(0, value) 
        except:
            entry.insert(0, error_message) 
        # Disable after writing
        entry.configure(state="disabled") 
        
    # Json paths were found after manually analysing the json response.
    def get_card_name(self, rs):
        pokemon_name = rs['ParsedResults'][0]['TextOverlay']['Lines'][1]['LineText']
        return pokemon_name

    # Usually codes are in format xxx/xxx hence the regex to extract them from the response
    # There are exceptions that will get added in future versions of the app.
    def get_card_code(self, rs):
        for line in rs['ParsedResults'][0]['TextOverlay']['Lines']:
            m = re.search(r"^([0-9]{3}/[0-9]{3})\s?([^A-Za-z0-9]?)$", line["LineText"])
            if m:
                return m.group(1)