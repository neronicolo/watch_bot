import collections
import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

def image_resize(file_path, size):
    img = Image.open(file_path)
    img.thumbnail(size, Image.ANTIALIAS)

    bg = Image.new('RGBA', size, (255, 255, 255, 0))
    bg.paste(img, (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2)))
    return bg

class ImageViewer(tk.Frame):
    def __init__(self, dir_path, file_name):
        tk.Frame.__init__(self)
        self.dir_path = dir_path
        self.file_name = file_name
        self.start_index = -1
        self.size = (500, 500)
        self.layout()
        self.display_next()
    
    def image_path(self):
        self.df = pd.read_csv(self.dir_path/file_name)
        self.img_name = self.df['name'][self.start_index]
        self.img_path = self.dir_path/self.img_name
        #return self.img_path

    def image_load(self):
        self.img = image_resize(self.img_path, self.size)
        self.img = ImageTk.PhotoImage(self.img)
        #return self.img

    def layout(self):
        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Previous", command=self.display_previous).grid(row=1, column=0, sticky=('E'))
        tk.Button(self, text="Next", command=self.display_next).grid(row=1, column=1, sticky=('W'))

    def display_next(self):
        self.start_index += 1
        self.image_path()
        self.image_load()
        self.img_label.configure(image=self.img)

    def display_previous(self):
        self.start_index -= 1
        self.image_path()
        self.image_load()
        self.img_label.configure(image=self.img)

    # TODO: Put duplicate code into one func and call it inside other func
    # TODO: Add padding around widgets recursively

def main(dir_path, file_name):
    root = tk.Tk()
    root.title("Image Viewer")

    app = ImageViewer(dir_path, file_name)
    app.grid(row=0, column=0)
    print(app.start_index)

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
