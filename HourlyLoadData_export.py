import numpy as np
import pandas as pd
from datetime import datetime as dt

## Load data
filePath = 'N:\\HVAC_ModelicaModel_Data\\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States\\Original Data\\USA_CA_Oakland.Intl.AP.724930_TMY3'
fileName = 'RefBldgLargeOfficeNew2004_7.1_5.0_3C_USA_CA_SAN_FRANCISCO.csv'
file = filePath + '\\' + fileName

df = pd.read_csv(file)
df = df[['Date/Time','Electricity:Facility [kW](Hourly)']]

## Parse data
# Check document for string to date
# https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
def parseDatetime(timeStr):
    return dt.strptime(timeStr,' %m/%d  %H:%M:%S')

# Adjust units: kW to W
# df['Electricity:Facility [kW](Hourly)'] = df['Electricity:Facility [kW](Hourly)'] * 1000

# Format the time
df.drop(index = len(df)-1,inplace = True) # last day at 24:00:00 is next year!
# 24:00:00 is next day's 00:00:00
for i in range(23,len(df),24):
    df['Date/Time'].loc[i] = df['Date/Time'].loc[i+1][:8] + '00:00:00'

    
timeCol = df['Date/Time'].apply(parseDatetime)
loadData = df['Electricity:Facility [kW](Hourly)']

# dt.strftime(timeCol[0], '%H:%M:%S')



# Reformulate our time-temp data into a table
# could use reshape method, but will lose the indices of columns and rows
for i in range(0,len(timeCol),24):
    if i == 0: # first column
        newCol = loadData[:24]
        newCol.name = dt.strftime(timeCol[i],'%m-%d')
        newCol.index = range(1,len(newCol)+1)
        table = newCol
    else:
        newCol = loadData[i:(i+24)]
        newCol.name = dt.strftime(timeCol[i],'%m-%d')
        newCol.index = range(1,len(newCol)+1)
        table = pd.concat([table,newCol],axis = 1)
# Save file
table.to_csv('N:\\HVAC_ModelicaModel_Data\\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States\\SF_LargeOfficeNew2004.csv')


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
plt.fill_between(xs,avg,avg+sd, color = 'blue', alpha = 0.2)
plt.plot(xs,avg - sd, color = 'blue',alpha = 0.5)
plt.fill_between(xs,avg,avg-sd, color = 'blue', alpha = 0.2)
plt.plot(xs,firstQ, color = 'red', linestyle = 'dashed',alpha = 0.5,label = '_nolegend_')
plt.plot(xs,thirdQ, color = 'red', linestyle = 'dashed',alpha = 0.5,label = '_nolegend_')
plt.fill_between(xs,firstQ,thirdQ,color = 'red',alpha = 0.2,label = '1st and 3rd Quantile')


plt.xlabel('time[hour]')
plt.ylabel('energy load[W]')
plt.legend()

plt.show()

## Modelica TimeTable place holder matrix
# generate new table data from file
newTable = '['
i = 0
for t in table['05-01']:
    newTable += str(i*3600) + ','  + str(round(t,2)) + '; '
    i += 1
newTable = newTable[:-2] + ']'















