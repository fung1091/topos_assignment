#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 00:02:46 2019

@author: jim
"""

#load libraries
import numpy as np
import requests
import bs4 as bs
import pandas as pd
import os
import codecs

resp = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
soup = bs.BeautifulSoup(resp.text, 'lxml')
tables = soup.findAll('table', { 'class' : 'wikitable sortable' })[0]

rows=tables.findAll("tr")[1:315]
row_lengths=[len(r.findAll(['th','td'])) for r in rows]
ncols=max(row_lengths)
nrows=len(rows)
data=[]
for i in range(nrows):
    rowD=[]
    for j in range(ncols):
        rowD.append('')
    data.append(rowD)
    
# process html
for i in range(len(rows)):
    row=rows[i]
    rowD=[]
    cells = row.findAll(["td","th"])
    for j in range(len(cells)):
        cell=cells[j]
            
        #lots of cells span cols and rows so lets deal with that
        cspan=int(cell.get('colspan',1))
        rspan=int(cell.get('rowspan',1))
        for k in range(rspan):
            for l in range(cspan):
                data[i+k][j+l]+=cell.text
    
    data.append(rowD)
    
# cleaning

frame1 = pd.DataFrame(data)
frame1 = frame1.iloc[:314, 1:11]

# remove "\n" symbol
frame1 = frame1.replace('\n','',regex=True)
frame1.columns = ['city','state','2018_estimate','2010_census','change','2016_land_area1','2016_land_area2','2016_pop_den1', '2016_pop_den2', 'loc']
frame1['city'] = frame1['city'].str.split('[').str[0]

# Display

display(frame1.head())

# Create CSV file
frame1.to_dense().to_csv("assignment.csv", index = False, sep=',', encoding='utf-8')