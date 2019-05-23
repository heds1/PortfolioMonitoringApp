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
import urllib
import json
import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt

#tickers = ['NZB.NZ', 'USF.NZ', 'GBF.NZ', 'FNZ.NZ', 'SPY']
tickers = ['SPY','F']
start_date = '2010-01-01'
end_date = pd.to_datetime('today')
panel_data = data.DataReader(tickers, 'google', start_date, end_date)
close = panel_data.ix['Close']
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')  # replace NAs with last closing value
# close.tail(10)
#NZX50 = close.ix[:, 'FNZ.NZ']
NZX50 = close.ix[:, 'SPY']
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(NZX50.index, NZX50, label='NZX50 Index')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def closeProgram():
   app.destroy()

def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataArray = pullData.split("\n")
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x, y = eachLine.split(",")
            xar.append(int(x))
            yar.append(int(y))
    a.clear()
    a.plot(xar, yar)

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func



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
        
        self.app_data = {"apiOptions": StringVar()}
        
        self.frames = {}
        for F in (AgreementPage, HomePage, NZX50Index, TestPage):
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
        Still under development. Last updated 29 July 2017 by H.L.S.
        Use at your own risk.
        Select the desired API from the dropdown menu.
        """, font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.controller = controller
        
        apiOptions = tk.StringVar(self)
        apiOptions.set("Yahoo")
        apiOptionsMenu = tk.OptionMenu(self, apiOptions, "Yahoo", "Google", "Another API")
        apiOptionsMenu.pack()
        
        #button3 = ttk.Button(self, text="Load API data",
            #                 command= lambda: load_api_data)
        
        button1 = ttk.Button(self, text="Proceed",
                            command= lambda: controller.show_frame(HomePage))
        button1.pack()
        button2 = ttk.Button(self, text="Exit",
                            command=closeProgram)
        button2.pack()           
    
        
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label1.pack(pady=10,padx=10)        
        #AgreementPage.get_chosenApi)
        
        #label2 = tk.Label(self, text="Chosen API is" apiOptions.get())
        #label2.pack()
        button1 = ttk.Button(self, text="TestPage",
                            command=lambda: controller.show_frame(TestPage))
        button1.pack()
        button2 = ttk.Button(self, text="NZX50 Index",
                            command=lambda: controller.show_frame(NZX50Index))
        button2.pack()   
        button3 = ttk.Button(self, text="Exit",
                             command=closeProgram)
        button3.pack()
 #       apiString()
        
class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Test Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
             
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

class NZX50Index(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="NZX50Index", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()
                
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        


        
        
app = PortfolioMonitorApp()
ani = animation.FuncAnimation(f,animate, interval=10000) #10,000 ms between updates
app.mainloop()
        
#%%