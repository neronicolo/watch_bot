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
# TODO: Refractor display_next(), display_previous(), @decorator?
# TODO: Change style.
#   import tkinter.ttk as ttk 
#   ttk.Style().theme_use("clam")

class Application(tk.Frame): 
    def __init__(self, master=None, imgs_dir_path=None, csv_file_path=None, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        # bind keys 
        self.master.bind("<Key>", self.callback)
        self.master.bind("<Control-s>", self.save)
        self.master.bind("<Control-a>", self.save_as)
        self.master.bind("<Control-r>", self.reset_filter_df)

        self.imgs_dir_path = Path(imgs_dir_path).resolve(strict=True)
        self.csv_file_path = Path(csv_file_path).resolve(strict=True)
        self._index = -1
        self._init_start = 1
        self.size = (640, 640)
        #self.size = (600, 600)
        self.df = pd.read_csv(self.imgs_dir_path/self.csv_file_path)
        self.df_filtered = self.df.copy()
         
        # store radiobutton values for image labels 
        self.dv_var = tk.DoubleVar(value=-1)
        self.lk_var = tk.DoubleVar(value=-1)
        self.iq_var = tk.DoubleVar(value=-1)
        
        # store entry widget values 
        self.filter_pattern_var = tk.StringVar()
        self.jump_to_image_var = tk.StringVar()
        self.threshold_label_var = tk.StringVar()

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

        label_frame_outer = tk.LabelFrame(self, text="Label Images", padx=8, pady=8)
        label_frame_outer.grid(row=0, column=1, columnspan=2)

        for i, text in enumerate(s['lf_txt']):
            label_frame = tk.LabelFrame(label_frame_outer, text=text, padx=8, pady=4)
            label_frame.grid(row=i, column=1, columnspan=2)

            for j, value in enumerate(s['rb_val']):
                radiobutton = tk.Radiobutton(label_frame, text=s['rb_txt'][j], variable=s['rb_var'][i], value=value)
                radiobutton.grid(row=i, column=j+1, padx=10)
        
        # filter image
        filter_frame_outer = tk.LabelFrame(self, text="Filter Images", padx=8, pady=4)
        filter_frame_outer.grid(row=3, column=1, columnspan=2)

        pred_threshold_label_frame = tk.LabelFrame(filter_frame_outer, text="Label Pattern:", padx=8, pady=4)
        pred_threshold_label_frame.grid(row=4, column=1, columnspan=2)            

        self.label_pattern_entry = tk.Entry(pred_threshold_label_frame, width=14, textvariable=self.filter_pattern_var)
        self.label_pattern_entry.grid(row=5, column=1, columnspan=2, pady=4)

        self.label_filter_button = tk.Button(pred_threshold_label_frame, text="Filter", command=self.filter_df)
        self.label_filter_button.grid(row=6, column=1, columnspan=2)

        # jump to image
        jump_to_image_label_frame = tk.LabelFrame(filter_frame_outer, text="Image Number:", padx=8, pady=4)
        jump_to_image_label_frame.grid(row=7, column=1, columnspan=2)            

        self.jump_to_image_entry = tk.Entry(jump_to_image_label_frame, width=14, textvariable=self.jump_to_image_var)
        self.jump_to_image_entry.grid(row=8, column=1, columnspan=2, pady=4)

        self.jump_button = tk.Button(jump_to_image_label_frame, text="Jump", command=self.jump_to_image)
        self.jump_button.grid(row=9, column=1, columnspan=2)

        # filter by prediction threshold
        pred_threshold_label_frame = tk.LabelFrame(filter_frame_outer, text="Threshold; Label:", padx=8, pady=4)
        pred_threshold_label_frame.grid(row=10, column=1, columnspan=2)            

        self.pred_threshold_entry = tk.Entry(pred_threshold_label_frame, width=14, textvariable=self.threshold_label_var)
        self.pred_threshold_entry.grid(row=11, column=1, columnspan=2, pady=4)

        self.pred_threshold_button = tk.Button(pred_threshold_label_frame, text="Filter", command=self.filter_by_prediction)
        self.pred_threshold_button.grid(row=12, column=1, columnspan=2)

        # reset to initial image
        self.reset_filter_button = tk.Button(filter_frame_outer, text="Reset", command=self.reset_filter_df)
        self.reset_filter_button.grid(row=13, column=1, columnspan=2, pady=4)

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

        # small thumbnail version    
        img.thumbnail(tuple(map(lambda x: int(x/5)-8, self.size)), Image.ANTIALIAS)
        thumbnail_size = tuple(map(lambda x: int(x/5), self.size))
        thumbnail_img = Image.new('RGB', thumbnail_size, (64, 64, 64))
        thumbnail_img.paste(img, (int((thumbnail_size[0] - img.size[0]) / 2), int((thumbnail_size[1] - img.size[1]) / 2)))
        new_img.paste(thumbnail_img, (self.size[0] - thumbnail_size[0], 0))
        
        return new_img

    def display_next(self):
        """Display next image. Get values form rbuttons and add them to the dataframe. Set values of rbuttons form dataframe. Update status bar"""
        # initial start of the programm
        if self._init_start == 1:
            self._init_start = 0
        else:
            self.get_rbutton_values()

        # get next image path, resize image, show image
        self._index += 1
        try:
            img_path = self.imgs_dir_path/self.df.loc[self.df_filtered.index[self._index], 'name']
        except (IndexError):
            self._init_start = 1
            self._index = -1
            self.display_next()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(self.csv_file_path.name + ' - ' + img_path.name)
        self.set_rbutton_values()
        self.statusbar.configure(text=f"{self._index}({self.df_filtered.index[self._index]})/{self.total_images - 1}")
                       
    def display_previous(self):
        """Display previous image. Get values form rbuttons and add them to the dataframe. Set values of rbuttons form dataframe. Update status bar"""
        # initial start of the programm
        if self._init_start == 1:
            self._init_start = 0
        else:
            self.get_rbutton_values()

        # get previous image path, resize image, show image
        self._index -= 1
        try:
            img_path = self.imgs_dir_path/self.df.loc[self.df_filtered.index[self._index], 'name']
        except (IndexError):
            self._init_start = 1
            self._index = 0
            self.display_previous()
            return
        resized_img = self.image_resize(img_path)
        photoimage = ImageTk.PhotoImage(resized_img)
        self.img_label.configure(image=photoimage)
        self.img_label.image = photoimage
        self.master.title(self.csv_file_path.name + ' - ' + img_path.name)
        self.set_rbutton_values()
        self.statusbar.configure(text=f"{self._index}({self.df_filtered.index[self._index]})/{self.total_images - 1}")
            
    def callback(self, event):
        if event.keysym == "bracketleft":
            self.display_previous()
        elif event.keysym == "bracketright":
            self.display_next()
        # watch face visibility
        elif event.keysym in "q":
            self.dv_var.set(1)
        elif event.keysym in "w":
            self.dv_var.set(0)       
        # like
        elif event.keysym in "a":
            self.lk_var.set(1)
        elif event.keysym in "s":
            self.lk_var.set(0)
        # image quality
        elif event.keysym in "z":
            self.iq_var.set(1)
        elif event.keysym in "x":
            self.iq_var.set(0)
        #print(event.keysym)

    def resume(self):
        """Get index of first unlabeled image."""
        self._init_start = 1
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
        else:
            self._index = -1

    def get_rbutton_values(self):
        """Get values from radiobuttons and add them to the dataframe"""
        for k,v in self.d.items():
            self.df.loc[self.df_filtered.index[self._index], k] = v.get()

    def set_rbutton_values(self):
        """Set values from dataframe columns to the radiobuttons"""       
        for k,v in self.d.items():
            v.set(self.remove_zero(self.df.loc[self.df_filtered.index[self._index], k]))

    def save(self,event=None):
        """Save file."""
        self.get_rbutton_values()
        file_path = self.imgs_dir_path/self.csv_file_path 
        self.df.to_csv(file_path, index=False)
        self.statusbar.configure(text=f"Saved to: {file_path}")

    def save_as(self, event=None):
        """Save file as."""
        self.get_rbutton_values()
        file_path = filedialog.asksaveasfilename()
        try:
            self.df.to_csv(file_path, index=False)
        except ValueError:
            pass
        else:
            self.statusbar.configure(text=f"Saved to: {file_path}")

    def remove_zero(self, num):
        """Remove zero from whole float number. Example: 1.0 --> 1"""
        if num % 1 == 0:
            return int(num)
        else:
            return num

    @property
    def total_images(self):
        "Total number of images"
        #return self.df_filtered['name'].size
        return self.df_filtered['name'].size

    def filter_df(self):
        '''Filter images based on their label values'''
        # test notebook for this can be found ../sandbox/pandas
        # column names to use when comparing against filter values
        filter_columns = list(self.d.keys())
        # filter values to compare against column values
        filter_values = self.filter_pattern_var.get().split(',') 
        try:
            # convert list of strings to list of int
            filter_values = list(map(int, filter_values))
            # check if values in filter_columns are equal to filter_values
            # all() returns True if all values are True 
            df_filtered = self.df[filter_columns].eq(filter_values).all(1)
        except (ValueError):
            self.label_pattern_entry.delete(0,'end')
            self.statusbar.configure(text=f"Invalid Filter Pattern")
            return
        finally:
            self.focus()
            #self.label_pattern_entry.delete(0,'end')
            self.jump_to_image_entry.delete(0,'end')            
            self.pred_threshold_entry.delete(0,'end') 
        # filtered dataframe
        self.df_filtered = self.df.loc[df_filtered]
        if not self.df_filtered.empty:
            # reset to the first image and display it
            self._init_start = 1
            self._index = -1
            self.display_next()
        else: 
            self.statusbar.configure(text=f"Invalid Filter Pattern")
            return

    def jump_to_image(self):
        '''Jump to image number'''
        #self.df_filtered = self.df.copy()
        image_value = self.jump_to_image_var.get()
        try:
            self._init_start = 1
            self._index = int(image_value) - 1
            self.display_next()
        except (ValueError):
            self.statusbar.configure(text=f"Invalid Image Number")
            return
        finally:
            self.focus()
            #self.label_pattern_entry.delete(0,'end')
            self.jump_to_image_entry.delete(0,'end')
            #self.pred_threshold_entry.delete(0,'end') 

    def filter_by_prediction(self):
        '''Filter images based on prediction value threshold'''
        threshold,label = tuple(self.threshold_label_var.get().split(';'))
        thresh_min, thresh_max = tuple(threshold.split('-'))
        try:
            if (int(label) == 0):
                self.df_filtered = self.df[self.df[['dial_visibility_p_0', 'dial_visibility_p_1']].max(1) > float(thresh_min)]
                self.df_filtered = self.df_filtered[self.df_filtered[['dial_visibility_p_0', 'dial_visibility_p_1']].max(1) < float(thresh_max)] 
            elif (int(label) == 1):
                pass
        except (ValueError):
            self.pred_threshold_entry.delete(0,'end')
            self.statusbar.configure(text=f"Invalid Filter Pattern")
            return
        finally:
            self.focus()
            self.jump_to_image_entry.delete(0,'end')            
            self.label_pattern_entry.delete(0,'end')
            #self.pred_threshold_entry.delete(0,'end') 
        if not self.df_filtered.empty:
            # reset to the first image and display it
            self._init_start = 1
            self._index = -1
            self.display_next()
        else: 
            self.statusbar.configure(text=f"Invalid Filter Pattern")
            return

    def reset_filter_df(self, event=None):
        self.df_filtered = self.df.copy()
        self.resume()
        self.display_next()

        self.focus()
        self.label_pattern_entry.delete(0,'end')
        self.jump_to_image_entry.delete(0,'end')
        self.pred_threshold_entry.delete(0,'end')
        
def main(imgs_path, csv_path):
    root = tk.Tk()
    Application(master=root, imgs_dir_path=imgs_path, csv_file_path=csv_path)

    root.mainloop()

if __name__ == "__main__":
    data_path = Path.home()/'programming/data/chrono24'
    csv_path = data_path/'file_attribs_chrono24_merged.csv'
    main(data_path, csv_path)
    
    #main(sys.argv[1], sys.argv[2])
