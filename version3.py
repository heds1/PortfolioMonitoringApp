# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 20:34:41 2017

@author: Hedley Stirrat

New version of portfolio monitoring app.

"""
#%%

import tkinter as tk
from tkinter import ttk

def closeProgram():
    app.destroy()
    
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, "clienticon.ico")
        tk.Tk.wm_title(self, "Portfolio monitoring app version 3")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LoadingPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoadingPage)
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        
class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(text="Select your desired API")
        label.pack(pady=10, padx=10)
     
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
app = App()
app.mainloop()

        