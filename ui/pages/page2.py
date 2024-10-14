import tkinter as tk
from .var import Finales
from ..vision.card_detection import Card_detection
from .page1 import Page1 as p1

class Page2(tk.Frame): 
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self._f = Finales()
        self._controller = controller
        self._cd = Card_detection()

        self._file_to_scan = []

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

    def receive_data(self, data):
        # This method will be called when data is passed from Page1
        self.file_list = data
        
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

    @property
    def file_to_scan(self):
        return self._file_to_scan

    @file_to_scan.setter
    def file_to_scan(self, value):
        self._file_to_scan.set(value)
