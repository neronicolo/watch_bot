import tkinter as tk

from tkinter import filedialog
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import sys
 
# TODO: Watch *args, **kwargs.
#       How to initialize instance attibute passed from **kwargs?
#       d = ("a":3, "b":4, "c":6) -->
#       def __init__(self, **kwargs):
#           self.a=3
#           self.b=4
#           self.c=6
#       https://www.fast.ai/2019/08/06/delegation/
#       https://www.udemy.com/course/complete-python-bootcamp/learn/lecture/9442732#overview
# TODO: @property, meaning, usage?
# TODO: modify self._index of display_next() with decorator, reuse func() since only self.index is different
# TODO: Refractor display_next()
# TODO: Change style.
#   import tkinter.ttk as ttk 
#   ttk.Style().theme_use("clam")

class Application(tk.Frame):
    def __init__(self, master=None, imgs_dir_path=None, csv_file_path=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        # bind keys 
        self.master.bind("<Key>", self.callback)

        self.imgs_dir_path = Path(imgs_dir_path).resolve(strict=True)
        self.csv_file_path = Path(csv_file_path).resolve(strict=True)
        self._index = -1
        self._init_start = 1
        self.size = (580, 580)
        self.df = pd.read_csv(self.imgs_dir_path/self.csv_file_path).head()

        
        # store radiobutton values for image labels 
        self.dv_var = tk.DoubleVar(value=-1)
        self.lk_var = tk.DoubleVar(value=-1)
        self.iq_var = tk.DoubleVar(value=-1)
        
        # store radiobutton values for filter images 
        self.filter_pattern_var = tk.StringVar()

        # helper dict
        self.d = {'dial_visibility':self.dv_var,
                'like':self.lk_var,
                'image_quality':self.iq_var}

        self.layout()
        self.resume()
        self.display_next()

        # add padding around frame, widgets and pack it into main window
        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)
        self.config(padx=5, pady=5)
        self.pack()

        # raise window to the top
        self.master.lift()
        self.master.attributes('-topmost', True)
        self.master.after_idle(self.master.attributes, '-topmost', False)

    def layout(self):
        "Widget layout"
        # menu bar
        menubar = tk.Menu(self.master)
        filemenu =tk. Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Open")
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save As", command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

        # image label
        self.img_label = tk.Label(self)
        self.img_label.grid(row=0, column=0, rowspan=39)

        # label radiobuttons(rb) and labelframe(lf)
        s = {'lf_txt':["Dial Visibility:", "Like:", "Image Quality:"],
            'rb_var':[self.dv_var, self.lk_var, self.iq_var],
            'rb_txt':["1", "0"],
            'rb_val':[1, 0]}

        label_frame_outer = tk.LabelFrame(self, text="Label Images", padx=10, pady=10)
        label_frame_outer.grid(row=0, column=1, columnspan=2)

        for i, text in enumerate(s['lf_txt']):
            label_frame = tk.LabelFrame(label_frame_outer, text=text, padx=10, pady=10)
            label_frame.grid(row=i, column=1, columnspan=2)

            for j, value in enumerate(s['rb_val']):
                radiobutton = tk.Radiobutton(label_frame, text=s['rb_txt'][j], variable=s['rb_var'][i], value=value)
                radiobutton.grid(row=i, column=j+1, padx=10)
        
        # filter labelframe, entry, button
        filter_frame_outer = tk.LabelFrame(self, text="Filter Images", padx=10, pady=5)
        filter_frame_outer.grid(row=3, column=1, columnspan=2)

        filter_pattern_label_frame = tk.LabelFrame(filter_frame_outer, text="Filter Pattern", padx=10, pady=5)
        filter_pattern_label_frame.grid(row=5, column=1, columnspan=2)            

        filter_pattern_entry = tk.Entry(filter_pattern_label_frame, width=14, textvariable=self.filter_pattern_var)
        filter_pattern_entry.grid(row=5, column=1, columnspan=2, pady=5)

        self.filter_button = tk.Button(filter_frame_outer, text="Filter", command=self.filter_df)
        self.filter_button.grid(row=6, column=1, columnspan=1, sticky=('E'))

        # previous, next button
        self.previous_button = tk.Button(self, text="Previous", command=self.display_previous)
        self.previous_button.grid(row=38, column=1, columnspan=1, sticky=('E'))
        self.next_button = tk.Button(self, text="Next", command=self.display_next)
        self.next_button.grid(row=38, column=2, sticky=('W'))
        
        # status bar
        self.statusbar = tk.Label(self)
        self.statusbar.grid(row=39, column=0, columnspan=4, sticky=('E'))
        return

    def image_resize(self, image_path):
        """Resize image"""
        img = Image.open(image_path)
        img.thumbnail(self.size, Image.ANTIALIAS)
        new_img = Image.new('RGBA', self.size, (255, 255, 255, 0))
        new_img.paste(img, (int((self.size[0] - img.size[0]) / 2), int((self.size[1] - img.size[1]) / 2)))
        return new_img

    def display_next(self):
        """Display next image. Get values form rbuttons and add them to the dataframe. Set values of rbuttons form dataframe. Update status bar"""
        # initial start of the programm or index == -1        
        if self._init_start == 1 or self._index == -1:
            self._init_start = 0
        else:
            self.get_rbutton_values()

        # get next image path, resize image, show image
        self._index += 1
        try:
            img_path = self.imgs_dir_path/self.df.loc[self.df.index[self._index], 'name']
        except (IndexError):
            self._index = -1
            self.display_next()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(self.csv_file_path.name + ' - ' + img_path.name)
        self.set_rbutton_values()
        self.statusbar.configure(text=f"({self.df.index[self._index] + 1}/{self.total_images})")
                       
    def display_previous(self):
        """Display previous image. Get values form rbuttons and add them to the dataframe. Set values of rbuttons form dataframe. Update status bar"""
        # if initial start of the programm or index == -1        
        if self._index != -1:
            self.get_rbutton_values()

        # get previous image path, resize image, show image
        self._index -= 1
        try:
            img_path = self.imgs_dir_path/self.df.loc[self.df.index[self._index], 'name']
        except (IndexError):
            self._index = 0
            self.display_previous()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(self.csv_file_path.name + ' - ' + img_path.name)
        self.set_rbutton_values()
        self.statusbar.configure(text=f"({self.df.index[self._index] + 1}/{self.total_images})")
            
    def callback(self, event):
        if event.keysym == "bracketleft":
            self.display_previous()
        elif event.keysym == "bracketright":
            self.display_next()
        # watch face visibility
        elif event.keysym in "e":
            self.dv_var.set(1)
        elif event.keysym in "r":
            self.dv_var.set(0)       
        # like
        elif event.keysym in "d":
            self.lk_var.set(1)
        elif event.keysym in "f":
            self.lk_var.set(0)
        # image quality
        elif event.keysym in "c":
            self.iq_var.set(1)
        elif event.keysym in "v":
            self.iq_var.set(0)
        elif event.keysym in "Return":
            self.filter_df()
        #print(event.keysym)

    def resume(self):
        """Get index of first unlabeled image."""
        df = self.df[self.d.keys()]
        # get index of first occurrence of minimum value for each column
        ser = df.idxmin(axis=0)
        # get the label of min index 
        resume_label = ser.idxmin()
        # get min index
        resume_idx = ser[resume_label]
        # check if column values for min index are == -1, not labeled
        if df.loc[resume_idx, resume_label] == -1:
            # set index to be one before index of min value found 
            self._index = resume_idx - 1 
        
        #print(f'{df}\n{ser}\n{resume_label}\n{resume_idx}\n{self._resume_index}')

    def get_rbutton_values(self):
        """Get values from radiobuttons and add them to the dataframe"""
        for k,v in self.d.items():
            self.df.loc[self.df.index[self._index], k] = v.get()

    def set_rbutton_values(self):
        """Set values from dataframe columns to the radiobuttons"""       
        for k,v in self.d.items():
            v.set(self.remove_zero(self.df.loc[self.df.index[self._index], k]))

    def save(self):
        """Save file."""
        self.get_rbutton_values()
        file_path = self.imgs_dir_path/self.csv_file_path 
        self.df.to_csv(file_path, index=False)
        self.statusbar.configure(text=f"Saved to: {file_path}")
        return

    def save_as(self):
        """Save file as."""
        self.get_rbutton_values()
        file_path = filedialog.asksaveasfilename()
        try:
            self.df.to_csv(file_path, index=False)
        except ValueError:
            pass
        else:
            self.statusbar.configure(text=f"Saved to: {file_path}")
        return

    def remove_zero(self, num):
        """Remove zero from whole float number. Example: 1.0 --> 1"""
        if num % 1 == 0:
            return int(num)
        else:
            return num

    @property
    def total_images(self):
        "Total number of images"
        return self.df['name'].size

    def filter_df(self):
        # test notebook for this can be found ../sandbox/pandas
        # set focus to
        self.filter_button.focus()
        
        # column names to use when comparing against filter values
        filter_columns = list(self.d.keys())
        # filter values to compare against column values
        filter_values = self.filter_pattern_var.get().split(',')
        # convert list of strings to list of int
        filter_values = list(map(int, filter_values))

        # check if values in filter_columns are equal to filter_values
        # all() returns True if all values are True 
        df_filtered = self.df[filter_columns].eq(filter_values).all(1)
        # filtered dataframe
        #self.df = self.df.loc[df_filtered]
#
        #try:
        #    img_path = self.imgs_dir_path/self.df.loc[self.df.index[self._index], 'name']
        #except (IndexError):
        #    self._index = -1
        #    self.display_next()
        #    return
     

def main(imgs_path, csv_path):
    root = tk.Tk()
    Application(master=root, imgs_dir_path=imgs_path, csv_file_path=csv_path)

    root.mainloop()

if __name__ == "__main__":
    imgs = Path.home()/'programming/data/watch_bot/'
    csv = Path.home()/'programming/projects/watch_bot/data_prep/wfc_file_attribs.csv'
    main(imgs, csv)
    
    #main(sys.argv[1], sys.argv[2])
    