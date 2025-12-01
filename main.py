import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(__file__))


from Controllers.main_controller import MainController

if __name__ == "__main__":
    
    root = tk.Tk()

    app = MainController(root) 
    
    root.mainloop()

    if app and hasattr(app, '__del__'):
        app.__del__()