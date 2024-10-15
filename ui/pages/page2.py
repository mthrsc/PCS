import tkinter as tk
from tkinter import Scrollbar, Canvas, Frame
from .var import Finales
from ..imageLogic.card_detection import Card_detection
from .page1 import Page1 as p1
from PIL import ImageTk, Image

class Page2(tk.Frame): 
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self._f = Finales()
        self._controller = controller
        self._cd = Card_detection()

        self._files_to_scan = []

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)


        backBtn = tk.Button(self, text ="Back", command = lambda : controller.show_frame(p1))
        backBtn.grid(row = 100, column = 1)

    def create_table(self):

        # Create a canvas widget
        self.canvas = Canvas(self)
        self.canvas.grid(row=1, column=0, sticky="nsew", columnspan=200)

        # Create a vertical scrollbar linked to the canvas
        self.v_scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scroll.grid(row=1, column=1, sticky="ns")

        # Create a horizontal scrollbar linked to the canvas
        self.h_scroll = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.grid(row=2, column=0, sticky="ew")

        # Configure the canvas to work with scrollbars
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Create a frame inside the canvas to hold the table (cells)
        self.table_frame = Frame(self.canvas)

        # Add the table_frame to the canvas
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Configure grid behavior for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Bind an event to resize the canvas scroll region
        self.table_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind mouse scroll to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows and Linux
        
        #Begin table builder
        print("len: " + str(len(self.files_to_scan)))
        self.rows = len(self.files_to_scan)
        self.columns = 4

        # Store the Entry widgets in a list of lists (table structure)
        self.table = []

        # Create the table layout
        for i in range(self.rows):
            row_entries = []
            for j in range(self.columns):
                if j == 0:
                    label = tk.Label(self.table_frame, relief="solid")
                    label.grid(row=i+20, column=j, padx=5, pady=5, sticky="nsew")  
                    row_entries.append(label)
                else:
                    entry = tk.Entry(self.table_frame, width=30, state="disabled")
                    entry.grid(row=i+20, column=j, padx=5, pady=5, sticky="nsew")
                    row_entries.append(entry)
            self.table.append(row_entries)
        # End table builder



    def on_show(self):
        ...
        #Create table
        #Show card on page

        #Resize card
        #Build RQ
        #Analyse RS
        #ParsedResults[0].Overlay.Lines[1].LineText
        #ParsedResults[0].Overlay.Lines[8].LineText
        #Crawl

    def receive_data(self, data):
        # This method will be called when data is passed from Page1
        self.files_to_scan = data
        # print(self.files_to_scan)
        self.create_table()
        self.populate_table_image()


    def populate_table_image(self):
        for idx, file in enumerate(self.files_to_scan):
            img = Image.open(file)
            img = img.resize((300, 400))
            img = ImageTk.PhotoImage(img)
            self.table[idx][0].config(image=img)
            self.table[idx][0].image=img


        # Update the content of a specific cell. For example: Row 2, Column 3 (index 1, 2).
        # self.table[1][2].delete(0, tk.END)  # Clear the cell
        # self.table[1][2].insert(0, "Updated")  # Insert new content

        # self.table[1][1].delete(0, tk.END)  # Clear the cell
        # self.table[1][1].insert(0, "Updated")  # Insert new content

    
    def _on_mousewheel(self, event):
        if event.num == 4:  # Scroll up on macOS (Button-4)
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down on macOS (Button-5)
            self.canvas.yview_scroll(1, "units")
        else:  # For Windows and Linux
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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
    def files_to_scan(self):
        return self._files_to_scan

    @files_to_scan.setter
    def files_to_scan(self, value):
        self._files_to_scan = value
