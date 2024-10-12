import tkinter as tk
# from tkinter import *
import cv2
from .var import Finales
from PIL import Image, ImageTk

class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        # Importing here to avoid circular import error
        from .page1 import Page1

        tk.Frame.__init__(self, parent)
        self._f = Finales()
        self._controller = controller

        # self.vid = cv2.VideoCapture(g.selectedCamera)
        # if not self.vid.isOpened():
        #     print("Unable to open video source", g.selectedCamera)

        img = tk.PhotoImage(file= self.f.MAINLOGOPATH)
        mainLogo = tk.Label(self, image=img)
        mainLogo.image = img
        mainLogo.pack_propagate(False)
        mainLogo.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan = 100)

        self.lbl_video  = tk.Label(self)
        self.lbl_video .grid(row = 50, column = 10)

        backBtn = tk.Button(self, text ="Back", command = lambda : controller.show_frame(Page1))
        backBtn.grid(row = 100, column = 1)

        nextBtn = tk.Button(self, text ="Next", command = lambda : controller.show_frame(Page1))
        nextBtn.grid(row = 100, column = 2)


    def update_frame(self):
        # Capture frame-by-frame
        ret, frame = self.vid.read()
        if ret:
            # Convert the image from BGR (OpenCV format) to RGB (Pillow format)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert the frame to an image that Tkinter can use
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update the label widget with the new frame
            self.lbl_video.imgtk = imgtk
            self.lbl_video.configure(image=imgtk)
        
        # Call the function again after a short delay (to create a video stream effect)
        self.lbl_video.after(10, self.update_frame)

    def on_show(self):
        # This method is called when Page2 is shown
        print("self.g.selectedCamera: ", self.controller.selectedCamera)
        self.vid = cv2.VideoCapture(self.controller.selectedCamera)
        if not self.vid.isOpened():
            print("Unable to open video source", self.controller.selectedCamera)
        self.update_frame()


    @property
    def f(self):
        return self._f
    @property
    def controller(self):
        return self._controller

    @property
    def vid(self):
        return self._vid
    @vid.setter
    def vid(self, value):
        self._vid = value

