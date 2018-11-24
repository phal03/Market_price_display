# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:03:21 2018

@author: PHALGUNI
"""


from tkinter import *
import matplotlib.pyplot as plt
import time
import requests
import pandas as pd

class takeInput(object):

    def __init__(self,requestMessage):
        self.root = Tk()
        self.string = ''
        self.frame = Frame(self.root)
        self.frame.pack()        
        self.acceptInput(requestMessage)

    def acceptInput(self,requestMessage):
        r = self.frame

        k = Label(r,text=requestMessage)
        k.pack(side='left')
        self.e = Entry(r,text='Name')
        self.e.pack(side='left')
        self.e.focus_set()
        b = Button(r,text='okay',command=self.gettext)
        b.pack(side='right')

    def gettext(self):
        self.string = self.e.get()
        self.root.destroy()

    def getString(self):
        return self.string

    def waitForInput(self):
        self.root.mainloop()

def getText(requestMessage):
    msgBox = takeInput(requestMessage)
    #loop until the user makes a decision and the window is destroyed
    msgBox.waitForInput()
    return msgBox.getString()

comp_names = list()


for i in range(1,5):
    name = getText('Enter {} company name'.format(i))
    comp_names.append(name)
print (comp_names)


comp_names_hist = list()

for i in range(1,3):
    name = getText('Enter {} company name to view historical data'.format(i))
    comp_names_hist.append(name)
print(comp_names_hist)



###############################################################################
###### LIVE DATA FOR 4 COMPANIES
##Read data from file for extracting initials

symbols = []
xyz = []
sym = []

from fuzzywuzzy import process
datafile = pd.read_csv('nasdaq.csv')
inputfile = datafile['Input']
for i in comp_names:
    print(i)
    sym = process.extract(i, inputfile, limit = 1)
    xyz = sym[0]
    index = datafile.loc[lambda datafile: datafile['Input'] == xyz[0]]
    test = index['Symbol'].item();
    symbols.append(test)
    


###############################################################################
##Get data from API

use = {}
for symbol in symbols:
    from alpha_vantage.timeseries import TimeSeries
    ts = TimeSeries(key='12C2NM6XXMMCNM8S', output_format='pandas', indexing_type='integer')
    data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')
    print(symbol)
    use[symbol] = data.loc[:,['date','2. high']]
    print(data.loc[len(data)-1,'2. high'])
    #for high market price

    


fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
axes_list = ax.flatten()
axes_dict = {}

for i in range(len(symbols)):
    axes_dict[symbols[i]] = axes_list[i]

def make_axes(x,y,axes,symbl):
    axes.plot(y)
    axes.set_title("Current value of: "+str(symbl))
    axes.set_ylabel('Price')
    axes.set_xticks([])
    return(axes)
    
    
for symbol in symbols:
    y = use[symbol]['2. high'].tolist()
    x = use[symbol].date.tolist()
    axes_dict[symbol] = make_axes(x,y,axes_dict[symbol],symbol)
    
plt.show()

###############################################################################
###### HISTORICAL DATA FOR 2 COMPANIES
##Read data from file for extracting initials
symbols_hist = []
for i in comp_names_hist:
    print(i)
    sym = process.extract(i, inputfile, limit = 1)
    xyz = sym[0]
    index = datafile.loc[lambda datafile: datafile['Input'] == xyz[0]]
    test = index['Symbol'].item();
    symbols_hist.append(test)

###############################################################################
##Get data from API

time.sleep(61)
data_hist = {}
for symbol in symbols_hist:
    high_data = []
    month = []
    API_URL="https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY"\
    "&symbol="+str(symbol)+"&apikey=12C2NM6XXMMCNM8S"
    response = requests.get(API_URL) 
    data = response.json()
    print(symbol)
    a = (data['Monthly Time Series'])
    keys = (a.keys())
    months = []     
    for key in a.keys():
        months.append(key)
    #print(len(months))
    months = months[0:24]
    #print(len(months))
    for month in months:
        high_data.append(float(a[month]['2. high']))
    months.reverse()
    print(months)
    high_data.reverse()
    data_hist[symbol] = (months, high_data)  
    
fig_hist, ax_hist = plt.subplots(nrows=2, ncols=1, figsize=(30, 15))
axes_hist_list = ax_hist.flatten()
axes_hist_dict = {}

for i in range(len(symbols_hist)):
    axes_hist_dict[symbols_hist[i]] = axes_hist_list[i]


def make_axes_hist(x,y,axes,symbl):
    axes.plot(x,y,marker = "o")
    axes.set_title("Historical Value of "+str(symbl))
    axes.set_ylabel('Price')
    for i, txt in enumerate(y):
        axes.annotate(txt, (x[i], y[i]))
    return(axes)

    
for symbol in symbols_hist:
    y_hist = data_hist[symbol][1]
    x_hist = data_hist[symbol][0]
    axes_hist_dict[symbol] = make_axes_hist(x_hist,y_hist,
                                              axes_hist_dict[symbol],symbol)

plt.show()