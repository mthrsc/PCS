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
        self.reader = Card_handling(self)
        self.scraper = Scraper(self)

        self._files_to_scan = []
        self._status = ""
        # Store the Entry widgets in a list of lists (table structure)
        self._table = []

        self._break_thread = False

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        backBtn = tk.Button(self, text ="Back", command = lambda : self.back_button())
        backBtn.grid(row = 150, column = 1)

        self._scan_label = tk.Label(self, text = "Scanning")
        self._scan_label.grid(row=150, column=0, padx=5, pady=5, sticky="w")  

        t1 = threading.Thread(target = lambda: self.scan_label_text(self.scan_label), name = "scan_label_text")
        t1.start()

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
        # The reason pricing is within one thread rather than concurent threads (as OCR is) is that we are parsing a website
        # which means that concurent calls will need n concurent selenium driver running, and the website will receive n concurent request
        # For both ethic and resource reasons I decided to parse the prices sequentially.
        pricing_thread = threading.Thread(target = lambda: self.scraper.pre_query_website(), name = "pricing_thread")
        pricing_thread.start()

    # Adding a small version of the picture in the first column of the table
    def populate_table_image(self):
        for idx, file in enumerate(self.files_to_scan):
            img = Image.open(file)
            img = img.resize((150, 200))
            img = ImageTk.PhotoImage(img)
            self.table[idx][0].config(image=img)
            self.table[idx][0].image=img
 
    # Mouse wheel listener for the table
    def _on_mousewheel(self, event):
        if event.num == 4:  
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: 
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Loop adding the message and three dots at the bottom left of the screen
    def scan_label_text(self, scan_label):
        i = 1
        message = "Scanning"
        dots = ""
        while (self.status == "reading" or self.status == "pricing") and self.break_thread == False:
            dots = dots + "."
            scan_label.config(text = str(message + dots))
            i = i + 1
            if i == 4:
                i = 1
                dots = ""
            sleep(1)

            # If card_process is finished running, we move on to pricing
            if sum(1 for thread in threading.enumerate() if thread.name.startswith("card_process")) == 0 and self.status == "reading":
                self.status = "pricing"

            # Update message text
            if self.status == "pricing":
                message = "Getting prices"
            elif self.status == "done_error":
                scan_label.config(text = "Scan complete with errors")
            elif self.status == "error":
                scan_label.config(text = "Scan error")
            elif self.status == "done":
                scan_label.config(text = "Scan complete")

    def back_button(self):
        # Gracefully destroying running threads
        self.destroy_threads()
        
        # We destroy the canvas is case the user navigate back to Page1
        # and add new cards to scan. It is faster than clearing each cell one by one.
        self.destroy_canvas()

        # Calling page1
        self.controller.show_frame(p1)

    def destroy_canvas(self):
        self.canvas.destroy()
        self.v_scroll.destroy()
        self.h_scroll.destroy()
        self.table_frame.destroy()
        self.table = []

    def destroy_threads(self):
        self.break_thread = True
        for thread in threading.enumerate():
            if thread.name.startswith("label_update") or thread.name.startswith("pricing_thread") or thread.name.startswith("card_process"):
                thread.join()
        self.break_thread = False

    # No setter needed for Final class object
    @property
    def f(self):
        return self._f
    
    # No setter needed for controller
    @property
    def controller(self):
        return self._controller

    @property
    def files_to_scan(self):
        return self._files_to_scan

    @files_to_scan.setter
    def files_to_scan(self, value):
        if not isinstance(value, list):
            raise ValueError("files_to_scan must be a list.")
        self._files_to_scan = value

    # No setter needed for label object
    @property
    def scan_label(self):
        return self._scan_label

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        self._table = value

    @property
    def break_thread(self):
        return self._break_thread

    @break_thread.setter
    def break_thread(self, value):
        if not(isinstance(value, bool)):
            raise ValueError("break_thread must be a boolean")
        self._break_thread = value
        
