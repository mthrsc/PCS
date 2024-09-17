import sys
from ui import tkinterApp
import os

def main():
    app = tkinterApp.tkinterApp()
    app.geometry("1024x800")

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



# def thread_example():
#     t1 = threading.Thread(target=t1_func, args=(0,), name="thread1")
#     t2 = threading.Thread(target=t2_func, args=(0,))

#     t1.start()
#     t2.start()


# def t1_func(i):
#     while(i < 10):
#         i = i + 1
#         print("i: ", i)
#     print("Task 1 assigned to thread: {}".format(threading.current_thread().name))

# def t2_func(y):
#     while(y < 20):
#         y = y + 2
#         print("y: ", y)    