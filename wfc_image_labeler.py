import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

# TODO: How to define **kwargs
class Application(tk.Frame):
    def __init__(self, master=None, dir_name=None, file_name=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.pack()

        self.dir_name = dir_name
        self.file_name = file_name
        self.start_index = -1
        self.layout()
        self.display_next()
        print(self.dir_name, self.file_name)

    def layout(self):
        pass

    def display_next(self):
        pass

    def display_previous(self):
        pass

if __name__ == "__main__":

    # Path to csv file
    d = Path.home()/'programming/data/watch_bot/'
    f = 'wfc_file_attribs.csv'
    check.path_check(d/f)

    root = tk.Tk()
    app = Application(master=root, dir_name=d, file_name=f)
    root.mainloop()
