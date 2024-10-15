from .image_modification import Image_modification
from .card_detection import Card_detection


class Card_handling():
    def __init__(self):
        self.imod = Image_modification()
        self.card_dect = Card_detection()


    def pre_process_card(self, card_list, table):
        print("card_list: ", card_list)

        for idx, file_path in enumerate(card_list):
            print("file path: " + str(file_path))
            self.process_card(file_path, idx, table)



    def process_card(self, file_path, idx, table):
        img = self.imod.reach_1024(file_path)