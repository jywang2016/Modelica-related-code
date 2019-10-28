## Imports
from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
from scipy.io.matlab import savemat
# from pyjmi.common.plotting import plot_gui

## Model loading and simulation

model_name = 'TestSys.BoilerTest'
# load multiple *.mo files, loading model with Buildings library!
mo_file1 = 'C:\Users\James\OneDrive\Documents\Berkeley\HVAC\Modelica\Test\TestSys\TestSys'
mo_file2 = 'C:\Users\James\Desktop\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2
# mo_files = 'C:\Users\James\OneDrive\Documents\Berkeley\HVAC\Modelica\Test\TestSys\TestSys,C:\Users\James\Desktop\Buildings 4.0.0'

fmu = compile_fmu(model_name,mo_files)
model = load_fmu(fmu)
res = model.simulate(final_time = 100.)

## JModelica PlotGUI
from pyjmi.common.plotting import plot_gui
plot_gui.startGUI()


## Plot
t = res['time']
T = res['boi.T']
plt.figure(1)
plt.plot(t,T)
plt.grid(True)
plt.legend(['Temperature'])
plt.xlabel('time [s]')
plt.ylabel('Temperature [degC]')
plt.show()

## Save *.mat

savemat("res.mat", dict(res))