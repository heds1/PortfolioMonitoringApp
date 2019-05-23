# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 17:58:51 2017

@author: Hedley Stirrat
"""

#%%
# Following Sentdex's Bitcoin trader GUI tutorial. Try to track NZX50 etc.

import tkinter as tk
from tkinter import ttk
#matplotlib.use("TkAgg")
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
#import urllib
#import json
import pandas as pd
import numpy as np

###TEST
from pandas_datareader import data
import matplotlib.pyplot as plt
tickers = ['NZB.NZ', 'USF.NZ', 'GBF.NZ', 'FNZ.NZ', 'SPY']
data_source = 'yahoo'
start_date = '2010-01-01'
end_date = pd.to_datetime('today')
panel_data = data.DataReader(tickers, data_source, start_date, end_date)
adj_close = panel_data.ix['Close']
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
adj_close = adj_close.reindex(all_weekdays)
adj_close = adj_close.fillna(method='ffill')  # replace NAs with last closing value
#adj_close.tail(10)
NZX50 = adj_close.ix[:, 'FNZ.NZ']
NZX50fig = plt.figure()
NZX50fig = NZX50fig.add_subplot(1,1,1)
NZX50fig.plot(NZX50.index, NZX50, label='NZX50 Index')
NZX50fig.set_xlabel('Date')
NZX50fig.set_ylabel('Adjusted closing price ($NZD)')
NZX50fig.legend()
###TEST


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def closeProgram():
   app.destroy()

class PortfolioMonitorApp(tk.Tk): # PMA class inheriting all attributes from
                                 # the tk.Tk class.
    def __init__(self, *args, **kwargs): # the __init__ method: everything
    # contained in this method will start when the PMA class is called.
        tk.Tk.__init__(self, *args, **kwargs) # initialising the inherited class
        tk.Tk.iconbitmap(self, "clienticon.ico")
        tk.Tk.wm_title(self, "Portfolio Monitoring App")
        #define the container: to be filled with a bunch of frames to be accessed
        #later on.
        container = tk.Frame(self) # the container contains everything basically
        container.pack(side="top", fill="both", expand=True) # fill will fill in
        # the space you've alotted the pack. Expand says, if there's anymore white
        # space in the window, you can expand if there's space.
        container.grid_rowconfigure(0, weight=1) # the "0" sets a minimum size,
        # weight = 1 sets a priority.
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (AgreementPage, HomePage, NZX50Index):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(AgreementPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont] # container
        frame.tkraise()
        
       
        
class AgreementPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # parent class i.e. PMA
        label = tk.Label(self, text="""Portfolio Monitoring Application. 
        This is in the beta stage. Use at your own discretion. Created by
        Hedley Stirrat. Last updated 24 July 2017.""", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
        button2 = ttk.Button(self, text="Disagree",
                            command=closeProgram)
        button2.pack()           
        
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button2 = ttk.Button(self, text="NZX50 Index",
                            command=lambda: controller.show_frame(NZX50Index))
        button2.pack()   
        button3 = ttk.Button(self, text="Exit",
                             command=closeProgram)
        button3.pack()

class NZX50Index(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="NZX50Index", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
                
        canvas = FigureCanvasTkAgg(NZX50fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = PortfolioMonitorApp()    
app.mainloop()
        
#%%