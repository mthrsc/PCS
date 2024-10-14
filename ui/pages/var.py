
class Finales():
    def __init__(self):
        self._LARGEFONT = ("Verdana", 35)
        self._NORMALFONT = ("Verdana", 20)
        self._MAINLOGOPATH = "assets/appTitleLogo.png"
        self._OCR_API_KEY = "K85462937588957"

    @property
    def LARGEFONT(self):
        return self._LARGEFONT

    @property
    def NORMALFONT(self):
        return self._NORMALFONT

    @property
    def MAINLOGOPATH(self):
        return self._MAINLOGOPATH

    @property
    def OCR_API_KEY(self):
        return self._OCR_API_KEY


