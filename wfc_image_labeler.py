import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

# TODO: why git push is asking me for password???
# TODO: Save(added expression to update statusbar), Save as, Exit, Open
# TODO: @property
# TODO: Watch *args, **kwargs.
#       How to initialize instance attibute passed from **kwargs?
#       d = ("a":3, "b":4, "c":6) -->
#       def __init__(self, **kwargs):
#           self.a=3
#           self.b=4
#           self.c=6
# TODO: Key mappings/events 
# TODO: Add padding for each child in frame class and for frame itself 
#       for child in app.winfo_children(): child.grid_configure(padx=2, pady=2)
# TODO: modify self._index of display_next() with decorator, reuse func() since only self.index is different
# TODO: Raise above oter windows
# TODO: Change style
#       tk.tk.Style().theme_use("clam")
# TODO: @property?
# TODO: Refractor display_next()
# TODO: Add docstrings and comments

class Application(tk.Frame):
    def __init__(self, master=None, dir_path=None, file_name=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.master.bind("<Key>", self.callback)
        self.config(padx=5, pady=5)
        self.pack()

        self.dir_path = Path(dir_path)
        self.file_name = Path(file_name)
        self._index = -1
        self._init_start = 1
        self.size = (520, 520)
        self.df = pd.read_csv(self.dir_path/self.file_name).head()
        self.wfv_var = tk.DoubleVar(value=-1)
        self.cq_var = tk.DoubleVar(value=-1)
        self.lq_var = tk.DoubleVar(value=-1)
        self.iq_var = tk.DoubleVar(value=-1)
        self.d = {'watch_face_visibility':self.wfv_var,
                'composition_quality':self.cq_var,
                'light_quality':self.lq_var,
                'image_quality':self.iq_var}

        self.layout()
        self.resume()
        self.display_next()

    def layout(self):
        # menu bar
        menubar = tk.Menu(self.master)
        filemenu =tk. Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

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
        
        # status bar
        self.statusbar = tk.Label(self, bd=2)
        self.statusbar.grid(row=40, column=0, columnspan=4, sticky=('E'))
        return

    def image_resize(self, image_path):
        img = Image.open(image_path)
        img.thumbnail(self.size, Image.ANTIALIAS)
        new_img = Image.new('RGBA', self.size, (255, 255, 255, 0))
        new_img.paste(img, (int((self.size[0] - img.size[0]) / 2), int((self.size[1] - img.size[1]) / 2)))
        return new_img

    def display_next(self):
        # initial start of the programm or index == -1        
        if self._init_start == 1 or self._index == -1:
            self._init_start = 0
        else:
            self.get_rbutton_values()

        # get next image path, resize image, show image
        self._index += 1
        try:
            img_path = self.dir_path/self.df.loc[self._index, 'name']
        except KeyError:
            self._index = -1
            self.display_next()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(img_path.name)
        self.set_rbutton_values()
        self.statusbar.configure(text=f"({self._index}/{self.total_images})")
                       
    def display_previous(self):
        # if initial start of the programm or index == -1        
        if self._index != -1:
            self.get_rbutton_values()

        # get previous image path, resize image, show image
        self._index -= 1
        try:
            img_path = self.dir_path/self.df.loc[self._index, 'name']
        except KeyError:
            self._index = -1
            self.display_next()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(img_path.name)
        self.set_rbutton_values()
        self.statusbar.configure(text=f"({self._index}/{self.total_images})")
            
    def callback(self, event):
        if event.keysym == "Right":
            self.display_next()
        elif event.keysym == "Left":
            self.display_previous()
        #print(event.keysym)

    def resume(self):
        df = self.df[['watch_face_visibility', 'composition_quality', 'light_quality', 'image_quality']]
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
        """Get values from radiobuttons and add them to dataframe"""
        for k,v in self.d.items():
            self.df.loc[self._index, k] = v.get()

    def set_rbutton_values(self):
        """Set values from dataframe columns to radiobuttons"""       
        for k,v in self.d.items():
            v.set(self.remove_zero(self.df.loc[self._index, k]))

    def save(self):
        # TODO: Dialog popup - Overwrite or increment file?
        increment = False
        if increment == True:
            counter = 1
            while True:
                file_name = self.dir_path/(self.file_name.stem + '_' + str(counter) + self.file_name.suffix)
                if file_name.exists():
                    counter = +1
                break
        else:
            file_name = self.dir_path/self.file_name

        csv_path = self.dir_path/file_name 
        
        self.get_rbutton_values()
        #self.df.to_csv(self.dir_path/file_name, index=False)
        self.statusbar.configure(text=f"Saved to:{csv_path}")
        return csv_path

    def remove_zero(self, num):
        """Remove zero from number if it's a whole nummber. Example: 1.0 --> 1"""
        if num % 1 == 0:
            return int(num)
        else:
            return num
    
    @property
    def total_images(self):
        return self.df['name'].size

if __name__ == "__main__":

    # Path to csv file
    d = Path.home()/'programming/data/watch_bot/'
    f = 'wfc_file_attribs.csv'
    #f = 'wfc_labels.csv'
    check.path_check(d/f)

    root = tk.Tk()
    app = Application(master=root, dir_path=d, file_name=f)
 
    root.mainloop()
