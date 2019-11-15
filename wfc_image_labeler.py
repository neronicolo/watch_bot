import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

# TODO: Add title
# TODO: Key mappings/events
# TODO: Refractor display_next()
# TODO: Separate status bar by line. Maybe add file name on status West side
# TODO: Add padding
# TODO: Add docstrings

class Application(tk.Frame):
    def __init__(self, master=None, dir_path=None, file_name=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.pack()

        self.dir_path = dir_path
        self.file_name = file_name
        self.df = pd.read_csv(self.dir_path/self.file_name)
        self._index = -1
        self.size = (520, 520)
        self.layout()
        self.display_next()

    def layout(self):
        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Previous", command=self.display_previous).grid(row=1, column=0, sticky=('E'))
        tk.Button(self, text="Next", command=self.display_next).grid(row=1, column=1, sticky=('W'))
        return

    def image_resize(self, image_path):
        img = Image.open(image_path)
        img.thumbnail(self.size, Image.ANTIALIAS)
        new_img = Image.new('RGBA', self.size, (255, 255, 255, 0))
        new_img.paste(img, (int((self.size[0] - img.size[0]) / 2), int((self.size[1] - img.size[1]) / 2)))
        return new_img

    def display_next(self):
        self._index += 1
        try:
            img_path = self.dir_path/self.df['name'][self._index]
        except KeyError:
            self._index = -1
            self.display_next()
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(img_path.name)

    def display_previous(self):
        pass

if __name__ == "__main__":

    # Path to csv file
    d = Path.home()/'programming/data/watch_bot/'
    f = 'wfc_file_attribs.csv'
    check.path_check(d/f)

    root = tk.Tk()
    app = Application(master=root, dir_path=d, file_name=f)
    root.mainloop()
