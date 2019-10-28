# import numpy as np
import pandas as pd
from datetime import datetime as dt
# import matplotlib.pyplot as plt

filePath = 'N:\\HVAC_ModelicaModel_Data\\NOAA_WeatherData\\OriginalData'
fileName = 'NOAA_SF_2010[1259616].csv'
file = filePath + '\\' + fileName

df = pd.read_csv(file)
df = df[['DATE','HLY-TEMP-NORMAL']] # Hourly temperature mean

# Check document for string to date
# https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

# dt.datetime.strptime('2010-'+df['DATE'][0],'%Y-%m-%dT%H:%M:%S')
def parseDatetime(timeStr):
    return dt.strptime(timeStr,'%Y-%m-%dT%H:%M:%S')

# Adding year at the front of df['DATE']
timeData = ('2010-'+df['DATE']).apply(parseDatetime)
tempData = df['HLY-TEMP-NORMAL']

# plt.plot(timeData,tempData)
# plt.show()

# ===============================================================
# Pandas: merge/join
# https://pandas.pydata.org/pandas-docs/stable/merging.html
# Note the differences of merge, join, concat, append
# ===============================================================


# Thes two give the same result
# df = pd.DataFrame({'time': timeData,'temperature':tempData})
df = pd.concat([timeData,tempData],axis = 1)

# ===============================================================
# numpy reshape order
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html#numpy.reshape
# ===============================================================
# x = pd.DataFrame(tempData[:8664].reshape((24,361),order = 'F'))
# y = pd.DataFrame(timeData[:8664].reshape((24,361),order = 'F'))


# Reformulate our time-temp data into a table
# could use reshape method, but will lose the indices of columns and rows
for i in range(0,len(timeData),24):
    if i == 0: # first column
        newCol = tempData[:24]
        newCol.name = dt.strftime(timeData[i],'%Y-%m-%d')
        newCol.index = range(1,len(newCol)+1)
        table = newCol
    else:
        newCol = tempData[i:(i+24)]
        newCol.name = dt.strftime(timeData[i],'%Y-%m-%d')
        newCol.index = range(1,len(newCol)+1)
        table = pd.concat([table,newCol],axis = 1)
    

# Transform degrees Celsius to Kelvins
table = table + 273.15

# Save file
table.to_csv(filePath + '\\TemperatureData.csv')


## Plot
import matplotlib.pyplot as plt

avg = table.mean(axis = 1)
sd = table.std(axis = 1)
xs = range(1,25)
firstQ = table.quantile(q = 0.25,axis = 1) # 1st quantile
thirdQ = table.quantile(q = 0.75,axis = 1) # 3rd quantile
# Draw curve
plt.plot(xs,avg,'k',label = 'Annual average load')
plt.plot(xs,avg + sd, color = 'blue',alpha = 0.5,label ='Standard deviation')
plt.fill_between(xs,avg,avg+sd, color = 'blue', alpha = 0.3)
plt.plot(xs,avg - sd, color = 'blue',alpha = 0.5)
plt.fill_between(xs,avg,avg-sd, color = 'blue', alpha = 0.3)
# plt.plot(xs,firstQ, color = 'red', linestyle = 'dashed',alpha = 0.5,label = '_nolegend_')
# plt.plot(xs,thirdQ, color = 'red', linestyle = 'dashed',alpha = 0.5,label = '_nolegend_')
plt.fill_between(xs,firstQ,thirdQ,color = 'red',alpha = 0.3,label = '1st and 3rd Quantile')


plt.xlabel('time[hour]')
plt.ylabel('Temperature[K]')
plt.legend()

plt.show()



