import tkinter as tk
from tkinter import *
from .var import Finales
import cv2
import threading
from cv2_enumerate_cameras import enumerate_cameras
from time import sleep

class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self._radioVar = IntVar()
        self._radioVar.set(1)
        f = Finales()
        XpaddingTable = 100
        XpaddingNxtBtn = 800
        YpaddingNxtBtn = 300
        self._controller = controller

        print("logopath: ", f.MAINLOGOPATH)
        img = tk.PhotoImage(file= f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        brwsBtn = tk.Button(self, text='Browse...', width='20', height='1', command = lambda : ...)
        brwsBtn.grid(row = 55, column = 80, padx = 0)

        nextBtn = tk.Button(self, text='Next', width='30', height='1', command = lambda : self.next_button())
        nextBtn.grid(row = 70, column = 80, padx = 0, pady = YpaddingNxtBtn)

    def next_button(self):
        from .page2 import Page2
        self.controller.show_frame(Page2)

    # Add validation on setters !!!!
    @property
    def radioVar(self):
        return self._radioVar.get()

    @radioVar.setter
    def radioVar(self, value):
        self._radioVar.set(value)

    @property
    def controller(self):
        return self._controller

