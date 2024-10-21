import sys
from ui import tkinterApp
import os

def main():
    app = tkinterApp.tkinterApp()
    app.geometry("1050x600")

    app.protocol("WM_DELETE_WINDOW", sys.exit)
    
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    # Handle keyboard interrupt during dev
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)



