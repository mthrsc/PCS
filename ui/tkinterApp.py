import tkinter as tk
from tkinter import *


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        from .pages import page1
        from .pages import page2
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)

        # Container fill the window
        container.pack(side = "top", fill = "both", expand = True)

        # Set amount of rows and columns
        container.grid_rowconfigure(list(range(2000)), minsize= 1)
        container.grid_columnconfigure(list(range(2000)), minsize= 1)

        # Set window title
        self.title("PCS - Pokemon Card Scanner")
  
        # Dict of frames
        self.frames = {}  

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (page1.Page1, page2.Page2):

            # Creating frame object
            frame = F(container, self)

            # Biding import to object in dict
            self.frames[F] = frame 

            # Set the frame object were it will be on the grid
            # It will start on the top left (0, 0) and expand in 4 directions
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        # We want the app to start on page 1, so we can call it directly
        self.show_frame(page1.Page1)
  
    def show_frame(self, cont, file_to_scan=None):

        # Get frame from dict
        frame = self.frames[cont]
        # Actually display the frame
        frame.tkraise()
        
        # if the frame's class (eg. Page1) has a on_show method, call it
        if hasattr(frame, 'on_show'):
            frame.on_show()
        
        # If the frame's class has a receive_data method, call it with a parameter
        # This is used when passing the file list from page1 to page2
        if file_to_scan and hasattr(frame, 'receive_data'):
            frame.receive_data(file_to_scan)
