import collections
import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

class ImageViewer(tk.Frame):
    def __init__(self, dir_path, file_name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.dir_path = dir_path
        self.file_name = file_name
        self.start_index = -1
        self.size = (500, 500)
        self.layout()
        self.display_next()
    
    def image_path(self):
        df = pd.read_csv(self.dir_path/file_name)
        img_name = df['name'][self.start_index]
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

    def layout(self):
        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Previous", command=self.display_previous).grid(row=1, column=0, sticky=('E'))
        tk.Button(self, text="Next", command=self.display_next).grid(row=1, column=1, sticky=('W'))

    def display_next(self):
        self.start_index += 1
        self.image_path()
        self.image_load()

    def display_previous(self):
        self.start_index -= 1
        self.image_path()
        self.image_load()

    # TODO: Put duplicate code into one func and call it inside other func
    # TODO: Add padding around widgets recursively

def main(dir_path, file_name):
    root = tk.Tk()
    root.title("Image Viewer")

    app = ImageViewer(dir_path, file_name)
    app.grid(row=0, column=0)
    for child in app.winfo_children(): child.grid_configure(padx=2, pady=2)
    
    # start event loop
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)

    root.mainloop()

if __name__ == "__main__":

    # Path to csv file
    dir_path = Path.home()/'programming/data/watch_bot/'
    file_name = 'wfc_file_attribs.csv'
    check.path_check(dir_path/file_name)

    main(dir_path, file_name)
