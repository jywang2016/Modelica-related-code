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
# import os
dataset_name = '102_HVACv4a_Weather+HeatLoadDataTest_Boston+SmallOffice'
# filePath = 'N:\\HVAC_ModelicaModel_Data\\' + dataset_name
# os.chdir(filePath)
# fileNames = os.listdir(filePath)

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

# heatload_df = EV_FTN['RoomLoadData.y']
# heatload_avg = heatload_df.quantile(0.5,axis = 1)
# heatload_Q1 = heatload_df.quantile(0.25,axis = 1)
# heatload_Q3 = heatload_df.quantile(0.75,axis = 1)
# heatload_std = heatload_df.std(axis = 1)



## Data Cleaning

# Remove the first few hours of data, for they are not meaningful since the system
# is initializing.
# Take out 0-4AM

start_step = 0 # 2*360
# 
# weather_df = weather_df.iloc[start_step:]
# weather_avg = weather_df.quantile(0.5,axis = 1)
# weather_Q1 = weather_df.quantile(0.25,axis = 1)
# weather_Q3 = weather_df.quantile(0.75,axis = 1)
# weather_std = weather_df.std(axis = 1)

# plt.figure()
# plt.plot(weather_avg,'b')
# plt.plot(weather_avg + weather_std,'b--')
# plt.plot(weather_avg - weather_std,'b--')
# plt.fill_between(weather_df.index,weather_Q1,weather_Q3,color = 'blue', alpha = 0.2)
# plt.xlabel('Time[hours]')
# plt.ylabel('Temperature[K]')
# plt.title('Day Temperature')
# plt.show()

## Divide TS data into smaller intervals(subsequences)
'''
T: Total number of time steps(dimension of orginal time series)
t: Number of time steps in the smaller time intervals(dimension of smaller time series)
i_step: Interval step
    (start,end,step) >> (0,T-t,i_step)
Will have ( math.floor((T-t)/i_step) + 1 ) time series data samples of i_step time steps
'''
# #######
# Weather
# #######
# estimate the number of samples
T = 360*24 # 24 hours
t = 360*6 # 6 hours
i_step = 6*60 # 60 min
import math
n_samples = math.floor((T-t)/i_step) + 1 # 


weather_ts = np.empty((n_samples*weather_df.shape[1],t)) # NT format
days = weather_df.columns
for day_count,day in enumerate(days):
    for count,i in enumerate(range(0,T-t+1,i_step)):
        ts = weather_df[day].loc[start_step+i:start_step+i+t-1]
        ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
        row = day_count * n_samples + count
        weather_ts[row,:] = ts
        

# ########
# Heatload
# ########
# estimate the number of samples
# T = 360*22 # 20 hours
# t = 360*6 # 6 hours
# i_step = 6*60 # 60 min
# import math
# n_samples = math.floor((T-t)/i_step) + 1 # 


# heatload_ts = np.empty((n_samples*heatload_df.shape[1],t)) # NT format
# days = heatload_df.columns
# for day_count,day in enumerate(days):
#     for count,i in enumerate(range(0,T-t+1,i_step)):
#         ts = heatload_df[day].loc[start_step+i:start_step+i+t-1]
#         ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
#         row = day_count * n_samples + count
#         heatload_ts[row,:] = ts


## Find the corresponding MV data

# Divide ts into smaller intervals
# same as previous
# T = 360*22 # 20 hours
# t = 360*6 # 6 hours
# i_step = 6*60 # 60 min
# import math
# n_samples = math.floor((T-t)/i_step) + 1

# MVs_ts.shape (MV index, N, T)
MVs_ts = np.empty((len(MV_FTN),n_samples*MV_FTN[list(MV_FTN.keys())[0]].shape[1],t))

for MV_index,key in enumerate(MV_FTN):
    MV_df = MV_FTN[key] # set MV
    MV_df = MV_df.iloc[start_step:] # truncate data
    # Divide ts
    MV_ts = np.empty((n_samples*MV_df.shape[1],t)) # NT format
    days = MV_df.columns
    for day_count,day in enumerate(days):
        for count,i in enumerate(range(0,T-t+1,i_step)):
            ts = MV_df[day].loc[start_step+i:start_step+i+t-1]
            ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
            row = day_count * n_samples + count
            MV_ts[row,:] = ts
    print('{} finished {}/{}'.format(key,MV_index+1,len(MV_FTN)))
    MVs_ts[MV_index] = MV_ts
    




## Compare test data with training data



























