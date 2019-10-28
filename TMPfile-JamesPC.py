from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
from pyjmi.common.plotting import plot_gui   # or pyfmi.common.plotting import plot_gui


model_name = 'TestSys.HVACv6a_3room'
mo_file1 = 'C:\Users\James\OneDrive\Documents\Berkeley\HVAC\Modelica\Test\TestSys\TestSys'
mo_file2 = 'C:\Users\James\Desktop\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2

# Compile fmu
fmu = compile_fmu(model_name,mo_files)

# Load fmu
model = load_fmu(fmu)
# if already compiled fmu, can use fmu from file and save time from recompiling
model = load_fmu(model_name.replace('.','_') + '.fmu')
# model = load_fmu('TestSys_HVACv3a_weather_load.fmu') # make sure working directory is correct

# model parameters setting
model.set(param,param_val)

# res = model.simulate(final_time = 3600.)
# res = model.simulate(start_time = 0., final_time = 3600.)
opts = model.simulate_options()
# opts['solver'] = 'RodasODE'#'RungeKutta34'#'Radau5ODE'#'CVode'
opts['ncp'] = 1440 # Changing the number of communication points
res = model.simulate(options=opts,start_time = 0., final_time = 86400.)

plot_gui.startGUI()


##

model_name = 'MyMedia.TwoTankTest'
# If the package is not in library form, then must assign the mo file instead of the directory
mo_file1 = 'C:\Users\James\OneDrive\Documents\Berkeley\HVAC\Modelica\Test\MyMedia.mo'
# If the package is in library form, then must assign the root directory
mo_file2 = 'C:\Users\James\Desktop\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2

fmu = compile_fmu(model_name,mo_files)


## 
# load existing result file
from pyfmi.common.io import ResultDymolaTextual

res = ResultDymolaTextual("MyResult.txt")

var = res.get_variable_data("MyVariable")

var.x #Trajectory
var.t #Corresponding time vector

# Example:
res = ResultDymolaTextual('TestSys_HVACv3a_weather_result.txt')
var = res.get_variable_data('ahu1.fanOA.m_flow')
print(var.x)



##
# Set compiler log level to 'info'
compile_fmu('myModel', 'myModels.mo', compiler_log_level='info')
'''
The available log levels are 'warning' (default), 'error', 'info','verbose' and 'debug' which can also be written as 'w', 'e', 'i','v' and 'd' respectively
'''

# Changing log level
model = load_fmu(fmu_name, log_level=5) # log_level = 0-7(7 is most verbose)
model.set_log_level(7) # change log level after loading is ok
model.set('_log_level', 6)

# Change output points, check JModelica UserGuide 2.0 page 32-33
opts = model.simulate_options() # Retrieve the default options
opts['ncp'] = 1000 # Changing the number of communication points.
opts['initialize'] = False # Don't initialize the model
model.simulate(options=opts) # Pass in the options to simulate and simulate

## Save model variables before simulating
modelVars = model.get_model_variables() # Dictionary type
modelVars = modelVars.keys() # List of names of variables
np.savetxt(model_name + '_[variable list].txt',modelVars,fmt='%s')





