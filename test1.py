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
# MVs = ['controlUnit.EOF',
#        'controlUnit.yOAD',
#        'controlUnit.ySAD',
#        'controlUnit.yRAD',
#        'controlUnit.yEAD',
#        'controlUnit.yHeating',
#        'controlUnit.yCooling']

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
# MV_FTN = pd.read_pickle(FTNpath+'\\MVs_FTN_' + dataset_name + '.pickle')


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


test_day = 123

## Find high and low temperature of each day

high_temps = weather_df.max(axis = 0)
low_temps = weather_df.min(axis = 0)

plt.plot(range(360),high_temps)
plt.plot(range(360),low_temps)
plt.show()


## Rank order comparable days

test_temp = (high_temps[test_day],low_temps[test_day]) # high-low temp pair

# dtype = [('Day','U10'),('distance',float)]
dtype = [('Day',int),('distance',float)]
ranked_arr = np.empty((weather_df.shape[1],),dtype=dtype)

# compare with days in data base
for day in range(weather_df.shape[1]):
    d_high = np.abs(high_temps[day] - test_temp[0])
    d_low = np.abs(low_temps[day] - test_temp[1])
    d = d_high + d_low
    
    # ranked_arr[day] = ('Day'+str(day),d)
    ranked_arr[day] = (day,d)

ranked_arr.sort(order = 'distance')



## DTW of raw temperature data
# from dtw import dtw
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

dtype = [('Day',int),('distance',float)]
ranked_arr_dtw = np.empty((weather_df.shape[1],),dtype=dtype)

# compute DTW distances
dtw_test = weather_df[weather_df.columns[test_day]]
for day in range(weather_df.shape[1]):
    seq = weather_df[weather_df.columns[day]]
    # p,C,D = dtw(dtw_test,seq)
    # d = D[-1]
    d,p = fastdtw(dtw_test,seq,dist=euclidean)

    ranked_arr_dtw[day] = (day,d)
    print('Finished {}/{}'.format(day+1,weather_df.shape[1]))

ranked_arr_dtw.sort(order = 'distance')

import pickle
# with open(loc + '\\ranked_arr_dtw.pickle','wb') as f:
#     pickle.dump(ranked_arr_dtw,f)

with open(loc + '\\ranked_arr_dtw.pickle','rb') as f:
    ranked_arr_dtw = pickle.load(f)



## Euclidean distance of raw temperature data

dtype = [('Day',int),('distance',float)]
ranked_arr_euclidean = np.empty((weather_df.shape[1],),dtype=dtype)

# compute Euclidean distances
euclidean_test = weather_df[weather_df.columns[test_day]]
for day in range(weather_df.shape[1]):
    seq = weather_df[weather_df.columns[day]]

    d = euclidean(euclidean_test,seq)

    ranked_arr_euclidean[day] = (day,d)
    print('Finished {}/{}'.format(day+1,weather_df.shape[1]))

ranked_arr_euclidean.sort(order = 'distance')

## absolute distance of raw temperature data

dtype = [('Day',int),('distance',float)]
ranked_arr_abs = np.empty((weather_df.shape[1],),dtype=dtype)

# compute absolute distances
abs_test = weather_df[weather_df.columns[test_day]]
for day in range(weather_df.shape[1]):
    seq = weather_df[weather_df.columns[day]]

    d = np.sum(np.absolute(abs_test - seq))

    ranked_arr_abs[day] = (day,d)
    print('Finished {}/{}'.format(day+1,weather_df.shape[1]))

ranked_arr_abs.sort(order = 'distance')



## SAX
from meSAX import *

dtype = [('Day',int),('distance',float)]
ranked_arr_sax = np.empty((weather_df.shape[1],),dtype=dtype)

seg = 24
cardinality = 30
r_min = 273.15 - 20
r_max = 273.15 + 40

# compute distances based on SAX
ts =weather_df[weather_df.columns[test_day]]
sax = SAX(ts,seg,cardinality,r_min,r_max,False)
for day in range(weather_df.shape[1]):
    seq = weather_df[weather_df.columns[day]]
    seq_sax = SAX(seq,seg,cardinality,r_min,r_max,False)
    d = np.sum(np.abs(sax - seq_sax))

    ranked_arr_sax[day] = (day,d)
    print('Finished {}/{}'.format(day+1,weather_df.shape[1]))

ranked_arr_sax.sort(order = 'distance')



# sax_splits = SAX_split_intervals(ts,seg,cardinality,r_min,r_max,True)
# sax_splits_minmax = SAX_split_intervals(ts,seg,cardinality,r_min,r_max,True,True)
# sax_scale = (r_max-r_min)/(2**cardinality-1)
# paa = PAA(ts,seg,True)
# sax_bounds = SAX_bounds(ts,seg,cardinality,r_min,r_max,True)


## Compare the differences of the measures

# Ranked order of days:
# ranked_arr['Day']
# ranked_arr_dtw['Day']
# ranked_arr_euclidean['Day']
# ranked_arr_sax['Day']

rank_df = pd.DataFrame({'HighLow':ranked_arr['Day'],
                        'DTW':ranked_arr_dtw['Day'],
                        'Euclidean':ranked_arr_euclidean['Day'],
                        'SAX':ranked_arr_sax['Day'],
                        'Absolute':ranked_arr_abs['Day']
                        })
                        

# Compare similarity ratio:
def similar_ratio(seq1,seq2):
    N1 = len(seq1)
    N2 = len(seq2)
    if N1 != N2:
        print('Two input sequence differ in length!')
        return(None)
    
    N = np.max([N1,N2])
    
    match = 0 # number of matches
    for i in range(N):
        if seq1[i] == seq2[i]: match += 1
    
    return(match/N)



    
def distance_rating(seq1,seq2):
    N1 = len(seq1)
    N2 = len(seq2)
    if N1 != N2:
        print('Two input sequence differ in length!')
        return(None)
    
    N = np.max([N1,N2])
    
    distance = 0
    for i in range(N):
        if seq1[i] != seq2[i]:
            # find corresponding value in seq2
            for j,day in enumerate(seq2):
                if seq1[i] == day: break
            distance += np.abs(i-j)
    return(distance)
    
    

    
    
# similar ratio matrix
sim_ratio_mat = np.empty((rank_df.shape[1],rank_df.shape[1]),dtype=float)
for i,seq1 in enumerate(rank_df.columns):
    for j,seq2 in enumerate(rank_df.columns):
        sim_ratio_mat[i,j] = similar_ratio(rank_df[seq1],rank_df[seq2])

sim_ratio_mat = pd.DataFrame(sim_ratio_mat,columns = rank_df.columns,index = rank_df.columns)
print(sim_ratio_mat)


# distance rating matrix
dist_rating_mat = np.empty((rank_df.shape[1],rank_df.shape[1]),dtype=float)
for i,seq1 in enumerate(rank_df.columns):
    for j,seq2 in enumerate(rank_df.columns):
        dist_rating_mat[i,j] = distance_rating(rank_df[seq1],rank_df[seq2])

dist_rating_mat = pd.DataFrame(dist_rating_mat,columns = rank_df.columns,index = rank_df.columns)
print(dist_rating_mat)




## Visualize

import matplotlib.pyplot as plt

data = rank_df

# fig,ax = plt.subplots()
# cax = ax.contourf(data,cmap = plt.cm.Blues)
# fig.colorbar(cax)
# plt.xticks(range(4))
# 
# plt.figure()
# im = plt.matshow(data,cmap = plt.cm.Blues)
# # im = plt.imshow(data,cmap = plt.cm.Blues)
# plt.colorbar(im)
# plt.xticks(range(4))
# 
# plt.show()

# 
plt.figure()
color_w = (0,1,0)
color_r = (1,0,0)


colors = np.empty((data.shape[0],4))
colors[:,0] = np.arange(data.shape[0])/data.shape[0] * (np.array(color_w)-np.array(color_r))[0] + np.array(color_r)[0]
colors[:,1] = np.arange(data.shape[0])/data.shape[0] * (np.array(color_w)-np.array(color_r))[1] + np.array(color_r)[1]
colors[:,2] = np.arange(data.shape[0])/data.shape[0] * (np.array(color_w)-np.array(color_r))[2] + np.array(color_r)[2]

alphas = np.linspace(0.3,0,data.shape[0])
colors[:,3] = alphas = 0.3

scatter_size = [625 for i in range(data.shape[0])]

for x in range(len(data.columns)):
    plt.scatter([x for i in range(data.shape[0])],data[data.columns[x]],
                color = colors, s = scatter_size, marker='_',label='_no_legends_')

# plt.scatter([0 for i in range(data.shape[0])],data[data.columns[0]],
#             color = colors, s = scatter_size, marker='_')
# plt.scatter([1 for i in range(data.shape[0])],data[data.columns[1]],
#             color = colors, s = scatter_size, marker='_')
# plt.scatter([2 for i in range(data.shape[0])],data[data.columns[2]],
#             color = colors, s = scatter_size, marker='_')
# plt.scatter([3 for i in range(data.shape[0])],data[data.columns[3]],
#             color = colors, s = scatter_size, marker='_')

plt.xticks(range(len(data.columns)),data.columns) #(locations, labels)

plt.scatter([],[],color = color_w,alpha=0.3,label='dissimilar')
plt.scatter([],[],color = color_r,alpha=0.3,label='similar')
plt.legend()
plt.title('Rank ordering with respect to day:{}'.format(test_day))
plt.show()



# GIF

for step in range(rank_df.shape[0]):
    data = rank_df[:step]
    
    plt.figure()
    color_w = (0,1,0)
    color_r = (1,0,0)
    
    
    colors = np.empty((data.shape[0],4))
    colors[:,0] = np.arange(data.shape[0])/data.shape[0] * (np.array(color_w)-np.array(color_r))[0] + np.array(color_r)[0]
    colors[:,1] = np.arange(data.shape[0])/data.shape[0] * (np.array(color_w)-np.array(color_r))[1] + np.array(color_r)[1]
    colors[:,2] = np.arange(data.shape[0])/data.shape[0] * (np.array(color_w)-np.array(color_r))[2] + np.array(color_r)[2]
    
    alphas = np.linspace(0.3,0,data.shape[0])
    colors[:,3] = alphas = 0.3
    
    scatter_size = [625 for i in range(data.shape[0])]
    
    for x in range(len(data.columns)):
        plt.scatter([x for i in range(data.shape[0])],data[data.columns[x]],
                    color = colors, s = scatter_size, marker='_')
    # plt.scatter([0 for i in range(data.shape[0])],data[data.columns[0]],
    #             color = colors, s = scatter_size, marker='_')
    # plt.scatter([1 for i in range(data.shape[0])],data[data.columns[1]],
    #             color = colors, s = scatter_size, marker='_')
    # plt.scatter([2 for i in range(data.shape[0])],data[data.columns[2]],
    #             color = colors, s = scatter_size, marker='_')
    # plt.scatter([3 for i in range(data.shape[0])],data[data.columns[3]],
    #             color = colors, s = scatter_size, marker='_')
    
    plt.xticks(range(len(data.columns)),data.columns)
    
    plt.ylim((-10,370))
    # plt.show()
    
    plt.savefig(r'C:\Users\James\Desktop\python_figs\rank_compare' + '\\Step{}'.format(step))
    plt.close()
    print('Step{}'.format(step+1))




# from matplotlib.animation import FuncAnimation



























