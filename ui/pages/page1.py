import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from .var import Finales
from cv2_enumerate_cameras import enumerate_cameras
from time import sleep

class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self._radioVar = IntVar()
        self._radioVar.set(1)
        self._f = Finales()
        self._controller = controller

        self._filetypes = ("gif", "png", "jpg", "jpeg", "tiff", "bmp")

        self._files_to_scan = []

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        paddingLabel1 = Label(self, text = "")
        paddingLabel1.grid(row = 25, column = 1, pady = 200, columnspan = 20)

        brwsBtn = tk.Button(self, text='Browse...', width='20', height='1', command = lambda : self.browse_window())
        brwsBtn.grid(row = 25, column = 20, padx = 50, pady = 0)

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

        paddingLabel2 = Label(self, text = "")
        paddingLabel2.grid(row = 69, column = 80, pady = 20, columnspan = 1)

        nextBtn = tk.Button(self, text='Next', width='30', height='1', command = lambda : self.next_button())
        nextBtn.grid(row = 70, column = 80, padx = 0, pady = 0)

    def next_button(self):
        from .page2 import Page2
        self.controller.frames[Page2].receive_data(self.files_to_scan)
        self.controller.show_frame(Page2)

    def browse_window(self):
        files = filedialog.askopenfilenames()
        if len(files) > 0:
            validated_files = self.validate_files(files)
            self.show_filenames(validated_files)

    def validate_files(self, files):
        result = {}
        for file in files:
            ext = file.rsplit(".",1)[-1]
            if ext in self.filetypes:
                result[file] = "ok"
            else:
                result[file] = "nok"
        return result
    
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

    @property
    def filetypes(self):
        return self._filetypes

    @filetypes.setter
    def filetypes(self, value):
        self._filetypes.set(value)

    @property
    def files_to_scan(self):
        return self._files_to_scan

    @files_to_scan.setter
    def files_to_scan(self, value):
        self._files_to_scan.set(value)

    @property
    def file_text_box(self):
        return self._file_text_box

    @file_text_box.setter
    def file_text_box(self, value):
        self._file_text_box.set(value)

    @property
    def f(self):
        return self._f
    @property
    def controller(self):
        return self._controller
