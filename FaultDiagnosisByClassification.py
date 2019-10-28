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

## my colors

color_list = ['gold', 'darkcyan','slateblue', 'hotpink', 'indigo', 'firebrick', 'skyblue', 'coral', 'sandybrown', 'mediumpurple',  'forestgreen', 'magenta', 'seagreen', 'greenyellow', 'roaylblue', 'gray', 'lightseagreen']

# Matplotlib default color cycler
# matplotlib.rcParams['axes.prop_cycle']
default_color_list = []
for obj in matplotlib.rcParams['axes.prop_cycle']:
    default_color_list.append(obj['color'])
# combine the two color lists
my_colors =  default_color_list
[my_colors.append(c) for c in color_list]

# my_colors = np.array(['#1f77b4','#2ca02c','#ff7f0e'])
my_colors = np.array(my_colors)



## generate data

# set random seed
np.random.seed(0)

# random data
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


y1 = np.ones((N1,))
y2 = np.ones((N2,)) * 2
y3 = np.ones((N3,)) * 3
yo = np.ones((2,)) * 4
ys = np.hstack((y1,y2,y3,yo))
ys = np.array(ys,dtype=np.int)

# test data
noise = np.random.randn(coords.shape[0],coords.shape[1])
coords_test = coords + noise 



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
from sklearn.svm import SVC

svm = SVC(kernel='rbf', degree=3,decision_function_shape='ovr')

svm.fit(coords,ys)

pred = np.array(svm.predict(coords_test),dtype=np.int)

# plot training data
plt.figure()
for i,p in enumerate(coords):
    plt.scatter(p[0],p[1],color = my_colors[ys[i]])
    # plt.scatter(coords_test[i][0],coords_test[i][1],color = my_colors[pred[i]],marker='x')
    

for i in range(ys.min(),ys.max()+1):
    plt.scatter([],[],color = my_colors[i],label = 'class: {}'.format(i))
plt.legend()
plt.show()


# plot test data, error prediction marked as 'x', correct preditction marked as 'o'
plt.figure()
for i,p in enumerate(coords_test):
    mk = 'o' if pred[i]==ys[i] else 'x'
    plt.scatter(p[0],p[1],color = my_colors[pred[i]],marker=mk)
    

for i in range(pred.min(),pred.max()+1):
    plt.scatter([],[],color = my_colors[i],label = 'class: {}'.format(i))
plt.legend()
plt.show()


# plot training and test data
plt.figure()
for i,p in enumerate(coords):
    plt.scatter(p[0],p[1],color = my_colors[ys[i]])
    plt.scatter(coords_test[i][0],coords_test[i][1],color = my_colors[pred[i]],marker='x')
    

for i in range(pred.min(),pred.max()+1):
    plt.scatter([],[],color = my_colors[i],label = 'class: {}'.format(i))
plt.legend()
plt.show()


## time-series data paths, parameters, and settings set up

# paths:
root_folder = 'L:\\HVAC_ModelicaModel_Data\\'
new_fault_dataset = '148_HVACv4a_SF+SmallOffice_Workday_Fault3_orifice'

fault_list = ['Fault 1',
              'Fault 2',
              'Fault 3',
              'Fault 4',
              'Fault 5',
              'Fault 6',
              ]

fault_root_loc = r'L:\HVAC_ModelicaModel_Data' + '\\'
training_data_list = ['140_HVACv4a_SF+SmallOffice_Workday',
                      '143_HVACv4a_SF+SmallOffice_Workday_Fault2',
                      '144_HVACv4a_SF+SmallOffice_Workday_Fault3',
                      '145_HVACv4a_SF+SmallOffice_Workday_Fault5',
                      '146_HVACv4a_SF+SmallOffice_Workday_Fault6',
                      '148_HVACv4a_SF+SmallOffice_Workday_Fault3_orifice',
                      '149_HVACv4a_SF+SmallOffice_Workday_Fault6_2'
                      ]
testdata_name = new_fault_dataset

# global parameters:

# Selected EVs
EVs = ['WeatherData.y']

# Selected MVs
MVs = ['controlUnit.EOF',
       'controlUnit.yOAD',
       'controlUnit.ySAD',
       'controlUnit.yRAD',
       'controlUnit.yEAD',
       'controlUnit.yHeating',
       'controlUnit.yCooling']
# time-series slicing
n_seg = 22
isOnOff = {'controlUnit.EOF' : True,
           'controlUnit.yOAD' : True,
           'controlUnit.ySAD' : True,
           'controlUnit.yRAD' : True,
           'controlUnit.yEAD' : True,
           'controlUnit.yHeating' : False,
           'controlUnit.yCooling' : False,
           'vavbox.PID_H.y' : False,
           'vavbox.PID_C.y' : False,
           'vavbox2.PID_H.y' : False,
           'vavbox2.PID_C.y' : False,
           'vavbox3.PID_H.y' : False,
           'vavbox3.PID_C.y' : False,
           'vavbox.swVal.u' : False,
           'vavbox.vavDamper.y' : False,
           'vavbox2.swVal.u' : False,
           'vavbox2.vavDamper.y' : False,
           'vavbox3.swVal.u' : False,
           'vavbox3.vavDamper.y' : False}
       
# 3room model has less ncp from simulation, 8640 > 4320
ncp = 8640 # number of communication points for JModelica
hr_pts = int(ncp/24 )# 360 # datapoints in an hour
n_sec = int(86400/ncp) # one sample per n_sec seconds
start_step = 2*hr_pts
# estimate the number of samples
T = hr_pts*22 # 22 hours
t = hr_pts*22 # 22 hours
i_step = hr_pts # 60 min/1hr
n_samples = math.floor((T-t)/i_step) + 1

# color list:
color_list = default_color_list


# # load training data: these become global data
rank_methods = [rank_euclidean]
rank_methods_names = ['Euclidean']

# contamination levels:
contam_values = np.array([0.01])

# save figure
savefig_ = False # True

# output paths:
fig_loc = root_folder + '\\Fault_diagnosis_{}'.format(new_fault_dataset)
result_loc = root_folder + '\\Fault_diagnosis_{}'.format(new_fault_dataset)

#

## load and stack data: example
# ------------------------------------------------------------------------------
# Load training datasets:
# ------------------------------------------------------------------------------
# stacked data with class labels
'''
stacked_MV_FTN is a dict() as FTN form, 'F'eatures as keys, and TN format DataFrames as values
compared to MV_FTN, stacked_MV_FTN has all training data stacked(axis=1, col direction) together
with class labels, class labels represent training datasets. Each training dataset has a class label

To access data: stacked_MV_FTN[key][class label(int)]['day'] # FDTN format [Feature,Dataset,Time,Day]
e.g.
stacked_MV_FTN['controlUnit.yHeating'][3]['day88']
'''
# intiailze
stacked_MV_FTN = dict()
stacked_class_labels = dict()
# stack data
for index,dataset_name in enumerate(training_data_list):
    filePath = root_folder + dataset_name
    os.chdir(filePath)
    fileNames = os.listdir(filePath)
    fileNames = [fname for fname in fileNames if fname[-4:]=='.csv'] # check if it's a csv file
    
    # Check if FTN files exist, if not, generate one:
    if not os.path.exists(filePath + '\\EV_FTN.pickle'):
        print('No FTN files found, generating one...')
        # Generate FTN files
        EV_FTN = gen_FTN_data(EVs,range(len(fileNames)),filePath,fileNames,n_sec=10)
        MV_FTN = gen_FTN_data(MVs,range(len(fileNames)),filePath,fileNames,n_sec=10)
        
        print('Saving FTN files...')
        # Save FTN files
        import pickle
        with open(filePath + '\\EV_FTN.pickle','wb') as f:
            pickle.dump(EV_FTN,f)
        with open(filePath + '\\MV_FTN.pickle','wb') as f:
            pickle.dump(MV_FTN,f)
    else:
        print('FTN files found, loading FTN files')
        # Load FTN files -----------------------------------------------------
        import pickle
        with open(filePath + '\\EV_FTN.pickle','rb') as f:
            EV_FTN = pickle.load(f)
        with open(filePath + '\\MV_FTN.pickle','rb') as f:
            MV_FTN = pickle.load(f)

    print('{} FTN files loaded'.format(dataset_name))
    
    
    
    # MVs    
    for key in MV_FTN.keys():
        class_labels = np.ones((MV_FTN[key].shape[1],),dtype=np.int)*(index)
        if not key in stacked_MV_FTN.keys(): # initialize
            stacked_MV_FTN[key] = MV_FTN[key]
            stacked_class_labels[key] = class_labels
        else: # stack for each training dataset
            stacked_MV_FTN[key] = pd.concat((stacked_MV_FTN[key],MV_FTN[key]),axis = 1)
            stacked_class_labels[key] = np.hstack((stacked_class_labels[key],class_labels))

# add labels(class: training dataset) as hierarchical multi-index columns
for key in  MV_FTN.keys():   
    arr = [stacked_class_labels[key],list(stacked_MV_FTN[key].columns)]
    micol = pd.MultiIndex.from_arrays(arr,names=['class','days']) # multi index column pd.DataFrame
    df = stacked_MV_FTN[key]
    df.columns = micol # change to hierarchical multi-index columns

print('Training dataset loaded')
# ------------------------------------------------------------------------------

##
# def load_training_datasets(root_folder,training_data_list):
#     '''
#     global parameters:
#         EVs: list of HVAC external variable names
#         MVs: list of HVAC manipulated variable names
#         i_step: increment step size for TS window t
#         T: Overall TS length
#         t: TS window size
#         start_step: data cleaning start step, crop out data before this time step
#         n_samples = number of samples for TS matrix
#         n_seg: number of segments for PAA conversion
#         n_sec: one sample per n_sec seconds
#     global parameters should be set before using this function
#     -------------------------------------------------------------------------------    
#     inputs:
#         root_folder: root folder path of all datasets
#         training_data_list: list of folder names of training datasets
#     outputs:
#         stacked_weather: Stacked divided TS weather data, numpy array in NT format
#         stacked_MV_FNT: Stacked MV_FNT data, a dictionary with
#                         keys = MV name, value = NT format data of MV
#         stacked_class_labels: a np.array of class labels(dataset index)
#     -------------------------------------------------------------------------------
#     Loads FTN data(pickel file) from "root_folder/dataset_name" path.
#     If no FTN data found, will generate one using function gen_FTN_data
#     Then use the FTN file to generate weather_ts and MVs_ts
#     '''
#     
#     import os
#     # intiailze
#     # stacked_EV_FTN = dict()
#     stacked_MV_FNT = dict()
#     stacked_class_labels = dict()
#     # stack data
#     for index,dataset_name in enumerate(training_data_list):
#         
#         # Load data files:
#         filePath = root_folder + dataset_name
#         os.chdir(filePath)
#         fileNames = os.listdir(filePath)
#         fileNames = [fname for fname in fileNames if fname[-4:]=='.csv'] # check if it's a csv file
#         
#         # Check if FTN files exist, if not, generate one:
#         if not os.path.exists(filePath + '\\EV_FTN.pickle'):
#             print('No FTN files found, generating one...')
#             # Generate FTN files
#             EV_FTN = gen_FTN_data(EVs,range(len(fileNames)),filePath,fileNames,n_sec=20)
#             MV_FTN = gen_FTN_data(MVs,range(len(fileNames)),filePath,fileNames,n_sec=20)
#             
#             print('Saving FTN files...')
#             # Save FTN files
#             import pickle
#             with open(filePath + '\\EV_FTN.pickle','wb') as f:
#                 pickle.dump(EV_FTN,f)
#             with open(filePath + '\\MV_FTN.pickle','wb') as f:
#                 pickle.dump(MV_FTN,f)
#         else:
#             print('FTN files found, loading FTN files')
#             # Load FTN files -----------------------------------------------------
#             import pickle
#             with open(filePath + '\\EV_FTN.pickle','rb') as f:
#                 EV_FTN = pickle.load(f)
#             with open(filePath + '\\MV_FTN.pickle','rb') as f:
#                 MV_FTN = pickle.load(f)
#         
#         
#         # EVs:
#         
#         weather_df = EV_FTN['WeatherData.y']
#         
#         # Data Cleaning
#         weather_df = weather_df.iloc[start_step:]
#         # weather_avg = weather_df.quantile(0.5,axis = 1)
#         # weather_Q1 = weather_df.quantile(0.25,axis = 1)
#         # weather_Q3 = weather_df.quantile(0.75,axis = 1)
#         # weather_std = weather_df.std(axis = 1)
#         # Divide TS data
#         # #######
#         # Weather
#         # #######
#         # # estimate the number of samples
#         # T = 360*22 # 20 hours
#         # t = 360*22 # 6 hours
#         # i_step = 6*60 # 60 min
#         import math
#         n_samples = math.floor((T-t)/i_step) + 1 # 
#         
#         
#         weather_ts = np.empty((n_samples*weather_df.shape[1],t)) # NT format
#         days = weather_df.columns
#         for day_count,day in enumerate(days):
#             for count,i in enumerate(range(0,T-t+1,i_step)):
#                 ts = weather_df[day].loc[start_step+i:start_step+i+t-1]
#                 ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
#                 row = day_count * n_samples + count
#                 weather_ts[row,:] = ts
#         
#         # weather_df = pd.DataFrame(weather_ts) # NT DataFrame
#         
#         
#         # corresponding MV data
#         
#         # convert on/off switch controlled MV to PAA
#         # n_seg is global parameter
#         for key in MVs:
#             if isOnOff[key]:
#                 MV = np.array(MV_FTN[key].T) # TN to NT format
#                 N = MV.shape[0]
#                 for i in range(N): # update MV values with PAA result
#                     # MV[i] = PAA(MV[i],n_seg,original_length=True)
#                     MV_FTN[key][MV_FTN[key].columns[i]] = PAA(MV[i],n_seg,original_length=True,print_=False)
#                 
#         
#         
#         MVs_ts = np.empty((len(MV_FTN),n_samples*MV_FTN[list(MV_FTN.keys())[0]].shape[1],t)) # FNT format
#         
#         for MV_index,key in enumerate(MV_FTN):
#             MV_df = MV_FTN[key] # set MV
#             MV_df = MV_df.iloc[start_step:] # truncate data
#             # Divide ts
#             MV_ts = np.empty((n_samples*MV_df.shape[1],t)) # NT format
#             days = MV_df.columns
#             for day_count,day in enumerate(days):
#                 for count,i in enumerate(range(0,T-t+1,i_step)):
#                     ts = MV_df[day].loc[start_step+i:start_step+i+t-1]
#                     ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
#                     row = day_count * n_samples + count
#                     MV_ts[row,:] = ts
#             print('{} finished {}/{}'.format(key,MV_index+1,len(MV_FTN)))
#             MVs_ts[MV_index] = MV_ts # NT format
#             # MVs_ts[MV_index] = MV_ts.T # NT to TN format => MVs_ts becomes FTN format
#     
#     
#     # ----------------------------------------------------
#         # Generate stacked_MVs    
#         for i,key in enumerate(MV_FTN.keys()):
#             class_labels = np.ones((MVs_ts.shape[1],),dtype=np.int)*(index)
#             if not key in stacked_MV_FNT.keys(): # initialize
#                 stacked_MV_FNT[key] = MVs_ts[i] # NT format #MV_FTN[key]
#                 stacked_class_labels[key] = class_labels
#                 
#                 stacked_weather = weather_ts # NT format
#             else: # stack for each training dataset
#                 stacked_MV_FNT[key] = np.concatenate((stacked_MV_FNT[key],MVs_ts[i]),axis = 0)
#                 stacked_class_labels[key] = np.hstack((stacked_class_labels[key],class_labels))
#                 stacked_weather = np.concatenate((stacked_weather,weather_ts),axis = 0) # NT format
#          
#          
#     
#         # for key in MV_FTN.keys():
#         #     class_labels = np.ones((MV_FTN[key].shape[1],),dtype=np.int)*(index)
#         #     if not key in stacked_MV_FTN.keys(): # initialize
#         #         stacked_MV_FTN[key] = MV_FTN[key]
#         #         stacked_class_labels[key] = class_labels
#         #     else: # stack for each training dataset
#         #         stacked_MV_FTN[key] = pd.concat((stacked_MV_FTN[key],MV_FTN[key]),axis = 1)
#         #         stacked_class_labels[key] = np.hstack((stacked_class_labels[key],class_labels))
#     
#     # # add labels(class: training dataset) as hierarchical multi-index columns
#     # for key in  MV_FTN.keys():   
#     #     arr = [stacked_class_labels[key],list(stacked_MV_FTN[key].columns)]
#     #     micol = pd.MultiIndex.from_arrays(arr,names=['class','days']) # multi index column pd.DataFrame
#     #     df = stacked_MV_FTN[key]
#     #     df.columns = micol # change to hierarchical multi-index columns
#         print('Dataset {} has been processed!'.format(dataset_name))
#     return(stacked_weather,stacked_MV_FNT,stacked_class_labels)

def load_training_data(root_folder,dataset_name):
    '''
    global parameters:
        EVs: list of HVAC external variable names
        MVs: list of HVAC manipulated variable names
        i_step: increment step size for TS window t
        T: Overall TS length
        t: TS window size
        start_step: data cleaning start step, crop out data before this time step
        n_samples = number of samples for TS matrix
        n_seg: number of segments for PAA conversion
        n_sec: one sample per n_sec seconds
    global parameters should be set before using this function
    -------------------------------------------------------------------------------    
    inputs:
        root_folder: root folder path of all datasets
        dataset_name: folder name of dataset
    outputs:
        weather_ts: Divided TS weather data, numpy array in NT format
        MVs_ts: Corresponding divided TS MVs data, numpy array in NT format
    -------------------------------------------------------------------------------
    Loads FTN data(pickel file) from "root_folder/dataset_name" path.
    If no FTN data found, will generate one using function gen_FTN_data
    Then use the FTN file to generate weather_ts and MVs_ts
    '''
    
    # Load data files
    import os
    # dataset_name = '130_HVACv4a_Boston+SmallOffice_Workday'
    filePath = root_folder + dataset_name
    os.chdir(filePath)
    fileNames = os.listdir(filePath)
    fileNames = [fname for fname in fileNames if fname[-4:]=='.csv'] # check if it's a csv file
    
    # Check if FTN files exist, if not, generate one:
    if not os.path.exists(filePath + '\\EV_FTN.pickle'):
        print('No FTN files found, generating one...')
        # Generate FTN files
        EV_FTN = gen_FTN_data(EVs,range(len(fileNames)),filePath,fileNames,n_sec=20)
        MV_FTN = gen_FTN_data(MVs,range(len(fileNames)),filePath,fileNames,n_sec=20)
        
        print('Saving FTN files...')
        # Save FTN files
        import pickle
        with open(filePath + '\\EV_FTN.pickle','wb') as f:
            pickle.dump(EV_FTN,f)
        with open(filePath + '\\MV_FTN.pickle','wb') as f:
            pickle.dump(MV_FTN,f)
    else:
        print('FTN files found, loading FTN files')
        # Load FTN files -----------------------------------------------------
        import pickle
        with open(filePath + '\\EV_FTN.pickle','rb') as f:
            EV_FTN = pickle.load(f)
        with open(filePath + '\\MV_FTN.pickle','rb') as f:
            MV_FTN = pickle.load(f)
    
    
    
    weather_df = EV_FTN['WeatherData.y']
    
    # Data Cleaning
    weather_df = weather_df.iloc[start_step:]
    # weather_avg = weather_df.quantile(0.5,axis = 1)
    # weather_Q1 = weather_df.quantile(0.25,axis = 1)
    # weather_Q3 = weather_df.quantile(0.75,axis = 1)
    # weather_std = weather_df.std(axis = 1)
    # Divide TS data
    # #######
    # Weather
    # #######
    # # estimate the number of samples
    # T = 360*22 # 20 hours
    # t = 360*22 # 6 hours
    # i_step = 6*60 # 60 min
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
    
    
    # corresponding MV data
    
    # convert on/off switch controlled MV to PAA
    # n_seg is global parameter
    for key in MVs:
        if isOnOff[key]:
            MV = np.array(MV_FTN[key].T) # TN to NT format
            N = MV.shape[0]
            for i in range(N): # update MV values with PAA result
                # MV[i] = PAA(MV[i],n_seg,original_length=True)
                MV_FTN[key][MV_FTN[key].columns[i]] = PAA(MV[i],n_seg,original_length=True,print_=False)
            
    
    
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
    
    return(weather_ts,MVs_ts)


##
def load_test_data(root_folder,testdata_name):
    '''
    global parameters:
        EVs: list of HVAC external variable names
        MVs: list of HVAC manipulated variable names
        i_step: increment step size for TS window t
        T: Overall TS length
        t: TS window size
        start_step: data cleaning start step, crop out data before this time step
        n_samples = number of samples for TS matrix
        n_sec: one sample per n_sec seconds
    global parameters should be set before using this function
    -------------------------------------------------------------------------------    
    inputs:
        root_folder: root folder path of all datasets
        testdata_name: folder name of testing dataset
    outputs:
        test_EVs_ts: Divided TS EVs data, numpy array in NT format
        test_MVs_ts: Corresponding divided TS MVs data, numpy array in NT format
    -------------------------------------------------------------------------------
    Loads FTN data(pickel file) from "root_folder/testdata_name" path.
    If no FTN data found, will generate one using function gen_FTN_data
    Then use the FTN file to generate weather_ts and MVs_ts
    '''
    # ------------------------------------------------------------------------------
    # Load testing dataset:
    # ------------------------------------------------------------------------------
    filePath = root_folder + testdata_name
    os.chdir(filePath)
    fileNames = os.listdir(filePath)
    fileNames = [fname for fname in fileNames if fname[-4:]=='.csv'] # check if it's a csv file
    
    # Check if FTN files exist, if not, generate one:
    if not os.path.exists(filePath + '\\EV_FTN.pickle'):
        print('No FTN files found, generating one...')
        # Generate FTN files
        test_EV_FTN = gen_FTN_data(EVs,range(len(fileNames)),filePath,fileNames,n_sec=10)
        test_MV_FTN = gen_FTN_data(MVs,range(len(fileNames)),filePath,fileNames,n_sec=10)
        
        print('Saving FTN files...')
        # Save FTN files
        import pickle
        with open(filePath + '\\EV_FTN.pickle','wb') as f:
            pickle.dump(test_EV_FTN,f)
        with open(filePath + '\\MV_FTN.pickle','wb') as f:
            pickle.dump(test_MV_FTN,f)
    else:
        print('FTN files found, loading FTN files')
        # Load FTN files -----------------------------------------------------
        import pickle
        with open(filePath + '\\EV_FTN.pickle','rb') as f:
            test_EV_FTN = pickle.load(f)
        with open(filePath + '\\MV_FTN.pickle','rb') as f:
            test_MV_FTN = pickle.load(f)
    
    print('{} FTN files loaded'.format(new_fault_dataset))
    print('Testing dataset loaded')
    
    
    
    # Data cleaning ------------------------------------------------------
    # truncate data
    for FTN in [test_EV_FTN,test_MV_FTN]:
        for key in FTN:
            FTN[key] = FTN[key].iloc[start_step:] # start step given previously, same as training data
    
    # Divide TS to smaller intervals -------------------------------------
    '''
    # estimate the number of samples
    # T = 360*22 # 20 hours
    # t = 360*6 # 6 hours
    # i_step = 6*60 # 60 min
    # import math
    # n_samples = math.floor((T-t)/i_step) + 1 # 
    '''
    
    
    test_EVs_ts = np.empty((len(test_EV_FTN),n_samples*test_EV_FTN[list(test_EV_FTN.keys())[0]].shape[1],t))
    
    for test_EV_index,key in enumerate(test_EV_FTN):
        test_EV_df = test_EV_FTN[key] # set test_EV
        
        # already truncated, skip this
        # test_EV_df = test_EV_df.iloc[start_step:] # truncate data
        
        # Divide ts
        test_EV_ts = np.empty((n_samples*test_EV_df.shape[1],t)) # NT format
        days = test_EV_df.columns
        for day_count,day in enumerate(days):
            for count,i in enumerate(range(0,T-t+1,i_step)):
                ts = test_EV_df[day].loc[start_step+i:start_step+i+t-1]
                ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
                row = day_count * n_samples + count
                test_EV_ts[row,:] = ts
        print('{} finished {}/{}'.format(key,test_EV_index+1,len(test_EV_FTN)))
        test_EVs_ts[test_EV_index] = test_EV_ts
        
    
        
    # corresponding MV data
    
    # convert on/off switch controlled MV to PAA
    # n_seg is global parameter
    for key in MVs:
        if isOnOff[key]:
            MV = np.array(test_MV_FTN[key].T) # TN to NT format
            N = MV.shape[0]
            for i in range(N): # update MV values with PAA result
                # MV[i] = PAA(MV[i],n_seg,original_length=True)
                test_MV_FTN[key][test_MV_FTN[key].columns[i]] = PAA(MV[i],n_seg,original_length=True,print_=False)
                
    
    test_MVs_ts = np.empty((len(test_MV_FTN),n_samples*test_MV_FTN[list(test_MV_FTN.keys())[0]].shape[1],t))
    
    for test_MV_index,key in enumerate(test_MV_FTN):
        test_MV_df = test_MV_FTN[key] # set test_MV
        
        # already truncated, skip this
        # test_MV_df = test_MV_df.iloc[start_step:] # truncate data
        
        # Divide ts
        test_MV_ts = np.empty((n_samples*test_MV_df.shape[1],t)) # NT format
        days = test_MV_df.columns
        for day_count,day in enumerate(days):
            for count,i in enumerate(range(0,T-t+1,i_step)):
                ts = test_MV_df[day].loc[start_step+i:start_step+i+t-1]
                ts = ts.values.reshape(1,t) # col vector to row vector, shape(t,1) to (1,t)
                row = day_count * n_samples + count
                test_MV_ts[row,:] = ts
        print('{} finished {}/{}'.format(key,test_MV_index+1,len(test_MV_FTN)))
        test_MVs_ts[test_MV_index] = test_MV_ts
    
    
    return(test_EVs_ts,test_MVs_ts)





## Rank order weather data
'''
Instead of using pattern matching methods, e.g. SAX, we use similarity rank-ordered
time-series data. The first k closest time-series are considered as in the same
group(comparables).

This seems to be doable due to the fact that we are comparing weather profiles.
Weather profiles are generally slow-changing and have similar trends, which makes
rank ordering to be a candidate approach.
'''


# Rank order functions:
'''
Given a weather data frame and a specified day, rank order the similar days compared
to the specified day, comparing with high-low tempeature differences.

Inputs:
    - weather_ts: Weather data in DataFrame format (TN format)
    - test_day: the specified day, rank ordering other days wrt this day. A (N,) array
    - print_: If True, function will print out status update
Output:
    - ranked_arr: a rank-ordered numpy array of the days

'''
def rank_high_low(weather_ts,test_day,print_=False):
    high_temps = weather_ts.max(axis = 1)
    low_temps = weather_ts.min(axis = 1)
    
    # test_temp = (high_temps[test_day],low_temps[test_day]) # high-low temp pair
    test_temp = (test_day.max(),test_day.min())
    
    dtype = [('Day',int),('distance',float)] # numpy.void data type
    ranked_arr = np.empty((weather_ts.shape[0],),dtype=dtype)
    
    # compare with days in data base
    for day in range(weather_ts.shape[0]):
        d_high = np.abs(high_temps[day] - test_temp[0])
        d_low = np.abs(low_temps[day] - test_temp[1])
        d = d_high + d_low
       
        ranked_arr[day] = (day,d)
        if print_: print('Finished {}/{}'.format(day+1,weather_ts.shape[0]))
    
    ranked_arr.sort(order = 'distance')
    
    return(ranked_arr)


'''
Given a weather data frame and a specified day, rank order the similar days compared
to the specified day, comparing with DTW differences.

Requires scipy and fastdtw packages

Inputs:
    - weather_ts: Weather data in DataFrame format (TN format)
    - test_day: the specified day, rank ordering other days wrt this day. A (N,) array
    - print_: If True, function will print out status update
    - mode:
        'save': compute and save the output result. DTW computation is time consuming!
        'compute': compute without saving.
        'load': load pre-computed output result
    - loc: A pickle file location. Used for loading pre-computed result or saving result.
    - fileName: File name used for save or load.
Output:
    - ranked_arr_dtw: a rank-ordered numpy array of the days

'''
def rank_dtw(weather_ts,test_day,print_ = True,mode = 'compute',loc = None,fileName= None):
    
    if mode == 'compute' or mode == 'save':
        from scipy.spatial.distance import euclidean
        from fastdtw import fastdtw
        
        dtype = [('Day',int),('distance',float)]
        ranked_arr_dtw = np.empty((weather_ts.shape[0],),dtype=dtype)
        
        # compute DTW distances
        # dtw_test = weather_df[weather_df.columns[test_day]]
        dtw_test = test_day
        for day in range(weather_ts.shape[0]):
            # seq = weather_df[weather_df.columns[day]]
            seq = weather_ts[day]
            # Use my own dtw
            # p,C,D = dtw(dtw_test,seq)
            # d = D[-1]
            
            # Use fastdtw
            d,p = fastdtw(dtw_test,seq,dist=euclidean)
        
            ranked_arr_dtw[day] = (day,d)
            if print_: print('Finished {}/{}'.format(day+1,weather_ts.shape[0]))
        
        ranked_arr_dtw.sort(order = 'distance')
        
        # Save
        if mode == 'save':
            import pickle
            with open(loc + '\\' + fileName,'wb') as f:
                pickle.dump(ranked_arr_dtw,f)
        
    elif mode == 'load':
        # load
        import pickle
        with open(loc + '\\' + fileName,'rb') as f:
            ranked_arr_dtw = pickle.load(f)
    
    
    return(ranked_arr_dtw)


# # load example:
# rank_dtw(weather_ts,test_day,mode='load',loc = loc, fileName = 'ranked_arr_dtw.pickle')
# # save example:
# rank_dtw(weather_ts,123,mode='save',loc = loc, fileName = 'ranked_arr_dtw.pickle')



'''
Given a weather data frame and a specified day, rank order the similar days compared
to the specified day, comparing with Euclidean distance of tempeature profiles.

Inputs:
    - weather_ts: Weather data in DataFrame format (TN format)
    - test_day: the specified day, rank ordering other days wrt this day. A (N,) array
    - print_: If True, function will print out status update
Output:
    - ranked_arr_euclidean: a rank-ordered numpy array of the days
'''
def rank_euclidean(weather_ts,test_day,print_ = False):
    from scipy.spatial.distance import euclidean
    
    dtype = [('Day',int),('distance',float)]
    ranked_arr_euclidean = np.empty((weather_ts.shape[0],),dtype=dtype)
    
    # compute Euclidean distances
    # euclidean_test = weather_df[weather_df.columns[test_day]]
    euclidean_test = test_day
    for day in range(weather_ts.shape[0]):
        # seq = weather_df[weather_df.columns[day]]
        seq = weather_ts[day]
    
        d = euclidean(euclidean_test,seq)
    
        ranked_arr_euclidean[day] = (day,d)
        if print_: print('Finished {}/{}'.format(day+1,weather_ts.shape[0]))
    
    ranked_arr_euclidean.sort(order = 'distance')
    return(ranked_arr_euclidean)

'''
Given a weather data frame and a specified day, rank order the similar days compared
to the specified day, comparing with absolute distance of tempeature profiles.

Inputs:
    - weather_ts: Weather data in DataFrame format (TN format)
    - test_day: the specified day, rank ordering other days wrt this day. A (N,) array
    - print_: If True, function will print out status update
Output:
    - ranked_arr_abs: a rank-ordered numpy array of the days
'''
def rank_abs(weather_ts,test_day,print_ = False):
    dtype = [('Day',int),('distance',float)]
    ranked_arr_abs = np.empty((weather_ts.shape[0],),dtype=dtype)
    
    # compute absolute distances
    # abs_test = weather_df[weather_df.columns[test_day]]
    abs_test = test_day
    for day in range(weather_ts.shape[0]):
        # seq = weather_df[weather_df.columns[day]]
        seq = weather_ts[day]
    
        d = np.sum(np.absolute(abs_test - seq))
    
        ranked_arr_abs[day] = (day,d)
        if print_: print('Finished {}/{}'.format(day+1,weather_ts.shape[0]))
    
    ranked_arr_abs.sort(order = 'distance')
    return(ranked_arr_abs)


'''
Given a weather data frame and a specified day, rank order the similar days compared
to the specified day, comparing with SAX approximated tempeature differences.

Inputs:
    - weather_ts: Weather data in DataFrame format (TN format)
    - test_day: the specified day, rank ordering other days wrt this day. A (N,) array
    - print_: If True, function will print out status update
Output:
    - ranked_arr_sax: a rank-ordered numpy array of the days
'''
def rank_SAX(weather_ts,test_day,print_ = False):
    from meSAX import SAX as SAX
    
    dtype = [('Day',int),('distance',float)]
    ranked_arr_sax = np.empty((weather_ts.shape[0],),dtype=dtype)
    
    seg = 24
    cardinality = 30
    r_min = 273.15 - 20
    r_max = 273.15 + 40
    
    # compute distances based on SAX
    # ts =weather_df[weather_df.columns[test_day]]
    ts = test_day
    sax = SAX(ts,seg,cardinality,r_min,r_max,False)
    for day in range(weather_ts.shape[0]):
        # seq = weather_df[weather_df.columns[day]]
        seq = weather_ts[day]
        seq_sax = SAX(seq,seg,cardinality,r_min,r_max,False)
        d = np.sum(np.abs(sax - seq_sax))
    
        ranked_arr_sax[day] = (day,d)
        # print('Finished {}/{}'.format(day+1,weather_ts.shape[0]))
    
    ranked_arr_sax.sort(order = 'distance')
    return(ranked_arr_sax)


## classify and stack time-series

# Rank grouping:

rank_method = rank_methods[0]
rank_method_name = rank_methods_names[0]

# load datasets
# stacked_weather,stacked_MV_FNT,stacked_class_labels = load_training_datasets(root_folder,training_data_list)

'''
Each MV needs a SVM classifier. Stack MV's [NT] and [label] data over all datasets vertically.
stacked_MV_NT: a dictionary with keys = MVs, values = vstacked MV data in NT format
stacked_class_labels: a dictionary with keys = MVs, values = stacked class/dataset labels
'''
# initialize stacked data
stacked_MV_NT = dict()
stacked_class_labels = dict()

# load test data, only needs to load once
test_EVs_ts,test_MVs_ts = load_test_data(root_folder,testdata_name)
test_weather_ts = test_EVs_ts[0] # test weather data

for c_label,training_dataset in enumerate(training_data_list):
    # load training data
    weather_ts,MVs_ts = load_training_data(root_folder,training_dataset)
    
    for n in range(test_weather_ts.shape[0]):
        # find nearest weather data from training dataset for each testing data sample:
        group_size = 5
        weather_group = rank_method(weather_ts,test_weather_ts[n])['Day'][:group_size] # day indices
        
        
        # corresponding MVs of nearest weather data
        for MV_index,key in enumerate(MVs):
            # class labels
            class_labels = np.ones((MVs_ts[MV_index,weather_group].shape[0],),dtype=np.int)*(c_label) 
            
            if not key in stacked_MV_NT.keys(): # initialize
                stacked_MV_NT[key] = MVs_ts[MV_index,weather_group]
                stacked_class_labels[key] = class_labels
            else:
                stacked_MV_NT[key] = np.vstack((stacked_MV_NT[key],MVs_ts[MV_index,weather_group]))
                stacked_class_labels[key] = np.hstack((stacked_class_labels[key],class_labels))
        
        print('test day: {}/{}'.format(n+1,test_weather_ts.shape[0]))
    print('Stacked {}/{}'.format(c_label+1,len(training_data_list)))

# # save data
# import pickle
# with open(r'L:\HVAC_ModelicaModel_Data\stacked_data.pickle','wb') as f:
#     data = [stacked_MV_NT,stacked_class_labels]
#     pickle.dump(data,f)

# load data
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\stacked_data.pickle','rb') as f:
    [stacked_MV_NT,stacked_class_labels] = pickle.load(f)
    
    

## SVM
# initialize SVM classifiers:
from sklearn.svm import SVC
SVMs = []
for i in range(len(MVs)): # each MV requires a SVM classifier
    SVMs.append(SVC(kernel='rbf', degree=3,decision_function_shape='ovr'))
# Train SVMs
# predictions = []
for MV_index,key in enumerate(MVs):
    svm = SVMs[MV_index]
    svm.fit(stacked_MV_NT[key],stacked_class_labels[key])
    print('{}/{} trained'.format(MV_index+1,len(MVs)))
    # pred = np.array(svm.predict(test_MVs_ts[MV_index]),dtype=np.int)
    # predictions.append(pred)

# # Save SVM classifiers
# import pickle
# with open(r'L:\HVAC_ModelicaModel_Data\SVMs.pickle','wb') as f:
#     pickle.dump(SVMs,f)

# Load SVM classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\SVMs.pickle','rb') as f:
    SVMs = pickle.load(f)

# Classify each MV with SVM
predictions = []
for MV_index,key in enumerate(MVs):
    svm = SVMs[MV_index]
    pred = np.array(svm.predict(test_MVs_ts[MV_index]),dtype=np.int)
    predictions.append(pred)

# print results
for pred in predictions:
    print(pred)

## GPC
# initialize GPC classifiers:
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
GPCs = []
for i in range(len(MVs)): # each MV requires a GPC classifier
    GPCs.append(GaussianProcessClassifier(kernel=RBF(1.0),multi_class='one_vs_rest',warm_start=True))
    
# Train GPCs
for MV_index,key in enumerate(MVs):
    gpc = GPCs[MV_index]
    gpc.fit(stacked_MV_NT[key],stacked_class_labels[key])
    print('{}/{} trained'.format(MV_index+1,len(MVs)))


# Save GPC classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\GPCs.pickle','wb') as f:
    pickle.dump(GPCs,f)

# Load GPC classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\GPCs.pickle','rb') as f:
    GPCs = pickle.load(f)

# Classify each MV with GPC
predictions = []
for MV_index,key in enumerate(MVs):
    gpc = GPCs[MV_index]
    pred = np.array(gpc.predict(test_MVs_ts[MV_index]),dtype=np.int)
    predictions.append(pred)

# print results
for pred in predictions:
    print(pred)


## K-nearest neighbors
from sklearn.neighbors import KNeighborsClassifier

KNCs = []
for i in range(len(MVs)): # each MV requires a KNC classifier
    KNCs.append(KNeighborsClassifier(n_neighbors=5))
    
# Train KNCs
for MV_index,key in enumerate(MVs):
    knn = KNCs[MV_index]
    knn.fit(stacked_MV_NT[key],stacked_class_labels[key])
    print('{}/{} trained'.format(MV_index+1,len(MVs)))


# # Save KNC classifiers
# import pickle
# with open(r'L:\HVAC_ModelicaModel_Data\KNCs.pickle','wb') as f:
#     pickle.dump(KNCs,f)

# Load KNC classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\KNCs.pickle','rb') as f:
    KNCs = pickle.load(f)

# Classify each MV with KNC
predictions = []
for MV_index,key in enumerate(MVs):
    knn = KNCs[MV_index]
    pred = np.array(knn.predict(test_MVs_ts[MV_index]),dtype=np.int)
    predictions.append(pred)

# print results
for pred in predictions:
    print(pred)



## Stochastic Gradient Descent Classifier
from sklearn.linear_model import SGDClassifier

SGDCs = []
for i in range(len(MVs)): # each MV requires a SGDC classifier
    SGDCs.append(SGDClassifier(loss='log',verbose=0,max_iter=1000,tol=1e-3))
    
# Train SGDs
for MV_index,key in enumerate(MVs):
    sgd = SGDCs[MV_index]
    sgd.fit(stacked_MV_NT[key],stacked_class_labels[key])
    print('{}/{} trained'.format(MV_index+1,len(MVs)))


# # Save SGDC classifiers
# import pickle
# with open(r'L:\HVAC_ModelicaModel_Data\SGDCs.pickle','wb') as f:
#     pickle.dump(SGDCs,f)

# Load SGDC classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\SGDCs.pickle','rb') as f:
    SGDCs = pickle.load(f)

# Classify each MV with SGDC
predictions = []
for MV_index,key in enumerate(MVs):
    sgd = SGDCs[MV_index]
    pred = np.array(sgd.predict(test_MVs_ts[MV_index]),dtype=np.int)
    predictions.append(pred)

# print results
for pred in predictions:
    print(pred)



## Boosting
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier

# Aboost_SVM = AdaBoostClassifier(SVC(kernel='rbf', degree=3,decision_function_shape='ovr'),n_estimators=200)


# initialize boostCLFs classifiers:
boostCLFs = []
for i in range(len(MVs)): # each MV requires a classifier
    '''
    AdaBoostClassifier: algorithm = 'SAMME.R' requires that the weak learner supports
    the calculation of class probabilities => use probability.
    Or use  algorithm = 'SAMME'
    '''
    # boost_svm = AdaBoostClassifier(SVC(kernel='rbf', degree=3,decision_function_shape='ovr'),
    #                                n_estimators=200, algorithm = 'SAMME')
    # boost_svm = AdaBoostClassifier(SVC(kernel='rbf',probability = True,
    #                                    degree=3,decision_function_shape='ovr'),n_estimators=200)
    # boost_clf = SGDClassifier(loss='log',verbose=1)
    # boost_clf = AdaBoostClassifier(SGDClassifier(loss='log',verbose=1),n_estimators=200,algorithm = 'SAMME')
    boost_clf = AdaBoostClassifier(n_estimators=200) # default uses DecisionTreeClassifier
    boostCLFs.append(boost_clf)
    
# Train boostCLFs
for MV_index,key in enumerate(MVs):
    boost_clf = boostCLFs[MV_index]
    boost_clf.fit(stacked_MV_NT[key],stacked_class_labels[key])
    print('{}/{} trained'.format(MV_index+1,len(MVs)))

# Save boostCLFs classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\boostCLFs.pickle','wb') as f:
    pickle.dump(boostCLFs,f)


# Load boostCLFs classifiers
import pickle
with open(r'L:\HVAC_ModelicaModel_Data\boostCLFs.pickle','rb') as f:
    boostCLFs = pickle.load(f)


# Classify each MV with boostCLFs
predictions = []
for MV_index,key in enumerate(MVs):
    boost_clf = boostCLFs[MV_index]
    pred = np.array(boost_clf.predict(test_MVs_ts[MV_index]),dtype=np.int)
    predictions.append(pred)

# print results
for pred in predictions:
    print(pred)


## Show stats

for i,MV in enumerate(MVs):
    pred = predictions[i]
    print('{}:'.format(MV))
    for j,dataset in enumerate(training_data_list):
        n = len(pred[pred==j])
        print('{}:\t{}%\n{}/{}'.format(dataset,n/len(pred)*100,n,len(pred)))
    print('\n\n')























