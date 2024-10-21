import threading
from time import sleep
import tkinter as tk
from tkinter import Scrollbar, Canvas, Frame
from var.var import Finales
from imageLogic.card_handling import Card_handling
from .page1 import Page1 as p1
from PIL import ImageTk, Image
from web_scraping.scraper import Scraper

class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        # Call super class
        tk.Frame.__init__(self, parent)
        # We import and create Finales for some static vars
        self._f = Finales()
        # Controller object to call page2 render
        self._controller = controller

        # Card_handling does the OCR (Optical Character Recognition)
        self.reader = Card_handling(self)
        # Scraper will load a website and parse its data
        self.scraper = Scraper(self)

        # Same file_to_scan than page1
        self._files_to_scan = []

        # status for the progress message at the bottom left
        self._status = ""

        # This list will be populater by lists of rows created in create_table()
        # that will result in a list of lists where cells are accessible by their coordinates
        self._table = []

        # Flag to stop threads
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

    def create_table(self):
        # Create a canvas widget
        self.canvas = Canvas(self)
        self.canvas.grid(row=1, column=0, sticky="nsew", columnspan=200)

        # Create a vertical and horizontal scrollbar linked to the canvas
        self.v_scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scroll.grid(row=1, column=1, sticky="ns")
        self.h_scroll = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.grid(row=2, column=0, sticky="ew")

        # Add scrollbars to canvas
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Create a frame inside the canvas to hold the table
        self.table_frame = Frame(self.canvas)

        # Add the table_frame to the canvas
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Configure grid behavior for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Bind an event to resize the canvas scroll region
        self.table_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind mouse scroll to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Table builder START
        # As many rows as we have cards to scan
        self.rows = len(self.files_to_scan)
        # 4 columns: Thumbnail, Name, card code, and prices
        self.columns = 4
        
        # All cells are created and then disabled to prevent user inputs
        for i in range(self.rows):
            # Create a list for the entries that will make the row
            row_entries = []
            for j in range(self.columns):
                if j == 0:
                    # At j == 0 we create a label that will host the thumbnail picture
                    label = tk.Label(self.table_frame, relief="solid")
                    label.grid(row=i+20, column=j, padx=5, pady=5, sticky="ew")  
                    row_entries.append(label)
                elif j == 3:
                    # At j == 3 we use a text widget that we will update with the prices
                    # Since we will need a little bit of formatting, text widget are better than entries or labels
                    text = tk.Text(self.table_frame, width=30, height=15, state="disabled")
                    text.grid(row=i+20, column=j, padx=5, pady=5, sticky="ew")
                    row_entries.append(text)
                else:
                    # Otherwise we use and simple entry which are fine to host a single line of text
                    entry = tk.Entry(self.table_frame, width=30, state="disabled")
                    entry.grid(row=i+20, column=j, padx=5, pady=5, sticky="ew")
                    row_entries.append(entry)
            # We add the list row_entries to the table list, hence creating a list of lists 
            # with a table like structure.
            self.table.append(row_entries)
        # End table builder

    # This method is called from the controller
    def receive_data(self, data):
        # Receive file list from page1
        self.files_to_scan = data
        # Create table
        self.create_table()
        # Create thumbnails and add them to the first column
        self.populate_table_image()
        # Set status to reading for progress label bottom left
        self.status = "reading"
        # Send the table and the files to scan to a method that will spawn a thread per card
        self.reader.pre_process_card(self.files_to_scan)
        
        # Start progress label thread
        label_thread = threading.Thread(target = lambda: self.scan_label_text(self.scan_label), name = "label_update")
        label_thread.start()

        # Start the pricing thread, it will wait for data or be killed if action is cancelled.
        # The reason pricing is within one thread rather than concurent threads (as OCR is) is that we are parsing a website
        # which means that concurent calls will need 'n' concurent selenium driver running, and the website will receive 'n' concurent request
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
            if sum(1 for thread in threading.enumerate() if thread.name.startswith("card_process")) == 0 and self.status == "reading" and self.break_thread == False:
                self.status = "pricing"

            # Update message text
            if self.status == "pricing":
                message = "Getting prices"
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

    # Remove all ui element and clearing the table list of lists
    def destroy_canvas(self):
        self.canvas.destroy()
        self.v_scroll.destroy()
        self.h_scroll.destroy()
        self.table_frame.destroy()
        self.table = []

    # Using the flag break_thread implemented in key parts of the threads, we try to detroy them as fast as possible
    # pricing_thread still take some time though since a parsing action can be long
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
        
