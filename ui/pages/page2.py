import tkinter as tk
import cv2
from .var import Finales
from ..vision.card_detection import Card_detection

class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        # Importing here to avoid circular import error
        from .page1 import Page1

        tk.Frame.__init__(self, parent)
        self._f = Finales()
        self._controller = controller
        self._cd = Card_detection()

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        # Add cv2 release of video feed - self.vid.release()
        backBtn = tk.Button(self, text ="Back", command = lambda : controller.show_frame(Page1))
        backBtn.grid(row = 100, column = 1)

        # nextBtn = tk.Button(self, text ="Next", command = lambda : controller.show_frame(Page1))
        # nextBtn.grid(row = 100, column = 2)

    def on_show(self):
        ...

    @property
    def f(self):
        return self._f
    @property
    def controller(self):
        return self._controller

    @property
    def cd(self):
        return self._cd
    @cd.setter
    def cd(self, value):
        self._cd = value
