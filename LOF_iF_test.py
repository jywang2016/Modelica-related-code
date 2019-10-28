## General imports
import numpy as np
import pandas as pd
import os,inspect
import math

# Get this current script file's directory:
loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Set working directory
os.chdir(loc)
os.chdir('..') # parent directory
from myFunctions import gen_FTN_data
from meSAX import *
os.chdir(loc) # change back to loc


# from dtw_featurespace import *
# from dtw import dtw
# from fastdtw import fastdtw

# to avoid tk crash
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## generate data

# set random seed
np.random.seed(0)

# my sample data
x_mean1 = 0
y_mean1 = 0

x_mean2 = 45
y_mean2 = 13

x_mean3 = 7
y_mean3 = 40

N1 = 100
N2 = 100
N3 = 100

# coords1 = np.random.uniform(0,12,(N1,2))
# coords2 = np.random.uniform(0,5,(N2,2))
coords1 = np.random.randn(N1,2) * 16
coords2 = np.random.randn(N2,2) * 4
coords3 = np.random.randn(N3,2) * 1
outliers = np.array([15,15,23,12]).reshape(2,2)
coords = np.empty((N1+N2+N3+outliers.shape[0],2))


coords[:N1] =  coords1 + (x_mean1,y_mean1)
coords[N1:(N1+N2)] =  coords2 + (x_mean2,y_mean2)
coords[(N1+N2):-2] =  coords3 + (x_mean3,y_mean3)
coords[-2:] = outliers

# # sklearn example data
# n_points_per_cluster = 250
# 
# C1 = [-5, -2] + .8 * np.random.randn(n_points_per_cluster, 2)
# C2 = [4, -1] + .1 * np.random.randn(n_points_per_cluster, 2)
# C3 = [1, -2] + .2 * np.random.randn(n_points_per_cluster, 2)
# C4 = [-2, 3] + .3 * np.random.randn(n_points_per_cluster, 2)
# C5 = [3, -2] + 1.6 * np.random.randn(n_points_per_cluster, 2)
# C6 = [5, 6] + 2 * np.random.randn(n_points_per_cluster, 2)
# coords = np.vstack((C1, C2, C3, C4, C5, C6))



## 
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest

LOF = LocalOutlierFactor(n_neighbors=20)
iForest = IsolationForest()


LOF.fit(coords)
lof_labels = LOF.fit_predict(coords)
iForest.fit(coords)
iforest_labels = iForest.predict(coords)

lof_scores = LOF.negative_outlier_factor_
LOF.threshold_
if_scores = iForest.decision_function(coords)
iForest.threshold_


# plot normalized scores
plt.figure()
plt.plot((lof_scores - np.mean(lof_scores))/np.std(lof_scores))
plt.plot((if_scores - np.mean(if_scores))/np.std(if_scores))

plt.hlines((LOF.threshold_ - np.mean(lof_scores))/np.std(lof_scores),xmin=0,xmax=coords.shape[0],color='steelblue')
plt.hlines((iForest.threshold_ - np.mean(if_scores))/np.std(if_scores),xmin=0,xmax=coords.shape[0],color='coral')

plt.show()







