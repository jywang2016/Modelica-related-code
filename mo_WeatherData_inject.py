'''
This script is used to modify the values of TimeTable component, WeatherData, in HVACv3a_weather.mo
For CombiTimeTable doesn't work in this model for some reason(don't ask me why).
One of our approach is to modify the values in the editor(OMC) manually, another
way is to use JModelica's pylab interface, which uses python, to modify the mo file directly.
A third method is to access the WeatherData.table variable in pylab(see "TimeTable_read_external.py")

Compared with "TimeTable_read_external.py", this method is more straightforward and doesn't
need a place holder matrix as "TimeTable_read_external.py" needs.
The drawback is the mo file has to be recompiled to a FMU everytime we change WeatherData,
which can be very time consuming.

'''

import numpy as np
import pandas as pd
# from datetime import datetime as dt
# import matplotlib.pyplot as plt

filePath = 'N:\\HVAC_ModelicaModel_Data\\NOAA_WeatherData'
fileName = 'Boston2010_TemperatureData.csv'#'SF2010_TemperatureData.csv'
weather_file = filePath + '\\' + fileName

filePath = 'C:\\Users\\James\\\OneDrive\\Documents\\Berkeley\\HVAC\\Modelica\\Test\\TestSys\\TestSys'
fileName = 'HVACv3a_weather.mo'
mo_file = filePath + '\\' + fileName

weatherDate = '2010-07-15'
weatherData = pd.read_csv(weather_file)

# read in modelica code
with open(mo_file,'r') as f:
    mo_code = f.readlines()

# locate the table data in modelica code
line = mo_code[51]
startIndex = line.find('table = [')
endIndex = line.find(']',startIndex) + 1

# generate new table data from file
newTable = 'table = ['
i = 0
for t in weatherData[weatherDate]:
    newTable += str(i*3600) + ','  + str(round(t,2)) + '; '
    i += 1
newTable = newTable[:-2] + ']'

# replace old data with new weather data
newLine = line.replace(line[startIndex:endIndex],newTable)
mo_code[51] = newLine

# write to file
with open(mo_file,'w') as f:
    f.writelines(mo_code)

