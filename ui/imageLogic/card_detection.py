
import cv2
import numpy as np

class Card_detection():
    def __init__(self):
        self._card_detected = False


    def read_card(self):
        ...

    @property
    def card_detected(self):
        return self._card_detected
    @card_detected.setter
    def card_detected(self, value):
        self._card_detected = value
