import tkinter as tk
from pathlib import Path

import pandas as pd
from PIL import Image, ImageTk

import check

# TODO: resume, write file to csv, create menu bar
# TODO; Add status bar to display image number/total images, saved file report... 
# TODO: Watch *args, **kwargs.
#       How to initialize instance attibute passed from **kwargs?
#       d = ("a":3, "b":4, "c":6) -->
#       def __init__(self, **kwargs):
#           self.a=3
#           self.b=4
#           self.c=6
# TODO: Key mappings/events 
# TODO: Separate status bar by line. Maybe add file name on status West side
# TODO: Add padding for each child in frame class and for frame itself 
#       for child in app.winfo_children(): child.grid_configure(padx=2, pady=2)
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
        self.size = (520, 520)
        self.df = pd.read_csv(self.dir_path/self.file_name).head()
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
        self.resume()
        self.display_next()

    def layout(self):
        # menu bar
        menubar = tk.Menu(self.master)
        filemenu =tk. Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save", command=self.save_to_csv)
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
        return

    def image_resize(self, image_path):
        img = Image.open(image_path)
        img.thumbnail(self.size, Image.ANTIALIAS)
        new_img = Image.new('RGBA', self.size, (255, 255, 255, 0))
        new_img.paste(img, (int((self.size[0] - img.size[0]) / 2), int((self.size[1] - img.size[1]) / 2)))
        return new_img

    def display_next(self):
        # add values from radiobuttons to dataframe columns
        d = {'watch_face_visibility':self.wfv_var,
            'composition_quality':self.cq_var,
            'light_quality':self.lq_var,
            'image_quality':self.iq_var}
       
        for k,v in d.items():
            if (self._index == -1):
                continue
            else:
                self.df.loc[self._index, k] = v.get()
                #print(f"{k} --> ({self.df.loc[self._index, k]}), {self.df.loc[self._index, 'name']}")
            v.set(-1)

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
                 
    # TODO: modify self._index of display_next() with decorator, reuse func() since only self.index is different
    def display_previous(self):
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

        # geta and set values from dataframe columns to radiobuttons
        d = {'watch_face_visibility':self.wfv_var,
            'composition_quality':self.cq_var,
            'light_quality':self.lq_var,
            'image_quality':self.iq_var}
       
        for k,v in d.items():
            # remove ".0" form float numbers
            float_num = lambda n: int(n) if not n%1 else n
            v.set(float_num(self.df.loc[self._index, k]))

    def callback(self, event):
        if event.keysym == "Right":
            self.display_next()
        elif event.keysym == "Left":
            self.display_previous()
        #print(event.keysym)

    def resume(self):
        # TODO: Dialog popup - Resume or start from begininng. Or start with resume and put button for reset?
        df = self.df[['watch_face_visibility', 'composition_quality', 'light_quality', 'image_quality']]
        # Return index of first occurrence of minimum value over requested axis
        ser = df.idxmin(axis=0)
        # get minimum value of index for returned indexes
        idx_min = ser.min()
        print(f'{df}\n{ser}\nidx_min={idx_min}')

        self._index = idx_min - 1

    def save_to_csv(self):
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

        print(f'File name: {file_name}')
        self.df.to_csv(self.dir_path/'wfc_labels.csv', index=False)

if __name__ == "__main__":

    # Path to csv file
    d = Path.home()/'programming/data/watch_bot/'
    f = 'wfc_file_attribs.csv'
    #f = 'wfc_labels.csv'
    check.path_check(d/f)

    root = tk.Tk()
    app = Application(master=root, dir_path=d, file_name=f)
 
    root.mainloop()
