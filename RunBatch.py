from pymodelica import compile_fmu
from pyfmi import load_fmu
import numpy as np


# Model files
model_name = 'TestSys.HVACv3a'
mo_file1 = 'C:\\Users\\James\\OneDrive\\Documents\\Berkeley\\HVAC\\Modelica\\Test\\TestSys\\TestSys'
mo_file2 = 'C:\\Users\\James\\Desktop\\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2

# File path
filePath = 'C:\\Users\\Public\\Documents\\JModelica.org\\'
fileName = (model_name).replace('.','_')

# Compile FMU, can skip if already compiled before
fmu = compile_fmu(model_name,mo_files)

# set parameter
param = 'TemperatureSetpoint.k'
param_range = np.linspace(273.15+20,273.15+30,6)
# run time
start_time = 0.
final_time = 3600.
# run simulations
for param_val in param_range:
    model = load_fmu(fmu) # if fmu already compiled, can use model = load_fmu(fileName+'.fmu')
    model.set(param,param_val)
    res = model.simulate(start_time = start_time, final_time = final_time)
    # export selected variables
    variables = SelectedVars(filePath+fileName + '_selected_variables')
    ExportVars(res,variables,filePath+fileName + '_' + str(param) + '_' + str(param_val))


## Functions

# Read in selected variables. 
# Input: fileName, Output: list of variable names
def SelectedVars(fileName):
    with open(fileName + '.txt') as f:
        read_data = f.read()
    f.closed
    variables = read_data.split('\n')
    return(variables)

# Export selected variables. 
# Input: res(model.simulation result), variables(list of variable names), fileName
# Saves selected variables' data to csv file
def ExportVars(res,variables,fileName):
    dataArr = np.zeros((len(variables),len(res[variables[0]])+1),dtype = np.object)
    varArr = list()
    
    for i in range(len(variables)):
        varArr.append(variables[i])
        dataArr[i,1:] = res[variables[i]]
    
    dataArr[:,0] = np.array(varArr)
    np.savetxt(fileName + '.csv', dataArr.transpose(),fmt = '%s',delimiter = ',')
    print(fileName + '.csv' + ' has been saved.')


# Save all data to file.
# Input: res(model.simulation result), fileName
# Saves all variables' data to csv file
def SaveAllData(res,fileName):
    variables = res.keys() # list of variable names
    # initialize
    dataArr = np.zeros((len(variables),len(res[variables[0]])+1),dtype = np.object)
    varArr = list()
    
    for i in range(len(variables)):
        varArr.append(variables[i])
        dataArr[i,1:] = res[variables[i]]
    
    dataArr[:,0] = np.array(varArr)
    np.savetxt(fileName + '.csv', dataArr.transpose(),fmt = '%s',delimiter = ',')
    print(fileName + '.csv' + ' has been saved.')








