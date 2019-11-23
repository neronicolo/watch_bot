import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

# TODO: Watch *args, **kwargs.
#       How to initialize instance attibute passed from **kwargs?
#       d = ("a":3, "b":4, "c":6) -->
#       def __init__(self, **kwargs):
#           self.a=3
#           self.b=4
#           self.c=6
# TODO: get radiobutton value before moving to next image,
#       store captured value into dataframe
#       reset value to 0
#       For previous button set to read value from data frame and writing will be handled with next button
# TODO: Key mappings/events 
# TODO: Separate status bar by line. Maybe add file name on status West side
# TODO: Add padding for each child in frame class and for frame itself 
#       for child in app.winfo_children(): child.grid_configure(padx=2, pady=2)
# TODO: Raise above oter windows
# TODO: Change style
#       tk.tk.Style().theme_use("clam")
# TODO: Refractor display_next()
# TODO: Add docstrings

class Application(tk.Frame):
    def __init__(self, master=None, dir_path=None, file_name=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.master.bind("<Key>", self.callback)
        self.config(padx=5, pady=5)
        self.pack()

        self.dir_path = dir_path
        self.file_name = file_name
        self._index = -1
        self.size = (520, 520)
        self.df = pd.read_csv(self.dir_path/self.file_name)
        # we don't need this since every time we start a program it will reset previously saved values
        #self.df['watch_face_visibility'] = -1
        #self.df['composition_quality'] = -1
        #self.df['light_quality'] = -1
        #self.df['image_quality'] = -1
        self.wfv_var = tk.DoubleVar(value=-1)
        self.cq_var = tk.DoubleVar(value=-1)
        self.lq_var = tk.DoubleVar(value=-1)
        self.iq_var = tk.DoubleVar(value=-1)
        self.layout()
        self.display_next()

    def layout(self):
        # image label
        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=0, rowspan=40)

        # radiobuttons(rb) and labelframe(lf)
        s = {'lf_txt':["Watch Face Visibility:","Composition quality:","Lighting quality:","Image quality:"],
            'rb_var':[self.wfv_var, self.cq_var, self.lq_var, self.iq_var],
            'rb_txt':["1", "0.5", "0"],
            'rb_val':[1, 0.5, 0]}

        for i, text in enumerate(s['lf_txt']):
            label_frame = tk.LabelFrame(self, text=text, padx=5, pady=5)
            label_frame.grid(row=i, column=1, columnspan=3, sticky=('W'))

            for j, value in enumerate(s['rb_val']):
                radiobutton = tk.Radiobutton(label_frame, text=s['rb_txt'][j], variable=s['rb_var'][i], value=value)
                radiobutton.grid(row=i, column=j+1, padx=5) 
    
        # previous, next button
        self.previous_button = tk.Button(self, text="Previous", command=self.display_previous)
        self.previous_button.grid(row=38, column=2, columnspan=1, sticky=('E'))
        self.next_button = tk.Button(self, text="Next", command=self.display_next)
        self.next_button.grid(row=38, column=3, sticky=('W'))
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
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(img_path.name)

        # TODO: Look at TODO #2
        d = {'watch_face_visibility':self.wfv_var,
            'composition_quality':self.cq_var,
            'light_quality':self.lq_var,
            'image_quality':self.iq_var}

        for k,v in d.items():
            val = v.get()
            self.df.loc[self._index-1, k]= val
            v.set(-1)
            print(f"{k} --> {self.df.loc[self._index-1, k]}, {self.df.loc[self._index, 'name']}")
     
    # TODO: modify self._index of display_next() with decorator, reuse func() since only one var is different
    def display_previous(self):
        self._index -= 1
        try:
            img_path = self.dir_path/self.df['name'][self._index]
        except KeyError:
            self._index = -1
            self.display_next()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(img_path.name)

    def callback(self, event):
        if event.keysym == "Right":
            self.display_next()
        elif event.keysym == "Left":
            self.display_previous()
        #print(event.keysym)

    def store_and_reset(self):
        pass

if __name__ == "__main__":

    # Path to csv file
    d = Path.home()/'programming/data/watch_bot/'
    f = 'wfc_file_attribs.csv'
    check.path_check(d/f)

    root = tk.Tk()
    app = Application(master=root, dir_path=d, file_name=f)
 
    #root.mainloop()
