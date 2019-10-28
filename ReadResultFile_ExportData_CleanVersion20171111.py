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
    splitData = data.split('\n')
    list_data.append(data)
    list_splitdata.append(splitData)

# variables 1st row are the variable names, 2nd row are variable descriptions
variables = np.array(list_splitdata[:2])[:,1:]
# remove system variables (not our interest)
mask = list() # intialize delete mask
for i in range(len(variables[0])-1):
    if variables[0][i][0] == '_' or variables[0][i] == '':
        mask.append(i)
variables = np.delete(variables,mask,axis=1)

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

# initialize output array
dataArr = np.zeros((maxLen+1,len(variables[0,:])-1),dtype = np.object) # Set dtype beforehand, conversion later causes error for large arrays
# header
header = list()
# fill in data and pad with NAN for empty entries, (var_time|var_value)
# first column must be time(both var.x and var.t, which are identical copies), no need to store '.t'
# dataArr[1:,0] = np.pad(dataAllt[0],(0,maxLen-len(dataAllt[0])),mode='constant',constant_values=np.nan)
# header.append(variables[0,0])
for i in range(len(variables[0])-1):
    dataArr[1:,i] = np.pad(dataAllx[i],(0,maxLen-len(dataAllx[i])),mode='constant',constant_values=np.nan)
    header.append(variables[0,i])
# Add header to top row
header = np.array(header)
dataArr[0] = header

# save to csv file
dataArr = dataArr.transpose() # Optional
np.savetxt(fileName + '.csv', dataArr,fmt = '%s',delimiter = ',') # don't forget the format '%s'


