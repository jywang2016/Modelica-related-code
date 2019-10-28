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

## Classify heatload by days in a week

# 7 days a week

heatload_weekly = []
for i in range(7): # NT format np.array(easier to work with compared to dataframes)
    arr = np.array(heatload_df[heatload_df.columns[i::7]]).T
    heatload_weekly.append(arr)



color_list = ['gold', 'darkcyan','slateblue', 'hotpink', 'indigo', 'firebrick', 'skyblue', 'coral', 'sandybrown', 'mediumpurple',  'forestgreen', 'magenta', 'seagreen', 'greenyellow', 'roaylblue', 'gray', 'lightseagreen']

# Matplotlib default color cycler
# matplotlib.rcParams['axes.prop_cycle']
default_color_list = []
for obj in matplotlib.rcParams['axes.prop_cycle']:
    default_color_list.append(obj['color'])
# combine the two color lists
my_colors =  default_color_list
[my_colors.append(c) for c in color_list]   
    

plt.figure()
for i in range(7):
    index = 420 + i + 1
    ax = plt.subplot(index)
    
    avg = heatload_weekly[i].mean(axis = 0)
    sd = heatload_weekly[i].std(axis = 0)
    # q1 = np.percentile(heatload_weekly[i],0.25,axis = 0)
    # q3 = np.percentile(heatload_weekly[i],0.75,axis = 0)
    
    
    plt.plot(avg,color = default_color_list[i])
    plt.plot(avg+sd,linestyle = 'dotted',color = default_color_list[i])
    plt.plot(avg-sd,linestyle = 'dotted',color = default_color_list[i])
    plt.fill_between(range(len(avg)),avg-sd,avg+sd,color = default_color_list[i],alpha = 0.2)
    # plt.fill_between(range(len(avg)),q1,q3,color = default_color_list[i],alpha = 0.3)
plt.show()


plt.figure()
for i in range(7):
    index = 420 + i + 1
    ax = plt.subplot(index)
    for row in range(heatload_weekly[i].shape[0]):
        plt.plot(heatload_weekly[i][row],color = default_color_list[i],alpha = 0.3)
plt.show()


plt.figure()
for i in range(7):
    for row in range(heatload_weekly[i].shape[0]):
        label_txt = str(i) if row==1 else '_no_legend_'
        plt.plot(heatload_weekly[i][row],color = default_color_list[i],alpha = 0.3,label=label_txt)
plt.legend()
plt.show()


## Classify heatload by months

heatload_month = []
for i in range(12): # NT format np.array(easier to work with compared to dataframes)
    s = i*30
    e = (i+1)*30
    arr = np.array(heatload_df[heatload_df.columns[s:e]]).T
    # print(heatload_df.columns[s:e])
    heatload_month.append(arr)


color1 = np.array(matplotlib.colors.to_rgba('steelblue'))
color2 = np.array(matplotlib.colors.to_rgba('coral'))
delta_color = (color2-color1)/5
colors12 = np.empty((12,4))
for i in range(6):
    colors12[i] = color1 + i*delta_color
    colors12[-1-i] = color1 + i*delta_color

plt.figure()
for i,mon in enumerate(heatload_month):
    # plt.plot(mon.mean(axis=0), color = my_colors[i],label = str(i))
    plt.plot(mon.mean(axis=0), color = colors12[i],label = str(i))
plt.legend()
plt.show()



##

# Days without Sundays and Saturdays
weekdays = [x for x in [x for x in range(360) if (x%7!=0)] if (x%7!=6)]


















