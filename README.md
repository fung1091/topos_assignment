
# TOPOS INTERN ASSIGNMENT

We are scraping the first table from "wikipedia", the link of datasource is from "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population", it contains several of table, we determine to extract the first one for this assignment. 

In this assignment, the python3 will be used to extract, clean and generate csv file for the next part in "BigQuery table". 


```python
#load libraries
import numpy as np
import requests
import bs4 as bs
import pandas as pd
import os
import codecs
```


```python
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
```


```python
# cleaning

frame1 = pd.DataFrame(data)
frame1 = frame1.iloc[:314, 1:11]

# remove "\n" symbol
frame1 = frame1.replace('\n','',regex=True)
frame1.columns = ['city','state','2018_estimate','2010_census','change','2016_land_area1','2016_land_area2','2016_pop_den1', '2016_pop_den2', 'loc']
frame1['city'] = frame1['city'].str.split('[').str[0]
```


```python
display(frame1.head())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>state</th>
      <th>2018_estimate</th>
      <th>2010_census</th>
      <th>change</th>
      <th>2016_land_area1</th>
      <th>2016_land_area2</th>
      <th>2016_pop_den1</th>
      <th>2016_pop_den2</th>
      <th>loc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>New York City</td>
      <td>New York</td>
      <td>8,398,748</td>
      <td>8,175,133</td>
      <td>+2.74%</td>
      <td>301.5 sq mi</td>
      <td>780.9 km2</td>
      <td>28,317/sq mi</td>
      <td>10,933/km2</td>
      <td>40°39′49″N 73°56′19″W﻿ / ﻿40.6635°N 73.9387°W﻿...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Los Angeles</td>
      <td>California</td>
      <td>3,990,456</td>
      <td>3,792,621</td>
      <td>+5.22%</td>
      <td>468.7 sq mi</td>
      <td>1,213.9 km2</td>
      <td>8,484/sq mi</td>
      <td>3,276/km2</td>
      <td>34°01′10″N 118°24′39″W﻿ / ﻿34.0194°N 118.4108°...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Chicago</td>
      <td>Illinois</td>
      <td>2,705,994</td>
      <td>2,695,598</td>
      <td>+0.39%</td>
      <td>227.3 sq mi</td>
      <td>588.7 km2</td>
      <td>11,900/sq mi</td>
      <td>4,600/km2</td>
      <td>41°50′15″N 87°40′54″W﻿ / ﻿41.8376°N 87.6818°W﻿...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Houston</td>
      <td>Texas</td>
      <td>2,325,502</td>
      <td>2,100,263</td>
      <td>+10.72%</td>
      <td>637.5 sq mi</td>
      <td>1,651.1 km2</td>
      <td>3,613/sq mi</td>
      <td>1,395/km2</td>
      <td>29°47′12″N 95°23′27″W﻿ / ﻿29.7866°N 95.3909°W﻿...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Phoenix</td>
      <td>Arizona</td>
      <td>1,660,272</td>
      <td>1,445,632</td>
      <td>+14.85%</td>
      <td>517.6 sq mi</td>
      <td>1,340.6 km2</td>
      <td>3,120/sq mi</td>
      <td>1,200/km2</td>
      <td>33°34′20″N 112°05′24″W﻿ / ﻿33.5722°N 112.0901°...</td>
    </tr>
  </tbody>
</table>
</div>



```python
# Create CSV file
frame1.to_dense().to_csv("assignment.csv", index = False, sep=',', encoding='utf-8')
```


```python

```

# Part 2 - CSV in GCP - Bigquery

![Screenshot](https://raw.githubusercontent.com/fung1091/topos_assignment/blob/master/assignment1.png)
