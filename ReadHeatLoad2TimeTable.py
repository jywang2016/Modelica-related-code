'''
This script is used to modify the values of TimeTable component, RoomLoadData, in HVACv3a_weather_load.mo
For CombiTimeTable doesn't work in this model for some reason(don't ask me why).
One of our approach is to modify the values in the editor(OMC) manually, another
way is to use JModelica's pylab interface, which uses python, to modify the mo file directly.(See "mo_WeatherData_inject.py"
A third method is to access the WeatherData.table variable in pylab.
'''

import numpy as np # JMoldelica.org's pylab only has numpy. Pandas is not supported

## Read in heat load data

filePath = 'N:\\HVAC_ModelicaModel_Data\\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States'
fileName = 'SF_LargeOfficeNew2004.csv'
load_file = filePath + '\\' + fileName
# weatherDate = '2010-06-23'

# load data
loadData = np.loadtxt(open(load_file, "rb"), delimiter=",", skiprows=1,dtype = np.object)
loadData[-1,-1] = 0 # last cell is empty(missing data)
loadData = np.array(loadData[:,1:],dtype = np.float)

day = 123 # loadData[:,day]
t = np.arange(0,3600*24,3600) # time 
mat = np.concatenate((t,loadData[:,day]))
mat = mat.reshape((24,2),order = 'F')
'''
# Note: putting weather data in such format is because we set the WeatherData's(TimeTable component)
# WeatherData.table with a value of a matrix with a [24,2] dimension.
# The value we set is a place holder, must comply to its matrix dimension to use this method,
# for the WeatherData.table vairable is already compiled into a FMU
'''

## Change the RoomLoadData parameter after loading the FMU(before model.simulate)
'''
# This part is used to check the variable format
filePath = 'D:'
fileName = 'modelVars.txt'
file = filePath + '\\' + fileName

var = model.get_model_variables()
varArr = np.array(var.keys())
np.savetxt(file,varArr,fmt='%s')
'''
# The matrix variable is saved as individual variables when in FMU(Don't ask me why)
# Thus, we have to change the matrix values element by elemnt in np.array class type
# e.g. WeatherData.table[11,2] = np.array[285]


for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        LD = 'RoomLoadData.table[' + str(i+1) + ',' + str(j+1) + ']'
        LD_val = np.array(mat[i,j])
        model.set(LD,LD_val)
    


# model.set('WeatherData.table[i,j]')