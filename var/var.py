
class Finales():
    def __init__(self):
        self._LARGEFONT = ("Verdana", 35)
        self._NORMALFONT = ("Verdana", 20)
        self._MAINLOGOPATH = "assets/appTitleLogo.png"
        self._OCR_API_KEY = "K85462937588957"
        self._OCR_RQ_URL = "https://api.ocr.space/parse/image"
        self._SCRAP_ADDRESS = "https://www.cardmarket.com/Pokemon/Products/Search?searchString="

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

    @property
    def OCR_RQ_URL(self):
        return self._OCR_RQ_URL

    @property
    def SCRAP_ADDRESS(self):
        return self._SCRAP_ADDRESS



