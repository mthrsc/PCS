import tkinter as tk
from tkinter import *
from .page2 import Page2
from .var import Finales
from .var import Globals
import cv2
import threading
from cv2_enumerate_cameras import enumerate_cameras
from time import sleep

class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self._cameraDetected = "detecting"
        self._available_cameras = set()
        self._radioVar = IntVar()
        self._radioVar.set(1)
        f = Finales()
        g = Globals()

        print("logopath: ", f.MAINLOGOPATH)
        img = tk.PhotoImage(file= f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 99, rowspan = 5)

        label = tk.Label(self, text ="Searching for cameras", font = f.NORMALFONT)
        label.grid(row = 50, column = 0, padx = 20, pady = 50, columnspan=55, sticky='NW')

        button2 = tk.Button(self, text='Next', width='30', height='1', command = lambda : self.next_button(g))
        button2.grid(row = 70, column = 30, padx = 0, pady = 0, columnspan = 10)

        t1 = threading.Thread(target = lambda: self.label_text(label), name = "camera_message")
        t1.start()

        t2 = threading.Thread(target = lambda: self.detect_cameras(label), name = "camera_detector")
        t2.start()

        t3 = threading.Thread(target = lambda: self.list_camera(), name = "camera_list")
        t3.start()


    def label_text(self, label):
        i = 1
        while self.cameraDetected == "detecting":
            message = "Searching for cameras"
            x = 0
            while x < i:
                message = message + "."
                x = x + 1
            label.config(text = message)
            i = i + 1
            if i == 4:
                i = 1
            sleep(1)
  

    def detect_cameras(self, label):
        
        for camera_info in enumerate_cameras():
            self.available_cameras.add((camera_info.index, camera_info.name))
            print(f'{camera_info.index}: {camera_info.name} - {camera_info.pid} - {camera_info.vid} - {camera_info.index} - {camera_info.path}')

        # print("set: ", self.available_cameras)

        if len(self.available_cameras) > 0:
            self.cameraDetected = "detected"
            label.config(text = "Select camera:")
        else:
            self.cameraDetected = "error"
            label.config(text = "Cannot find cameras")


    def list_camera(self):
        done = False
        values = {}

        while not(done):
            if len(self.available_cameras) > 0 and self.cameraDetected == "detected":
                for i, item in enumerate(self.available_cameras):
                    count = i + 1
                    # values.update("RadioButton" + str(count), item[0])
                    values["RadioButton" + str(count)] = item[0]
                
                for i, (text, value) in enumerate(values.items()):
                    button = Radiobutton(self, text = (str(text) + " - " + str(value)), variable=self._radioVar, value=value)
                    button.grid(row = (51 + i), column = 0, padx = 20, pady = 0, columnspan=550, sticky='NW')
                done = True
            elif self.cameraDetected == "error":
                done = True

        # label = tk.Label(self, text ="Searching for cameras", font = f.NORMALFONT)
        # label.grid(row = 50, column = 0, padx = 20, pady = 50, columnspan=55, sticky='NW')

    def next_button(self, g):
        g.selectedCamera = self.radioVar
        # g.selectedCamera(self.radioVar)
        print(g.selectedCamera)

        # controller.show_frame(Page2)

    # Add validation on setters !!!!
    @property
    def cameraDetected(self):
        return self._cameraDetected

    @cameraDetected.setter
    def cameraDetected(self, value):
        self._cameraDetected = value

    @property
    def available_cameras(self):
        return self._available_cameras

    @available_cameras.setter
    def available_cameras(self, value):
        self._available_cameras = value

    @property
    def radioVar(self):
        return self._radioVar.get()

    @radioVar.setter
    def radioVar(self, value):
        self._radioVar.set(value)
