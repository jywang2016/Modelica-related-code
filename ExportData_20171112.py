from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
from pyjmi.common.plotting import plot_gui 

model_name = 'TestSys.HVACv3a'
mo_file1 = 'C:\Users\James\OneDrive\Documents\Berkeley\HVAC\Modelica\Test\TestSys\TestSys'
mo_file2 = 'C:\Users\James\Desktop\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2

fmu = compile_fmu(model_name,mo_files)
model = load_fmu(fmu)
res = model.simulate(final_time = 3600.)

##

import numpy as np
import matplotlib.pyplot as plt

## Read file
fileName = 'C:\\Users\\Public\\Documents\\JModelica.org\\TestSys_HVACv3a_result'

# with open(fileName + '.txt') as f:
#     read_data = f.read()
# f.closed

## Get variable names
variables = res.keys() # list of variable names

## Save all data to file
# initialize
dataArr = np.zeros((len(variables),len(res[variables[0]])+1),dtype = np.object)
varArr = list()

for i in range(len(variables)):
    varArr.append(variables[i])
    dataArr[i,1:] = res[variables[i]]
    # if res.is_variable(variables[i]): # choose variables only, constants are left out
    #     dataArr.append(res[variables[i]])
    #     varArr.append(variables[i])

dataArr[:,0] = np.array(varArr)
# varArr = np.array(varArr)
# dataArr = np.concatenate((np.array(variables).reshape(len(variables),1),dataArr), axis = 0)
np.savetxt(fileName + '.csv', dataArr,fmt = '%s',delimiter = ',') # don't forget the format '%s'



## Save variable names (and description) with order number to txt file
# save to txt file
varArr = np.zeros((len(variables[0]),3),dtype = np.object)
varArr[:,0] = np.arange(len(variables[0]))
varArr[:,1] = variables[0]
varArr[:,2] = variables[1]

np.savetxt(fileName + '_variables.txt', varArr,fmt = '%s',delimiter = '\t\t')

## Get variables in JModelica pylab

# load existing result file
from pyfmi.common.io import ResultDymolaTextual
# initialize
dataAllx = list()
dataAllt = list()
maxLen = 0 # record the longest sequence length
resData = ResultDymolaTextual(fileName+'.txt')
for i in range(len(variables[0])-1):
    data = resData.get_variable_data(variables[0][i])
    dataAllx.append(data.x)
    dataAllt.append(data.t)
    maxLen = len(data.x) if len(data.x) > maxLen else maxLen


## Save all data to csv file (This is not recommended)

# # initialize output array
# dataArr = np.zeros((maxLen+1,2*(len(variables[0,:])-1)),dtype = np.object) # Set dtype beforehand, conversion later causes error for large arrays
# # header
# header = list()
# # fill in data and pad with NAN for empty entries, (var_time|var_value)
# for i in range(len(variables[0])-1):
#     dataArr[1:,2*i] = np.pad(dataAllt[i],(0,maxLen-len(dataAllt[i])),mode='constant',constant_values=np.nan)
#     dataArr[1:,2*i+1] = np.pad(dataAllx[i],(0,maxLen-len(dataAllx[i])),mode='constant',constant_values=np.nan)
#     header.append(variables[0,i]+'.t')
#     header.append(variables[0,i]+'.x')
# # Add header to top row
# header = np.array(header)
# dataArr[0] = header
# 
# # save to csv file
# np.savetxt(fileName + '.csv', dataArr,fmt = '%s',delimiter = ',') # don't forget the format '%s'


## Save all data to csv file, saving only one copy of time(reduces half of storage space)

# # initialize output array
# dataArr = np.zeros((maxLen+1,len(variables[0,:])-1),dtype = np.object) # Set dtype beforehand, conversion later causes error for large arrays
# # header
# header = list()
# # fill in data and pad with NAN for empty entries, (var_time|var_value)
# # first column must be time(both var.x and var.t, which are identical copies), no need to store '.t'
# # dataArr[1:,0] = np.pad(dataAllt[0],(0,maxLen-len(dataAllt[0])),mode='constant',constant_values=np.nan)
# # header.append(variables[0,0])
# for i in range(len(variables[0])-1):
#     dataArr[1:,i] = np.pad(dataAllx[i],(0,maxLen-len(dataAllx[i])),mode='constant',constant_values=np.nan)
#     header.append(variables[0,i])
# # Add header to top row
# header = np.array(header)
# dataArr[0] = header
# 
# # save to csv file
# dataArr = dataArr.transpose() # Optional
# np.savetxt(fileName + '.csv', dataArr,fmt = '%s',delimiter = ',') # don't forget the format '%s'


