import sys
from ui import tkinterApp
import os

def main():
    app = tkinterApp.tkinterApp()
    app.geometry("1280x800")

    #Create a fullscreen window
    # app.state('zoomed')

    # app.protocol("WM_DELETE_WINDOW", app.destroy)
    app.protocol("WM_DELETE_WINDOW", sys.exit)
    
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)

