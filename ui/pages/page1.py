import tkinter as tk
from tkinter import *
from tkinter import filedialog
from var.var import Finales

class Page1(tk.Frame):
    
    def __init__(self, parent, controller):
        # Call super class
        tk.Frame.__init__(self, parent)
        # We import and create Finales for some static vars
        self._f = Finales()
        # Controller object to call page2 render
        self._controller = controller

        # File types accepter by the app
        self._filetypes = ("gif", "png", "jpg", "jpeg", "tiff", "bmp")
        
        # List of files to scan
        self._files_to_scan = []

        # Main logo creation and position
        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        # Empty label used as padding for page layout
        paddingLabel1 = Label(self, text = "")
        paddingLabel1.grid(row = 25, column = 1, pady = 200, columnspan = 20)

        #Browse button creation, position and listener
        brwsBtn = tk.Button(self, text='Browse...', width='20', height='1', command = lambda : self.browse_window())
        brwsBtn.grid(row = 25, column = 20, padx = 50, pady = 0)

        # Text box with scrollbar START
        # Create a Frame to hold the Text and Scrollbar
        file_frame = tk.Frame(self)
        file_frame.grid(row=25, column=50, padx=0, pady=0, sticky="w") 

        # Create a Scrollbar widget
        scrollbar = tk.Scrollbar(file_frame)
        scrollbar.pack(side="right", fill="y")

        # Create a Text widget
        self._file_text_box = tk.Text(file_frame, wrap="word", yscrollcommand=scrollbar.set, height=10, width=50, state=DISABLED)
        self._file_text_box.pack(side="left", fill="both", expand=True)

        # Configure the Scrollbar to work with the Text widget
        scrollbar.config(command=self.file_text_box.yview)
        # Text box with scrollbar END

        # Empty label used as padding for page layout
        paddingLabel2 = Label(self, text = "")
        paddingLabel2.grid(row = 69, column = 80, pady = 20, columnspan = 1)

        #Next button creation, position and listener
        nextBtn = tk.Button(self, text='Next', width='30', height='1', command = lambda : self.next_button())
        nextBtn.grid(row = 70, column = 80, padx = 0, pady = 0)

    def next_button(self):
        from .page2 import Page2
        # Verifying that the list of files is not empty before moving on to the next page.
        if not(self.files_to_scan == []):
            self.controller.frames[Page2].receive_data(self.files_to_scan)
            self.controller.show_frame(Page2)

    # Explorer view
    def browse_window(self):
        files = filedialog.askopenfilenames()
        if len(files) > 0:
            validated_files = self.validate_files(files)
            self.show_filenames(validated_files)

    # Validating file format
    def validate_files(self, files):
        result = {}
        for file in files:
            ext = file.rsplit(".",1)[-1]
            if ext in self.filetypes:
                result[file] = "ok"
            else:
                result[file] = "nok"
        return result
    
    # Displaying files in text box
    def show_filenames(self, validated_files):
        if len(validated_files) > 0:
            self.file_text_box.configure(state="normal")
            for key in validated_files:
                if validated_files[key] == "ok":
                    self.file_text_box.insert(tk.END, key)
                    self.file_text_box.insert(tk.END, "\n\n")
                    self.files_to_scan.append(key)
                else:
                    message = key + " - Invalid file format"
                    self.file_text_box.insert(tk.END, message)
                    self.file_text_box.insert(tk.END, "\n\n")
            self.file_text_box.configure(state="disabled")

    # Called from the controller, 
    # here we clear both the text box and file_to_scan to start a new scan session
    def on_show(self):
        # Clear the text box when the page is shown
        self.file_text_box.configure(state="normal")
        self.file_text_box.delete("1.0", tk.END)
        self.file_text_box.configure(state="disabled")
        # Reset the files_to_scan list
        self._files_to_scan = []

    # No setter for controller
    @property
    def controller(self):
        return self._controller

    # No setter for tuple filetypes    
    @property
    def filetypes(self):
        return self._filetypes

    @property
    def files_to_scan(self):
        return self._files_to_scan

    @files_to_scan.setter
    def files_to_scan(self, value):
        if not isinstance(value, list):
            raise ValueError("files_to_scan must be a list.")
        self._files_to_scan = value

    @property
    def file_text_box(self):
        return self._file_text_box

    @property
    def f(self):
        return self._f