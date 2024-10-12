import tkinter as tk
from tkinter import *
import cv2
from .var import Finales


class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        # Importing here to avoid circular import error
        from .page1 import Page1

        tk.Frame.__init__(self, parent)
        self._f = Finales()
        self._controller = controller

        # self.vid = cv2.VideoCapture(g.selectedCamera)
        # if not self.vid.isOpened():
        #     print("Unable to open video source", g.selectedCamera)

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)
        

        backBtn = tk.Button(self, text ="Back", command = lambda : controller.show_frame(Page1))
        backBtn.grid(row = 100, column = 1)

        nextBtn = tk.Button(self, text ="Next", command = lambda : controller.show_frame(Page1))
        nextBtn.grid(row = 100, column = 2)

    def on_show(self):

        # This method is called when Page1 is shown
        print("self.g.selectedCamera: ", self.controller.selectedCamera)
        self.vid = cv2.VideoCapture(self.controller.selectedCamera)
        if not self.vid.isOpened():
            print("Unable to open video source", self.controller.selectedCamera)

    @property
    def f(self):
        return self._f
    @property
    def controller(self):
        return self._controller
