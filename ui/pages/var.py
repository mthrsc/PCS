
class Finales():
    def __init__(self):
        self._LARGEFONT = ("Verdana", 35)
        self._NORMALFONT = ("Verdana", 20)
        self._MAINLOGOPATH = "assets/appTitleLogo.png"

    @property
    def LARGEFONT(self):
        return self._LARGEFONT

    @property
    def NORMALFONT(self):
        return self._NORMALFONT

    @property
    def MAINLOGOPATH(self):
        return self._MAINLOGOPATH





#############################################

class Globals():
    def __init__(self):
        ...
        self._selectedCamera = -1

    @property
    def selectedCamera(self):
        return self._selectedCamera
    @selectedCamera.setter
    def selectedCamera(self, value):
        self._selectedCamera = value
