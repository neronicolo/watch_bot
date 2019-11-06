import collections
from pathlib import Path
from tkinter import *
from tkinter import ttk

import pandas as pd
from PIL import Image, ImageTk

import check

# Get image file path
dir_path = check.path_check(Path.home()/'programming/data/watch_bot/')
df = pd.read_csv(dir_path/'wfc_file_attribs.csv')
#file_name = df['name']
#file_path = dir_path/file_name[666]

# TODO: We have list of images, how to show 'next' or 'previous' image from the list.
# How to choose which one to start from? Initially form the first image, otherwise form the first unlabeled(-1)
start_index = -1
file_name = df.iloc[start_index]['name']
file_path = dir_path/file_name

def display_next():
    global start_index 
    global img_lbl
    start_index += 1
    file_name = df.iloc[start_index]['name']
    file_path = dir_path/file_name

    img = Image.open(file_path)
    img.thumbnail((500, 500), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(img)
    img_lbl = ttk.Label(mainframe, image=img)
    img_grid = img_lbl.grid(row=0, column=0, rowspan=40)


def display_prev():
    pass

# TODO: After we label them update DataFrame with new values.
# TODO: If any of label related coulums are actually not labeled yes(valu is -1) grey out radiobutton

# Open and resize image
img = Image.open(file_path)
img.thumbnail((500, 500), Image.ANTIALIAS)

# Creating main class(window) and title
root = Tk()
root.title("LabelMe" + " - " + Path(file_name).name)

# Creating frame widget which will hold all the content of our user interface
mainframe = ttk.Frame(root, padding="5")
mainframe.grid(row=0, column=0)

# The "columnconfigure"/"rowconfigure" bits just tell Tk that if the main window is resized
# the frame should expand to take up the extra space.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Style
s = ttk.Style()
s.theme_use("clam")

# Creating labels, buttons, radiobuttons
img = ImageTk.PhotoImage(img)
img_lbl = ttk.Label(mainframe, image=img)
img_grid = img_lbl.grid(row=0, column=0, rowspan=40)

ttk.Label(mainframe, text="Watch face visibility:").grid(row=34, column=1, sticky=(W, N))
watch_face_vis = IntVar()
ttk.Radiobutton(mainframe, text="1", variable=watch_face_vis, value=1).grid(row=34, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0.5", variable=watch_face_vis, value=0.5).grid(row=34, column=3, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0", variable=watch_face_vis, value=0).grid(row=34, column=4, sticky=(W, N))

ttk.Label(mainframe, text="Composition quality:").grid(row=35, column=1, sticky=(W, N))
comp_quality = IntVar()
ttk.Radiobutton(mainframe, text="1", variable=comp_quality, value=1).grid(row=35, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0.5", variable=comp_quality, value=0.5).grid(row=35, column=3, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0", variable=comp_quality, value=0).grid(row=35, column=4, sticky=(W, N))

ttk.Label(mainframe, text="Lighting quality:").grid(row=36, column=1, sticky=(W, N))
lght_quality = IntVar()
ttk.Radiobutton(mainframe, text="1", variable=lght_quality, value=1).grid(row=36, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0", variable=lght_quality, value=0).grid(row=36, column=3, sticky=(W, N))

ttk.Label(mainframe, text="Image quality:").grid(row=37, column=1, sticky=(W, N))
img_quality = IntVar()
ttk.Radiobutton(mainframe, text="1", variable=img_quality, value=1).grid(row=37, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0", variable=img_quality, value=0).grid(row=37, column=3, sticky=(W, N))

ttk.Button(mainframe, text="Prev").grid(row=38, column=1, columnspan=1, sticky=())
ttk.Button(mainframe, text="Next", command=display_next).grid(row=38, column=2, columnspan=3, sticky=())
#ttk.Button(mainframe, text="Save").grid(row=39, column=1, columnspan=2, sticky=(W))
#ttk.Button(mainframe, text="Exit").grid(row=39, column=3, columnspan=2, sticky=(E))
#ttk.Label(mainframe, text="Status bar", relief=SUNKEN).grid(row=40, column=4, columnspan=4, sticky=(E))
# TODO: Status bar
 
# Walks through all of the widgets in mainframe and add padding around each
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


root.mainloop()
