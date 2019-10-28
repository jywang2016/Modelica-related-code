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
# # Selected EVs
# EVs = ['WeatherData.y',
#        'RoomLoadData.y']
# 
# 
# # Selected MVs
# # MVs = ['controlUnit.yHeating',
# #        'controlUnit.yCooling']
# MVs = ['controlUnit.EOF',
#        'controlUnit.yOAD',
#        'controlUnit.ySAD',
#        'controlUnit.yRAD',
#        'controlUnit.yEAD',
#        'controlUnit.yHeating',
#        'controlUnit.yCooling']

# Load data files
import os
dataset_name = 'SF_SmallOfficeNew2004.csv'#'SF_LargeOfficeNew2004.csv' # 'SF_PrimarySchoolNew2004.csv'
filePath = r'N:\HVAC_ModelicaModel_Data\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States'
os.chdir(filePath)
fileName = filePath + '\\' + dataset_name
# fileNames = os.listdir(filePath)

heatload_df = pd.read_csv(fileName)#np.loadtxt(fileName,delimiter = ',')
heatload_df = heatload_df[heatload_df.columns[1:-1]]

# EV_FTN = gen_FTN_data(EVs,range(360),filePath,fileNames)
# MV_FTN = gen_FTN_data(MVs,range(360),filePath,fileNames)

# FTNpath = r'C:\Users\James\OneDrive\PythonFiles\scripts\DBSCAN+LOF'

# # Save in FTN format
# pd.to_pickle(EV_FTN, FTNpath+'\\EVs_FTN_' + dataset_name + '.pickle')
# pd.to_pickle(MV_FTN, FTNpath+'\\MVs_FTN_' + dataset_name + '.pickle')

# # Load in FTN format
# EV_FTN = pd.read_pickle(FTNpath+'\\EVs_FTN_' + dataset_name + '.pickle')
# MV_FTN = pd.read_pickle(FTNpath+'\\MVs_FTN_' + dataset_name + '.pickle')


# data summary
# weather_df = EV_FTN['WeatherData.y']
# weather_avg = weather_df.quantile(0.5,axis = 1)
# weather_Q1 = weather_df.quantile(0.25,axis = 1)
# weather_Q3 = weather_df.quantile(0.75,axis = 1)
# weather_std = weather_df.std(axis = 1)

# heatload_df = EV_FTN['RoomLoadData.y']
# heatload_avg = heatload_df.quantile(0.5,axis = 1)
# heatload_Q1 = heatload_df.quantile(0.25,axis = 1)
# heatload_Q3 = heatload_df.quantile(0.75,axis = 1)
# heatload_std = heatload_df.std(axis = 1)



start_step = 2 # 2*360

# weather_df = weather_df.iloc[start_step:]
# weather_avg = weather_df.quantile(0.5,axis = 1)
# weather_Q1 = weather_df.quantile(0.25,axis = 1)
# weather_Q3 = weather_df.quantile(0.75,axis = 1)
# weather_std = weather_df.std(axis = 1)

heatload_df = heatload_df.iloc[start_step:]
heatload_avg = heatload_df.quantile(0.5,axis = 1)
heatload_Q1 = heatload_df.quantile(0.25,axis = 1)
heatload_Q3 = heatload_df.quantile(0.75,axis = 1)
heatload_std = heatload_df.std(axis = 1)


heatload = np.array(heatload_df.T)

## k-means

from sklearn.cluster import KMeans
N = 5 # number of clusters

kmeans = KMeans(n_clusters = N)
kmeans.fit(heatload)


color_list = ['gold', 'darkcyan','slateblue', 'hotpink', 'indigo', 'firebrick', 'skyblue', 'coral', 'sandybrown', 'mediumpurple',  'forestgreen', 'magenta', 'seagreen', 'greenyellow', 'roaylblue', 'gray', 'lightseagreen']

# Matplotlib default color cycler
# matplotlib.rcParams['axes.prop_cycle']
default_color_list = []
for obj in matplotlib.rcParams['axes.prop_cycle']:
    default_color_list.append(obj['color'])
# combine the two color lists
my_colors =  default_color_list
[my_colors.append(c) for c in color_list]
my_colors = np.array(my_colors)


plt.figure()
for i in range(heatload.shape[0]):
    plt.plot(heatload[i], color = my_colors[kmeans.labels_[i]], alpha = 0.3)

for i in range(N):
    plt.plot([],color = my_colors[i],label = 'cluster{}'.format(i))

plt.xlabel('Time[hour]')
plt.ylabel('Heat load[W]')
plt.legend()
plt.show()

# weekends+holidays when N = 2
np.arange(kmeans.labels_ .shape[0])[kmeans.labels_ == 1]


## Compare with DBSCAN
# Get this current script file's directory:
loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Set working directory
os.chdir(loc)
from myFunctions import gen_dist_mat, k_dist
from scipy.spatial import distance
dist = distance.minkowski
D = gen_dist_mat(heatload,dist)

# '''
# inputs:
#     D: distance matrix(N by N)
#     k: k-th neighbor distance
# '''
# def k_dist(D,k = 4):
#     import numpy as np
#     D = np.array(D)
#     N = D.shape[0]
#     # initialize k_dist vector
#     k_dist = np.zeros((N,1))
#     for i in range(N):
#         row = list(D[i,:])
#         for j in range(k): # remove min(row) k times, not k-1 times, because closest is always itself!
#             row.remove(min(row))
#         k_dist[i] = min(row)
#     return(k_dist)

k_distances = k_dist(D,k=4)
k_distances = np.sort(k_distances,axis = 0)

plt.figure()
plt.plot(k_distances)
plt.show()

eps = 1643.21#381.1 #30281
from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=eps, min_samples=4).fit(heatload)
dbscan.labels_
clusters = list(set(dbscan.labels_))
print(clusters)
for cluster in clusters:
    cluster_size = len(dbscan.labels_[dbscan.labels_== cluster])
    print('cluster{} \t has a size of {}'.format(cluster,cluster_size))

plt.figure()
plt.hist(dbscan.labels_)
plt.show()


plt.figure()
for i in range(heatload.shape[0]):
    plt.plot(heatload[i], color = my_colors[dbscan.labels_[i]], alpha = 0.3)

for i in range(-1,len(set(dbscan.labels_))-1):
    plt.plot([],color = my_colors[i],label = 'cluster{}'.format(i))

plt.xlabel('Time[hour]')
plt.ylabel('Heat load[W]')
plt.legend()
plt.show()

## using mean shift to determine k /model selection: k

from sklearn.cluster import MeanShift

ms = MeanShift().fit(heatload)
N = max(ms.labels_) + 1


plt.figure()
for i in range(heatload.shape[0]):
    plt.plot(heatload[i], color = my_colors[ms.labels_[i]], alpha = 0.3)

for i in range(N):
    plt.plot([],color = my_colors[i],label = 'cluster{}'.format(i))

plt.legend()
plt.show()



## MDS

from sklearn.manifold import MDS

# mds = MDS(n_components=2, max_iter=3000, eps=1e-9, dissimilarity="precomputed")
# mds.fit(D)
mds = MDS(n_components=2, max_iter=3000, eps=1e-9, dissimilarity='euclidean')
mds.fit(heatload)

# embedding_ : array-like, shape (n_components, n_samples)
# Stores the position of the dataset in the embedding space.
# stress_ : float
# The final value of the stress (sum of squared distance of the disparities and the distances for all constrained points).

plt.scatter(mds.embedding_[:,0],mds.embedding_[:,1],alpha = 0.3, marker = 'x')
plt.title('Multidimensional Scaling')
plt.show()


c_algorithm = dbscan#kmeans # clustering algorithm
color_list = my_colors
# # colored with clustering labels
# import matplotlib.colors as colors
# color_list = list(colors.cnames.keys())
# color_shift = 0
# color_list = ['gray','firebrick','coral','sandybrown','gold','greenyellow','forestgreen',
#               'lightseagreen','seagreen','darkcyan','skyblue','roaylblue','slateblue',
#               'mediumpurple','indigo','magenta','hotpink']
# import random
# color_list = random.sample(color_list,len(color_list))

plt.figure()
for i,pos in enumerate(mds.embedding_):
    plt.scatter(pos[0],pos[1],color = color_list[c_algorithm.labels_[i]+color_shift],alpha = 0.8,
                marker = 'o')
# empty plot to set up legends
for i in list(set(c_algorithm.labels_)):
    plt.scatter([],[],color = color_list[i+color_shift],alpha = 0.8,
                marker = 'o',label = 'Cluster: ' + str(i))
    
plt.legend()

plt.title('Multidimensional Scaling')
plt.show()


# # 3D
# # mds3d = MDS(n_components=3, max_iter=3000, eps=1e-9, dissimilarity="precomputed")
# # mds3d.fit(D)
# mds = MDS(n_components=2, max_iter=3000, eps=1e-9, dissimilarity='euclidean')
# mds.fit(heatload)
# 
# 
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# for i,pos in enumerate(mds.embedding_):
#     ax.scatter(pos[0],pos[1],color = color_list[c_algorithm.labels_[i]+color_shift],alpha = 0.8,
#                 marker = 'o')
# plt.title('Multidimensional Scaling')
# plt.show()



## OPTICS
# Get this current script file's directory:
loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Set working directory
os.chdir(loc)

from meOPTICS import *
from meOPTICS import DataPoint
from meOPTICS import meOPTICS
from meOPTICS import gen_dist_mat
from scipy.spatial import distance
dist = distance.minkowski

# parameters
D = gen_dist_mat(heatload,dist)
eps = 21096
eps2 = 10000
MinPts = 15
xi = 0.01

# Run OPTICS
optics = meOPTICS(heatload,eps,eps2,MinPts,D = None,xi = xi)
order_list = optics.get_order()
cluster_list = optics.auto_cluster(order_list)


clusters = []
for i,cluster in enumerate(cluster_list):
    clusters.append(range(cluster[0],cluster[1]))


# reachability-distance plot
plt.figure()
# reachability-distances
cluster_r_dists = np.array([o.r_dist for o in order_list])

# cluster labels
cluster_labels = np.ones((D.shape[0],),dtype=int) * -1 # if unset, default is -1(noise)
for i,o in enumerate(order_list):
    for j,cluster in enumerate(clusters):
        if i in cluster: cluster_labels[i] = j
# legend labels
for i,cluster in enumerate(cluster_list):
    plt.scatter([],[],color = my_colors[i],alpha = 0.5,label = 'cluster{}:{}'.format(i,clusters[i]))
plt.scatter([],[],color = my_colors[-1],alpha = 0.5,marker='x',label = 'noise')
# plot

# plt.scatter(range(cluster_r_dists.shape[0]),cluster_r_dists,color = my_colors[cluster_labels],alpha = 0.4)
# plt.legend(bbox_to_anchor=(1.01, 1))

cluster_markers = np.array(['o' if o != -1 else 'x' for o in cluster_labels])
for i,r_dist in enumerate(cluster_r_dists):
    plt.scatter(i,r_dist,color = my_colors[cluster_labels[i]],alpha = 0.5,marker=cluster_markers[i])
    

plt.legend()
plt.title('reachability-distance plot\nauto extract')
plt.show()



# plot heatload
plt.figure()
for i,o in enumerate(order_list):
    plt.plot(heatload[o.index], color = my_colors[cluster_labels[i]], alpha = 0.3,
    linestyle= '--' if cluster_labels[i]==-1 else '-')

for i in range(-1,len(set(cluster_labels))-1):
    plt.plot([],color = my_colors[i],label = 'noise' if i==-1 else 'cluster{}'.format(i),
    linestyle= '--' if i == -1 else '-')

plt.xlabel('Time[hour]')
plt.ylabel('Heat load[W]')
plt.legend()
plt.show()




## max clusters in OPTICS
import copy
max_clusters = copy.deepcopy(cluster_list)

i = 0
while i < len(max_clusters):
    flag = False
    ci = max_clusters[i]
    for j,cj in enumerate(max_clusters):
        if ((cj[0] < ci[0] and cj[1] >= ci[1]) or (cj[0] <= ci[0] and cj[1] > ci[1])):
            max_clusters.pop(i)
            flag = True
            break
    if not flag: i += 1

# generate clusters and legend labels
m_clusters = []
for i,cluster in enumerate(max_clusters):
    m_clusters.append(range(cluster[0],cluster[1]))


# reachability-distance plot
plt.figure()
# reachability-distances
cluster_r_dists = np.array([o.r_dist for o in order_list])

# cluster labels
max_cluster_labels = np.ones((D.shape[0],),dtype=int) * -1 # if unset, default is -1(noise)
for i,o in enumerate(order_list):
    for j,cluster in enumerate(m_clusters):
        if i in cluster: max_cluster_labels[i] = j
# legend labels
for i,cluster in enumerate(max_clusters):
    plt.scatter([],[],color = my_colors[i],alpha = 0.5,label = 'cluster{}:{}'.format(i,m_clusters[i]))
plt.scatter([],[],color = my_colors[-1],alpha = 0.5,marker='x',label = 'noise')
# plot

# plt.scatter(range(cluster_r_dists.shape[0]),cluster_r_dists,color = my_colors[max_cluster_labels],alpha = 0.4)

max_cluster_markers = np.array(['o' if o != -1 else 'x' for o in max_cluster_labels])
for i,r_dist in enumerate(cluster_r_dists):
    plt.scatter(i,r_dist,color = my_colors[max_cluster_labels[i]],alpha = 0.5,marker=max_cluster_markers[i])
    
plt.legend()
plt.xlabel('Data sample index')
plt.ylabel('Distance')
# plt.title('reachability-distance plot\nauto extract(max clusters)')
plt.show()





# plot heatload
plt.figure()
for i,o in enumerate(order_list):
    plt.plot(heatload[o.index], color = my_colors[max_cluster_labels[i]], alpha = 0.3,
    linestyle= '--' if max_cluster_labels[i]==-1 else '-')

for i in range(-1,len(set(max_cluster_labels))-1):
    plt.plot([],color = my_colors[i],label = 'noise' if i==-1 else 'cluster{}'.format(i),
    linestyle= '--' if i == -1 else '-')

plt.xlabel('Time[hour]')
plt.ylabel('Heat load[W]')
plt.legend()
plt.show()








