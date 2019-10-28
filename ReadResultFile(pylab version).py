import numpy as np
import matplotlib.pyplot as plt


## Read file
fileName = 'C:\\Users\\Public\\Documents\\JModelica.org\\TestSys_ControlUnitTest_result.txt'

with open(fileName) as f:
    read_data = f.read()
f.closed

## Get variable names
# split data
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

#  variables 1st row are the variable names, 2nd row are variable descriptions
variables = np.array(list_splitdata[0])[2:]
#  remove system variables (not our interest)
mask = list() # intialize delete mask
for i in range(len(variables)-1):
    if variables[i][0] == '_':
        mask.append(i)

variables = np.delete(variables,mask)

## Get variables in JModelica pylab

# Cannot access data by doing this...
# ------------------------------------
# for i in range(len(variables)-1):
#     result.append(res[variables[i]])
# ------------------------------------

# load existing result file
from pyfmi.common.io import ResultDymolaTextual
# initialize
dataAllx = list()
dataAllt = list()
resData = ResultDymolaTextual(fileName)
for i in range(len(variables)-1):
    data = resData.get_variable_data(variables[i])
    dataAllx.append(data.x)
    dataAllt.append(data.t)

lookupDic = dict(zip(list(variables),range(len(variables))))
var_index = lookupDic['controlUnit1.yHeating']

plt.plot(dataAllt[var_index],dataAllx[var_index])

## Found this! Seems to work!!!
# load existing result file

res = ResultDymolaTextual("MyResult.txt")

var = res.get_variable_data("MyVariable")

var.x #Trajectory
var.t #Corresponding time vector



##
# Found at
# https://stackoverflow.com/questions/32030069/what-is-the-format-of-jmodelica-result-file-name-output
# this doesn't seem to work
with open(filename,'w') as fout:
    #Print all variables at the top of the file, along with relevant information
    #about them.
    for var in result.model.getAllVariables():
      if not result.is_variable(var.getName()):
        val = result.initial(var.getName())
        col = -1
      else:
        val = "Varies"
        col = result.get_column(var.getName())

      unit = StripMX(var.getUnit())
      if not unit:
        unit = "X"

      fout.write(varstr.format(
        name    = var.getName(),
        unit    = unit,
        val     = val,
        col     = col,
        comment = StripMX(var.getAttribute('comment'))
      ))

## doesn't work....
res.result_data.get_variable_data(1)
res.result_data.get_variable_index('time')




















