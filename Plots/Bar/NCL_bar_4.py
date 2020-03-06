#Lily's version of the NCL example bar_4.ncl
#This is a work in progress

#import packages
import numpy as np
import xarray as xr

import matplotlib.pyplot as plt

import geocat.datafiles as gdf

#read data file
dataf = xr.open_dataset(gdf.get('netcdf_files/SOI.nc'), decode_times=False)

data = dataf.SOI_SIGNAL[0:dataf.time.size]


#print(dataf)

#print(data)

def bar_color(df,color1,color2):
    return np.where(df.values>0,color1,color2).T

fig = plt.figure(figsize=(5,5))
ax = plt.gca()

colorlist = ['red', 'orange', 'yellow', 'green', 'blue', 'navyblue', 'purple']
x = dataf.yyyymm[:] / 100.0

#print(x)

#print(dataf.time.size)

plt.bar(x,data,edgecolor=bar_color(data,'red','blue'))

plt.xticks(np.arange(min(x),max(x),20))
plt.ylabel('Anomalies')
plt.title('Darwin Southern Oscillation Index')

plt.show()
