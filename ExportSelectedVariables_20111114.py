import numpy as np
import matplotlib.pyplot as plt

## File name/path
model_name = 'TestSys.ControlUnitType2Test'
JM_result_path = 'C:\\Users\\Public\\Documents\\JModelica.org\\'
fileName = JM_result_path + (model_name).replace('.','_') + '_selected_variables'

## Read txt variable list

with open(fileName + '.txt') as f:
    read_data = f.read()
f.closed

variables = read_data.split('\n')

## Export selected variables

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


