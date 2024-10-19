import threading
from time import sleep
import tkinter as tk
from tkinter import Scrollbar, Canvas, Frame
from var.var import Finales
from imageLogic.card_handling import Card_handling
from .page1 import Page1 as p1
from PIL import ImageTk, Image

class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        from web_scraping.scraper import Scraper

        tk.Frame.__init__(self, parent)
        self._f = Finales()
        self._controller = controller
        self.reader = Card_handling()
        self.scraper = Scraper(self)

        self._files_to_scan = []
        self._status = ""
        # Store the Entry widgets in a list of lists (table structure)
        self._table = []

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        backBtn = tk.Button(self, text ="Back", command = lambda : controller.show_frame(p1))
        backBtn.grid(row = 150, column = 1)

        self._scan_label = tk.Label(self, text = "Scanning")
        self._scan_label.grid(row=150, column=0, padx=5, pady=5, sticky="w")  



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
        self.rows = len(self.files_to_scan)
        self.columns = 4
        
        # Create the table layout
        for i in range(self.rows):
            row_entries = []
            for j in range(self.columns):
                if j == 0:
                    label = tk.Label(self.table_frame, relief="solid")
                    label.grid(row=i+20, column=j, padx=5, pady=5, sticky="ew")  
                    row_entries.append(label)
                elif j == 3:
                    text = tk.Text(self.table_frame, width=30, height=15, state="disabled")
                    text.grid(row=i+20, column=j, padx=5, pady=5, sticky="ew")
                    row_entries.append(text)
                else:
                    entry = tk.Entry(self.table_frame, width=30, state="disabled")
                    entry.grid(row=i+20, column=j, padx=5, pady=5, sticky="ew")
                    row_entries.append(entry)
            self.table.append(row_entries)
        # End table builder

    def on_show(self):
        ...

    def receive_data(self, data):
        # This method will be called when data is passed from Page1
        self.files_to_scan = data
        #Create table
        #Show card on page
        self.create_table()
        self.populate_table_image()

        self.status = "reading"
        self.reader.pre_process_card(self.files_to_scan, self.table)
        
        t1 = threading.Thread(target = lambda: self.scan_label_text(self.scan_label), name = "label_update")
        t1.start()

        pricing_thread = threading.Thread(target = lambda: self.scraper.pre_query_website(), name = "pricing_thread")
        pricing_thread.start()


    def populate_table_image(self):
        for idx, file in enumerate(self.files_to_scan):
            img = Image.open(file)
            img = img.resize((150, 200))
            img = ImageTk.PhotoImage(img)
            self.table[idx][0].config(image=img)
            self.table[idx][0].image=img
 
    def _on_mousewheel(self, event):
        if event.num == 4:  
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: 
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def scan_label_text(self, scan_label):
        i = 1
        message = "Scanning"
        dots = ""
        while self.status == "reading" or self.status == "pricing":
            print(self.status)
            dots = dots + "."
            scan_label.config(text = str(message + dots))
            i = i + 1
            if i == 4:
                i = 1
                dots = ""
            sleep(1)

            #Are threads still running ?
            if sum(1 for thread in threading.enumerate() if thread.name.startswith("card_process")) == 0 and self.status == "reading":
                self.status = "pricing"

            

            # Update message
            if self.status == "pricing":
                message = "Getting prices"
            elif self.status == "done_error":
                scan_label.config(text = "Scan complete with errors")
            elif self.status == "error":
                scan_label.config(text = "Scan error")
            elif self.status == "done":
                scan_label.config(text = "Scan complete")



    @property
    def f(self):
        return self._f
    @property
    def controller(self):
        return self._controller

    @property
    def files_to_scan(self):
        return self._files_to_scan

    @files_to_scan.setter
    def files_to_scan(self, value):
        self._files_to_scan = value

    @property
    def scan_label(self):
        return self._scan_label

    @scan_label.setter
    def scan_label(self, value):
        self._scan_label = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        print(f"Setting status to: {value}")  # Debugging line
        self._status = value

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        self._table = value
