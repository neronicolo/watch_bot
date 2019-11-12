from pathlib import Path
import tkinter as tk
from tkinter import ttk

import pandas as pd
from PIL import Image, ImageTk

import check
# TODO: Revrite __init__ to look like tkinter_example.py
# TODO: Key mappings/events
# TODO: Add title
# TODO: Separate status bar by line. Maybe add file name on status West side
# TODO: Add docstrings
# TODO: How to define **kwargs

class Application(tk.ttk.Frame):
    def __init__(self, *args, **kwargs):
        DIR_PATH = kwargs['dir_path']
        FILE_NAME = kwargs['file_name']

        # remove kwargs from passing to tk.ttk.Frame
        for e in ['dir_path', 'file_name']:
            kwargs.pop(e)
        
        tk.ttk.Frame.__init__(self, *args, **kwargs)

        self.dir_path = DIR_PATH
        self.file_name = FILE_NAME
        self.df = pd.read_csv(self.dir_path/self.file_name)
        self.start_index = -1
        self.size = (480, 480)
        self.layout()
        self.display_next()
    
    def total_items(self):
        return self.df['name'].size
        
    def image_path(self):
        img_name = self.df['name'][self.start_index]
        img_path = self.dir_path/img_name
        return img_path

    def image_resize(self):
        img = Image.open(self.image_path())
        img.thumbnail(self.size, Image.ANTIALIAS)
        bg = Image.new('RGBA', self.size, (255, 255, 255, 0))
        bg.paste(img, (int((self.size[0] - img.size[0]) / 2), int((self.size[1] - img.size[1]) / 2)))
        return bg

    def image_load(self):
        img = self.image_resize()
        img = ImageTk.PhotoImage(img)
        self.img_label.configure(image=img)
        self.img_label.image = img
        return img

    def update_widgets(self):
        self.progress_label.configure(text=f"({self.start_index + 1} / {self.total_items() - 1})")
        self.img_name_label.configure(text=str(Path(self.image_path()).name))

    def layout(self):
        self.img_label = ttk.Label(self)
        self.img_label.grid(row=0, column=0, columnspan=2)
        self.progress_label = ttk.Label(self)
        self.progress_label.grid(row=2, column=1, columnspan=2, sticky=('E'))
        self.img_name_label = ttk.Label(self)
        self.img_name_label.grid(row=2, column=0, columnspan=2, sticky=('W'))
        ttk.Button(self, text="Previous", command=self.display_previous).grid(row=1, column=0, sticky=('E'))
        ttk.Button(self, text="Next", command=self.display_next).grid(row=1, column=1, sticky=('W'))

    def display_next(self):
        try:
            self.start_index += 1
            self.image_path()
        except KeyError:
            self.start_index = -1 # reset index beginning
            self.display_next()
            return
        self.image_load()
        self.update_widgets()

    def display_previous(self):
        try:
            self.start_index -= 1
            self.image_path()
        except KeyError:
            self.start_index = -1 # reset index to beginning
            self.display_next()
            return
        self.image_load()
        self.update_widgets()

def main(DIR_PATH, FILE_NAME):
    root = tk.Tk()

    app = Application(root, dir_path=DIR_PATH, file_name=FILE_NAME, padding=5)
    app.grid(row=0, column=0)
    #for child in app.winfo_children(): child.grid_configure(padx=2, pady=2)
    #tk.ttk.Style().theme_use("clam")

    root.title("Image Viewer" + " - ")
    root.mainloop()

if __name__ == "__main__":

    # Path to csv file
    d = Path.home()/'programming/data/watch_bot/'
    f = 'wfc_file_attribs.csv'
    check.path_check(d/f)

    main(d, f)
