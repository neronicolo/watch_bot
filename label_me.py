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
file_path = dir_path/df['name'][11]
# Open and resize image
img = Image.open(file_path)
img.thumbnail((500, 500), Image.ANTIALIAS)

# Creating main class(window) and title
root = Tk()
root.title("LabelMe")

# Creating frame widget which will hold all the content of our user interface
mainframe = ttk.Frame(root, padding="5")
mainframe.grid(row=0, column=0)

# The "columnconfigure"/"rowconfigure" bits just tell Tk that if the main window is resized
# the frame should expand to take up the extra space.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Creating labels, buttons, radiobuttons
img = ImageTk.PhotoImage(img)
ttk.Label(mainframe, image=img).grid(row=0, column=0, rowspan=40)

ttk.Label(mainframe, text="Watch face visibility:").grid(row=0, column=1, sticky=(W, N))
watch_face_vis = IntVar()
ttk.Radiobutton(mainframe, text="1", variable=watch_face_vis, value=1).grid(row=0, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0.5", variable=watch_face_vis, value=0.5).grid(row=0, column=3, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0", variable=watch_face_vis, value=0).grid(row=0, column=4, sticky=(W, N))

ttk.Label(mainframe, text="Composition quality:").grid(row=1, column=1, sticky=(W, N))
ttk.Radiobutton(mainframe, text="1").grid(row=1, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0.5").grid(row=1, column=3, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0").grid(row=1, column=4, sticky=(W, N))

ttk.Label(mainframe, text="Lighting quality:").grid(row=2, column=1, sticky=(W, N))
ttk.Radiobutton(mainframe, text="1").grid(row=2, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0").grid(row=2, column=3, sticky=(W, N))

ttk.Label(mainframe, text="Image quality:").grid(row=3, column=1, sticky=(W, N))
ttk.Radiobutton(mainframe, text="1").grid(row=3, column=2, sticky=(W, N))
ttk.Radiobutton(mainframe, text="0").grid(row=3, column=3, sticky=(W, N))

#ttk.Button(mainframe, text="<<").grid(row=8, column=1)
#ttk.Button(mainframe, text=">>").grid(row=8, column=2)
#ttk.Button(mainframe, text="Save").grid(row=9, column=1)
#ttk.Button(mainframe, text="Exit").grid(row=9, column=2)
# TODO: Radionbuttons
# TODO: Status bar

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
