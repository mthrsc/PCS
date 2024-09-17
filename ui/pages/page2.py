import tkinter as tk
from tkinter import *
from .var import Finales
from .var import Globals


class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        # Importing here to avoid circular inport error
        from .page1 import Page1

        tk.Frame.__init__(self, parent)
        var = Finales()




        label = tk.Label(self, text ="Page 2", font = var.LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        

        # button to show frame 2 with text
        # layout2
        button1 = tk.Button(self, text ="Page 1", command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by 
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        # button2 = tk.Button(self, text ="Startpage", command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        # button2.grid(row = 2, column = 1, padx = 10, pady = 10)