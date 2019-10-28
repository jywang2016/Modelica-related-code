### Run simulation
from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
from pyjmi.common.plotting import plot_gui 

model_name = 'TestSys.ControlUnitType2Test'
mo_file1 = 'C:\Users\James\OneDrive\Documents\Berkeley\HVAC\Modelica\Test\TestSys\TestSys'
mo_file2 = 'C:\Users\James\Desktop\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2

fmu = compile_fmu(model_name,mo_files)
model = load_fmu(fmu)
res = model.simulate(final_time = 3600.)

### Save data to csv file

import numpy as np
import matplotlib.pyplot as plt

## File path
JM_result_path = 'C:\\Users\\Public\\Documents\\JModelica.org\\'
fileName = JM_result_path + (model_name+'_result').replace('.','_')

## Get variable names
variables = res.keys() # list of variable names

## Save all data to file
# initialize
dataArr = np.zeros((len(variables),len(res[variables[0]])+1),dtype = np.object)
varArr = list()

for i in range(len(variables)):
    varArr.append(variables[i])
    dataArr[i,1:] = res[variables[i]]
    # choose variables only, constants are left out
    # if res.is_variable(variables[i]):
    #     dataArr.append(res[variables[i]])
    #     varArr.append(variables[i])

dataArr[:,0] = np.array(varArr)
np.savetxt(fileName + '.csv', dataArr,fmt = '%s',delimiter = ',')

## Save variable names (without description) to txt file
# save to txt file
varArr = np.zeros((len(variables),2),dtype = np.object)
varArr[:,0] = np.arange(len(variables))
varArr[:,1] = np.array(variables)

np.savetxt(fileName + '_variables.txt', varArr,fmt = '%s',delimiter = '\t\t')







### Read simulation result file and get variable list with description


## Read file
# fileName = 'C:\\Users\\Public\\Documents\\JModelica.org\\TestSys_HVACv3_result'

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

np.savetxt(fileName + '_variables_des.txt', varArr,fmt = '%s',delimiter = '\t\t')


