import tkinter as tk
from tkinter import *


class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        from .pages import page1
        from .pages import page2
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(list(range(2000)), minsize= 1)
        container.grid_columnconfigure(list(range(2000)), minsize= 1)

        # Set window title
        self.title("PCS - Pokemon Card Scanner")
  
        # initializing frames to an empty array
        self.frames = {}  

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (page1.Page1, page2.Page2):                   # <<<<< UPDATE THIS WITH NEW PAGES (and import them) !!!! eg. for F in (Page1, Page2, Page3....):
            # print("F: ",F)

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(page1.Page1)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont, data=None):
        frame = self.frames[cont]
        frame.tkraise()

        if data and hasattr(frame, 'receive_data'):
            frame.receive_data(data)

        if hasattr(frame, 'on_show'):
            frame.on_show()