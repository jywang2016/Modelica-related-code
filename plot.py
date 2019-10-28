## General imports
import numpy as np
import pandas as pd
import os,inspect

# Get this current script file's directory:
loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Set working directory
os.chdir(loc)
# from myFunctions import gen_FTN_data
# from meSAX import *

# from dtw_featurespace import *
# from dtw import dtw
# from fastdtw import fastdtw

# to avoid tk crash
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


## Load data
# Selected EVs
EVs = ['WeatherData.y',
       'RoomLoadData.y']


# Selected MVs
# MVs = ['controlUnit.yHeating',
#        'controlUnit.yCooling']
MVs = ['controlUnit.EOF',
       'controlUnit.yOAD',
       'controlUnit.ySAD',
       'controlUnit.yRAD',
       'controlUnit.yEAD',
       'controlUnit.yHeating',
       'controlUnit.yCooling']

# Load data files
import os
dataset_name = '102_HVACv4a_Weather+HeatLoadDataTest_Boston+SmallOffice'
filePath = 'N:\\HVAC_ModelicaModel_Data\\' + dataset_name
os.chdir(filePath)
fileNames = os.listdir(filePath)

# EV_FTN = gen_FTN_data(EVs,range(360),filePath,fileNames)
# MV_FTN = gen_FTN_data(MVs,range(360),filePath,fileNames)

FTNpath = r'C:\Users\James\OneDrive\PythonFiles\scripts\DBSCAN+LOF'

# Save in FTN format
# pd.to_pickle(EV_FTN, FTNpath+'\\EVs_FTN_' + dataset_name + '.pickle')
# pd.to_pickle(MV_FTN, FTNpath+'\\MVs_FTN_' + dataset_name + '.pickle')

# Load in FTN format
EV_FTN = pd.read_pickle(FTNpath+'\\EVs_FTN_' + dataset_name + '.pickle')
MV_FTN = pd.read_pickle(FTNpath+'\\MVs_FTN_' + dataset_name + '.pickle')


# data summary
weather_df = EV_FTN['WeatherData.y']
weather_avg = weather_df.quantile(0.5,axis = 1)
weather_Q1 = weather_df.quantile(0.25,axis = 1)
weather_Q3 = weather_df.quantile(0.75,axis = 1)
weather_std = weather_df.std(axis = 1)

heatload_df = EV_FTN['RoomLoadData.y']
heatload_avg = heatload_df.quantile(0.5,axis = 1)
heatload_Q1 = heatload_df.quantile(0.25,axis = 1)
heatload_Q3 = heatload_df.quantile(0.75,axis = 1)
heatload_std = heatload_df.std(axis = 1)



start_step = 2*360

weather_df = weather_df.iloc[start_step:]
weather_avg = weather_df.quantile(0.5,axis = 1)
weather_Q1 = weather_df.quantile(0.25,axis = 1)
weather_Q3 = weather_df.quantile(0.75,axis = 1)
weather_std = weather_df.std(axis = 1)

heatload_df = heatload_df.iloc[start_step:]
heatload_avg = heatload_df.quantile(0.5,axis = 1)
heatload_Q1 = heatload_df.quantile(0.25,axis = 1)
heatload_Q3 = heatload_df.quantile(0.75,axis = 1)
heatload_std = heatload_df.std(axis = 1)




n = len(weather_df.columns)

# To find color: matplotlib.colors.to_rgba('coral')
color1 = np.array([1.0, 0.4980392156862745, 0.3137254901960784, 1]) # RGBA
color2 = np.array([0.0, 0.75, 0.75,0.1])

colors = np.empty((n,4),dtype = float)
colors = (np.arange(n)/n).reshape(n,1) * (color2-color1).reshape(1,4) + color1
plt.figure()
for i,col in enumerate(heatload_df.columns):
    plt.plot(heatload_df.index,heatload_df[col],color = colors[i])
plt.show()


##
# np.array([1.0, 0.4980392156862745, 0.3137254901960784, 1]) # RGBA
color1 = np.array([1.0, 0.8431372549019608, 0.0,0.2])
color2 = np.array([0.2549019607843137, 0.4117647058823529, 0.8823529411764706,0.2])
color_new = np.array([1.0, 0.8431372549019608, 0.0, 1.0])

n_plot = 30

for i in range(n):
    ii = i+1
    colors = np.empty((n_plot,4),dtype = float)
    colors = (np.arange(n_plot)/n_plot).reshape(n_plot,1) * (color2-color1).reshape(1,4) + color1
    
    
    start_plot = (i-n_plot+1)
    plot_days = np.arange(start_plot,ii)
    
    plt.figure()
    for j,day in enumerate(plot_days):
        plt.plot(weather_df.index,weather_df[weather_df.columns[day]],color = colors[j])
    

    # highlight new heatload profile
    plt.plot(weather_df.index,weather_df[weather_df.columns[i]],color = color_new)
    
    plt.ylim((weather_df.min().min(),weather_df.max().max()))
    plt.title('Day {}'.format(ii))
    
    plt.savefig(r'C:\Users\James\Desktop\python_figs\weather\{}.png'.format(i))
    plt.close()
    print('{}/{}'.format(ii,n))

























