import tkinter as tk
from tkinter import ttk

class Application(tk.ttk.Frame):
    def __init__(self, dir, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.dir = dir
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        print(self.dir)

dir = 'test'
root = tk.Tk()
app = Application(dir, master=root, padding=5)
app.mainloop()