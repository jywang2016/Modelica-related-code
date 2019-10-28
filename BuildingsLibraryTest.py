from pymodelica import compile_fmu
from pyfmi import load_fmu
import matplotlib.pyplot as plt
from pyjmi.common.plotting import plot_gui   # or pyfmi.common.plotting import plot_gui
##


# C:/OpenModelica1.11.0-64bit/lib/omlibrary/Buildings latest/Fluid/Movers/Validation/FlowControlled_dp.mo
model_name = 'Buildings.Fluid.Movers.Validation.FlowControlled_dp'
mo_file = 'C:\Users\James\Desktop\Buildings 4.0.0'

fmu = compile_fmu(model_name,mo_file)
model = load_fmu(fmu)
res = model.simulate(final_time = 1.)

t = res['time']
dp = res['dpDyn.dp']

plt.figure(1)
plt.plot(t,dp)
plt.grid(True)
plt.legend(['dp'])
plt.xlabel('time [s]')
plt.ylabel('dp')
plt.show()

plot_gui.startGUI()