from io import BytesIO
from .image_modification import Image_modification
from .card_detection import Card_detection
from ..pages.var import Finales
import requests
import tkinter as tk

class Card_handling():
    def __init__(self):
        self.imod = Image_modification()
        self.card_dect = Card_detection()
        self.f = Finales()



    def pre_process_card(self, card_list, table):
        print("card_list: ", card_list)

        for idx, file_path in enumerate(card_list):
            print("file path: " + str(file_path))
            #Add thread here !
            self.process_card(file_path, idx, table)

    def process_card(self, file_path, idx, table):
        #Resize card
        img = self.imod.reach_1024(file_path)
        buffer = BytesIO()
        img.save(buffer, 'jpeg')
        buffer.seek(0)

        file_ext = self.get_file_type(file_path)

        headers = {"apikey": self.f.OCR_API_KEY}
        data = {
            "filetype": file_ext,
            "isOverlayRequired": "true",
            "detectOrientation": "true",
            "OCREngine": "2"
        }
        rs = requests.post(self.f.OCR_RQ_URL, headers=headers, files={'file': buffer}, data=data)
        # print(rs.text)
        rs = rs.json()
        pokemon_name = rs['ParsedResults'][0]['TextOverlay']['Lines'][1]['LineText']
        print(pokemon_name)
        self.update_table(pokemon_name, idx, table)

        #Build RQ
        #Analyse RS
        #ParsedResults[0].Overlay.Lines[1].LineText
        #ParsedResults[0].Overlay.Lines[8].LineText
        #Crawl

    def get_file_type(self, file_path):
        ext = file_path.rsplit(".",1)[-1]
        return ext
    
    def update_table(self, pokemon_name, idx, table):
        print(table)
        entry = table[idx][1]
        entry.configure(state="normal")
        entry.delete(0, tk.END)  # Clear any existing text in the Entry
        entry.insert(0, pokemon_name)  # Insert the new text
        entry.configure(state="disabled")  # Optionally set it back to disabled