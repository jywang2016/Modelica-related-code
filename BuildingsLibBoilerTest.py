from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
from pyjmi.common.plotting import plot_gui   # or pyfmi.common.plotting import plot_gui
##


model_name = 'Buildings.Fluid.Boilers.Examples.BoilerPolynomial'
mo_file = 'C:\Users\James\Desktop\Buildings 4.0.0'

fmu = compile_fmu(model_name,mo_file)
model = load_fmu(fmu)
res = model.simulate(final_time = 10.)

t = res['time']
T = res['boi1.temSen.T']

plt.figure(1)
plt.plot(t,T)
plt.grid(True)
plt.legend(['T'])
plt.xlabel('time [s]')
plt.ylabel('T')
plt.show()

plot_gui.startGUI()