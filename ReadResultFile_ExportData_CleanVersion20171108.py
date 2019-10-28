import numpy as np
import matplotlib.pyplot as plt

## Read file
fileName = 'C:\\Users\\Public\\Documents\\JModelica.org\\TestSys_HVACv3_result'

with open(fileName + '.txt') as f:
    read_data = f.read()
f.closed

## Get variable names
index_vars = read_data.find('char name')
index_vars_d = read_data.find('char description')
index_datainfo = read_data.find('int dataInfo')
index_fd1 = read_data.find('float data_1')
index_fd2 = read_data.find('float data_2')

list_index = [index_vars,index_vars_d,index_datainfo,index_fd1,index_fd2] # list of indices
list_index.append(len(read_data)-1)
list_data = list() # initialize list_data
list_splitdata = list() # initialize list_splitdata


for i in range(len(list_index)-1):
    data = read_data[list_index[i]:list_index[i+1]-1]
    splitData = data.split()
    list_data.append(data)
    list_splitdata.append(splitData)

# variables 1st row are the variable names, 2nd row are variable descriptions
variables = np.array(list_splitdata[0])[2:]
# remove system variables (not our interest)
mask = list() # intialize delete mask
for i in range(len(variables)-1):
    if variables[i][0] == '_':
        mask.append(i)
variables = np.delete(variables,mask)


## Get variables in JModelica pylab

# load existing result file
from pyfmi.common.io import ResultDymolaTextual
# initialize
dataAllx = list()
dataAllt = list()
maxLen = 0 # record the longest sequence length
resData = ResultDymolaTextual(fileName+'.txt')
for i in range(len(variables)):
    data = resData.get_variable_data(variables[i])
    dataAllx.append(data.x)
    dataAllt.append(data.t)
    maxLen = len(data.x) if len(data.x) > maxLen else maxLen

## Save all data to csv file

# initialize output array
dataArr = np.zeros((maxLen+1,2*len(variables)),dtype = np.object) # Set dtype beforehand, conversion later causes error for large arrays
# header
header = list()
# fill in data and pad with NAN for empty entries, (var_time|var_value)
for i in range(len(variables)):
    dataArr[1:,2*i] = np.pad(dataAllt[i],(0,maxLen-len(dataAllt[i])),mode='constant',constant_values=np.nan)
    dataArr[1:,2*i+1] = np.pad(dataAllx[i],(0,maxLen-len(dataAllx[i])),mode='constant',constant_values=np.nan)
    header.append(variables[i]+'.t')
    header.append(variables[i]+'.x')
# Add header to top row
header = np.array(header).reshape((1,len(header)))
dataArr[0] = header

# save to csv file
np.savetxt(fileName + '.csv', dataArr,fmt = '%s',delimiter = ',') # don't forget the format '%s'