import sys
from ui import tkinterApp
import os

def main():
    app = tkinterApp.tkinterApp()

    set_window_size(app, "1050x600")
    set_window_name(app, "PCS - Pokemon Card Scanner")
    set_close_cross_behaviour(app)
    
    app.mainloop()

# Three custom function in project.py requested by assignment
# Set app title
def set_window_name(app, title):
    app.title(title)

# Set app size on screen
def set_window_size(app, resolution):
    app.geometry(resolution)

# Set what happens when clicking the closing cross
def set_close_cross_behaviour(app):
    app.protocol("WM_DELETE_WINDOW", sys.exit)


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



