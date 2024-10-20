from io import BytesIO
from time import sleep
from .image_modification import Image_modification
from var.var import Finales
import requests
import tkinter as tk
import threading
import re

class Card_handling():
    def __init__(self):
        self.imod = Image_modification()
        self.f = Finales()

    def pre_process_card(self, card_list, table):
        for idx, file_path in enumerate(card_list):
            # Using thread since each request has its own card to anlyse and will update its own part of the table,
            # so no worries about thread safety
            t = threading.Thread(target = lambda: self.process_card(file_path, idx, table), name = "card_process")
            t.start()

    def process_card(self, file_path, idx, table):
        #Resize card
        img = self.imod.reach_1024(file_path)
        buffer = BytesIO()
        img.save(buffer, 'jpeg')
        buffer.seek(0)

        #Build RQ
        file_ext = self.get_file_type(file_path)

        headers = {"apikey": self.f.OCR_API_KEY}
        data = {
            "filetype": file_ext,
            "isOverlayRequired": "true",
            "detectOrientation": "true",
            "OCREngine": "2"
        }
        #Send RQ
        rs = requests.post(self.f.OCR_RQ_URL, headers=headers, files={'file': buffer}, data=data)

        #Analyse RS / Update name
        rs = rs.json()

        #Add exception or unreadable name handling
        pokemon_name = self.get_card_name(rs)
        self.update_table(pokemon_name, idx, table, "name")
        print(pokemon_name)

        #Analyse RS / Update code
        #Add exception or unreadable code handling
        card_code = self.get_card_code(rs)
        print("card_code: ", card_code)
        self.update_table(card_code, idx, table, "code")

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

        entry = table[idx][column]
        entry.configure(state="normal")

        try:
            entry.insert(0, value)  # Insert the new text
        except:
            entry.insert(0, error_message)  # Insert the new text

        entry.configure(state="disabled")  # Optionally set it back to disabled
        

    def get_card_name(self, rs):
        pokemon_name = rs['ParsedResults'][0]['TextOverlay']['Lines'][1]['LineText']
        return pokemon_name


    def get_card_code(self, rs):
        for line in rs['ParsedResults'][0]['TextOverlay']['Lines']:
            m = re.search(r"^([0-9]{3}/[0-9]{3})\s?([^A-Za-z0-9]?)$", line["LineText"])
            if m:
                return m.group(1)