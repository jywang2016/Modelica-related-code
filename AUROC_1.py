'''
The starting half is a copy of FDD_rank_order.py

The latter half will run different comtamination parameters for fault detection,
in order to get TPF and FPF for AUROC
'''

'''
Need these two packages for pandas to work with excel files
pip install openpyxl
pip install xlrd
'''

## General imports
import numpy as np
import pandas as pd
import os,inspect
import math

# Get this current script file's directory:
loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Set working directory
os.chdir(loc)
from myFunctions import gen_FTN_data
from meSAX import *

# from dtw_featurespace import *
# from dtw import dtw
# from fastdtw import fastdtw

# to avoid tk crash
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


## Load data: Training data

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


## Compare test data with training data

# Load data


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
    # testdata_name = testdata_names[testdata_index]
    
    filePath = root_folder + testdata_name
    # filePath = 'N:\\HVAC_ModelicaModel_Data\\' + testdata_name
    os.chdir(filePath)
    fileNames = os.listdir(filePath)
    fileNames = [fname for fname in fileNames if fname[-4:]=='.csv'] # check if it's a csv file
    
    if not os.path.exists(filePath + '\\EV_FTN.pickle'):
        print('No FTN files found, generating one...')
        # Generate FTN files
        test_EV_FTN = gen_FTN_data(EVs,range(len(fileNames)),filePath,fileNames,n_sec=20)
        test_MV_FTN = gen_FTN_data(MVs,range(len(fileNames)),filePath,fileNames,n_sec=20)
        
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
    
    '''
    These steps are going over the same work flow as we did for training data
    '''
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
        

## Anomaly detection:

def anomaly_detection(testdata_name,rank_method_index,test_EVs_ts,test_MVs_ts,fig_loc,result_loc,contam,savefig_ = True):
    '''
    Runs LOF and Isolation Forest for fault detection.
    Starts with using given rank function to group test_EVs_ts data to 
    weather_ts data, then compare MVs data with test_MVs_ts data using LOF and Isolation Forest
    
    -----------------------------------------------------------------------------
    global inputs:
        weather_ts: Divided TS weather data, numpy array in NT format
        MVs_ts: Corresponding divided TS MVs data, numpy array in NT format
        n_seg: number of segments for PAA conversion
    -----------------------------------------------------------------------------
    inputs:
        testdata_name: folder name of testing dataset, used to print out progress
        rank_method_index: index to identify rank method used
        test_EVs_ts: Divided TS EVs data, numpy array in NT format
        test_MVs_ts: Corresponding divided TS MVs data, numpy array in NT format
        fig_loc: folder path for saved faulty figure plots
        result_loc: folder path for fault detection rate result text files
        contam: contamination parameter used for scikit-learn anomaly detection algorithms
        savefig_: save figure if set to True, default is True
    outputs:
        Faulty TS is saved as a plot
        The fault detection rate of a dataset is saved in a text file
    '''
    # Local Outlier Factor
    from sklearn.neighbors import LocalOutlierFactor
    from myFunctions import gen_dist_mat
    
    #
    experimentName = '{}_LOF'.format(testdata_name)
    # Choose ranking method
    # rank_group = rank_high_low
    rank_group = rank_methods[rank_method_index]
    rank_method_name = rank_methods_names[rank_method_index]
    
    test_weather_ts = test_EVs_ts[0] # test weather data
    
    # MV_index = 0 # MV we are examining
    MV_predictions = []
    for MV_index in range(len(MVs)):
        predictions = []
        for n in range(test_weather_ts.shape[0]):
            # The 20th closest weather data
            weather_group = rank_group(weather_ts,test_weather_ts[n])['Day'][:30]
    
            print('{} - group length:{}'.format(n,len(weather_group)))
            if len(weather_group) < 10:
                predictions.append('len<')
                continue
            
    
            # reshape to row array to concatenate
            test_data_point = test_MVs_ts[MV_index,n].reshape((1,MVs_ts[MV_index,weather_group].shape[1]))
            # concatenated matrix of training data and the test data sample
            NT_data = np.concatenate((MVs_ts[MV_index,weather_group],test_data_point),axis = 0)
            
            LOF = LocalOutlierFactor(n_neighbors = 10,metric='precomputed',contamination = contam)
            D = gen_dist_mat(NT_data) # distance matrix
            
            # if distance matrix are all zeros(all TS are identical), then skip this
            if len(D[D == 0]) == D.shape[0]*D.shape[1]:
                predictions.append('D=0')
                continue
                
            pred = LOF.fit_predict(D)
            predictions.append(str(pred[-1])) # change to string to avoid comparison error in numpy later
            
            # if detected as outlier, save plot of MVs
            if pred[-1] == -1 and savefig_:
                plt.figure()
                # # draw only the current MV-----
                for c in weather_group:
                    plt.plot(MVs_ts[MV_index,c],color='steelblue',alpha=0.5,linestyle='dotted')
                plt.plot(test_MVs_ts[MV_index,n],color='gold')
                #--------------------------------
                
                # # draw for all MVs-------------
                # for index in range(MVs_ts.shape[0]):
                #     for c in combination:
                #         plt.plot(MVs_ts[index,c],color=color_list[index],alpha=0.5,linestyle='dotted')
                #     plt.plot(test_MVs_ts[index,n],color='gold')
                # plt.show()
                # -------------------------------
                
                # dir_loc = r'C:\Users\James\Desktop\python_figs\rank\{}\{}\{}'.format(rank_method_name,experimentName,MVs[MV_index])
                dir_loc = fig_loc+r'\{}\{}\{}'.format(rank_method_name,experimentName,MVs[MV_index])
                
                # check directory if exists
                if not os.path.exists(dir_loc):
                    os.makedirs(dir_loc)
                # save faulty plot
                plt.savefig(dir_loc + '\\n{}.png'.format(n))
                plt.close()
            
        MV_predictions.append(np.array(predictions))
    
    
    p_fault = np.empty(MV_predictions[0].shape,dtype = np.bool) # faulty
    p_normal = np.empty(MV_predictions[0].shape,dtype = np.bool) # normal
    p_lack = np.empty(MV_predictions[0].shape,dtype = np.bool) # lack of data
    p_fault[:] = False
    p_normal[:] = True # False
    p_lack[:] = True # False
    for predictions in MV_predictions:
        p_fault = np.logical_or(p_fault, predictions=='-1')
        normal_with_identical = np.logical_or(predictions=='1',predictions=='D=0')
        p_normal = np.logical_and(p_normal,normal_with_identical)
        p_lack = np.logical_and(p_lack, predictions=='len<')
        
    # the indices of ts sample which are considered faulty
    fault_index = np.arange(len(p_fault))[p_fault]
    normal_index = np.arange(len(p_normal))[p_normal]
    lack_index = np.arange(len(p_lack))[p_lack]
    
    # print results:
    fd_rate = 'Fault detection rate:\t {}%'.format(len(fault_index)/test_weather_ts.shape[0]*100)
    nd_rate = 'Normal operation rate:\t {}%'.format(len(normal_index)/test_weather_ts.shape[0]*100)
    ld_rate = 'Lack of data rate:\t {}%'.format(len(lack_index)/test_weather_ts.shape[0]*100)
    
    print(fd_rate)
    print(nd_rate)
    print(ld_rate)
    
    # Save results:
    # dir_loc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank\{}\{}'.format(rank_method_name,experimentName)
    dir_loc = result_loc+r'\{}\{}'.format(rank_method_name,experimentName)
    
    # check directory if exists
    if not os.path.exists(dir_loc):
        os.makedirs(dir_loc)
        
    with open(dir_loc+'\\results.txt','w') as f:
        f.write(fd_rate + '\n' + nd_rate+ '\n' + ld_rate)
    
    # save prediction results
    predArr_lof = np.array(MV_predictions).T # NF format(row:day/sample, col:MV)
    header = np.array(MVs).reshape(1,len(MVs)) # add header
    predArr_lof = np.concatenate((header,predArr_lof),axis = 0)
    np.savetxt(dir_loc+'\\MV_predictions.csv',predArr_lof,fmt='%s',delimiter=',')
    
    
    
    
    
    
    # Isolation Forest
    
    from sklearn.ensemble import IsolationForest
    from myFunctions import gen_dist_mat
    
    #
    experimentName = '{}_IsolationForest'.format(testdata_name)
    # Choose ranking method
    # rank_group = rank_high_low
    rank_group = rank_methods[rank_method_index]
    rank_method_name = rank_methods_names[rank_method_index]
    
    # test_weather_ts = test_EVs_ts[0] # test weather data
    
    # MV_index = 0 # MV we are examining
    MV_predictions = []
    for MV_index in range(len(MVs)):
        predictions = []
        for n in range(test_weather_ts.shape[0]):
            # The 20th closest weather data
            weather_group = rank_group(weather_ts,test_weather_ts[n])['Day'][:30]
            
            print('{} - group length:{}'.format(n,len(weather_group)))
            if len(weather_group) < 10:
                predictions.append('len<')
                continue
            
    
            # reshape to row array to concatenate
            test_data_point = test_MVs_ts[MV_index,n].reshape((1,MVs_ts[MV_index,weather_group].shape[1]))
            # concatenated matrix of training data and the test data sample
            NT_data = np.concatenate((MVs_ts[MV_index,weather_group],test_data_point),axis = 0)
            
            D = gen_dist_mat(NT_data) # distance matrix
            
            # if distance matrix are all zeros(all TS are identical), then skip this
            if len(D[D == 0]) == D.shape[0]*D.shape[1]:
                predictions.append('D=0')
                continue
            
            IsoForest = IsolationForest(contamination = contam)
            IsoForest.fit(NT_data)
            pred = IsoForest.predict(NT_data)    
            
            predictions.append(str(pred[-1])) # change to string to avoid comparison error in numpy later
            
            # if detected as outlier, save plot of MVs
            if pred[-1] == -1 and savefig_:
                plt.figure()
                # # draw only the current MV-----
                for c in weather_group:
                    plt.plot(MVs_ts[MV_index,c],color='steelblue',alpha=0.5,linestyle='dotted')
                plt.plot(test_MVs_ts[MV_index,n],color='gold')
                #--------------------------------
                
                # # draw for all MVs-------------
                # for index in range(MVs_ts.shape[0]):
                #     for c in combination:
                #         plt.plot(MVs_ts[index,c],color=color_list[index],alpha=0.5,linestyle='dotted')
                #     plt.plot(test_MVs_ts[index,n],color='gold')
                # plt.show()
                # -------------------------------
                
                # dir_loc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank\{}\{}\{}'.format(rank_method_name,experimentName,MVs[MV_index])
                dir_loc = fig_loc+r'\{}\{}\{}'.format(rank_method_name,experimentName,MVs[MV_index])
                
                # check directory if exists
                if not os.path.exists(dir_loc):
                    os.makedirs(dir_loc)
                # save faulty plot
                plt.savefig(dir_loc + '\\n{}.png'.format(n))
                plt.close()
            
        MV_predictions.append(np.array(predictions))
    
    
    p_fault = np.empty(MV_predictions[0].shape,dtype = np.bool) # faulty
    p_normal = np.empty(MV_predictions[0].shape,dtype = np.bool) # normal
    p_lack = np.empty(MV_predictions[0].shape,dtype = np.bool) # lack of data
    p_fault[:] = False
    p_normal[:] = True # False
    p_lack[:] = True # False
    for predictions in MV_predictions:
        p_fault = np.logical_or(p_fault, predictions=='-1')
        normal_with_identical = np.logical_or(predictions=='1',predictions=='D=0')
        p_normal = np.logical_and(p_normal,normal_with_identical)
        p_lack = np.logical_and(p_lack, predictions=='len<')
        
    # the indices of ts sample which are considered faulty
    fault_index = np.arange(len(p_fault))[p_fault]
    normal_index = np.arange(len(p_normal))[p_normal]
    lack_index = np.arange(len(p_lack))[p_lack]
    
    # print results:
    fd_rate = 'Fault detection rate:\t {}%'.format(len(fault_index)/test_weather_ts.shape[0]*100)
    nd_rate = 'Normal operation rate:\t {}%'.format(len(normal_index)/test_weather_ts.shape[0]*100)
    ld_rate = 'Lack of data rate:\t {}%'.format(len(lack_index)/test_weather_ts.shape[0]*100)
    
    print(fd_rate)
    print(nd_rate)
    print(ld_rate)
    
    # Save results:
    # dir_loc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank\{}\{}'.format(rank_method_name,experimentName)
    dir_loc = result_loc+r'\{}\{}'.format(rank_method_name,experimentName)
    
    # check directory if exists
    if not os.path.exists(dir_loc):
        os.makedirs(dir_loc)
        
    with open(dir_loc+'\\results.txt','w') as f:
        f.write(fd_rate + '\n' + nd_rate+ '\n' + ld_rate)
    
    # save prediction results
    predArr_iForest = np.array(MV_predictions).T # NF format(row:day/sample, col:MV)
    header = np.array(MVs).reshape(1,len(MVs)) # add header
    predArr_iForest = np.concatenate((header,predArr_iForest),axis = 0)
    np.savetxt(dir_loc+'\\MV_predictions.csv',predArr_iForest,fmt='%s',delimiter=',')
    # return prediction results
    return(predArr_lof,predArr_iForest)


## Run all tests:

# global parameters:

# Selected EVs
# EVs = ['WeatherData.y',
#        'RoomLoadData.y']
EVs = ['WeatherData.y']

# Selected MVs
# MVs = ['controlUnit.EOF',
#        'controlUnit.yOAD',
#        'controlUnit.ySAD',
#        'controlUnit.yRAD',
#        'controlUnit.yEAD',
#        'controlUnit.yHeating',
#        'controlUnit.yCooling']

# MVs for 3room model
MVs = ['controlUnit.yHeating',
       'controlUnit.yCooling',
       'vavbox.swVal.u',
       'vavbox.vavDamper.y',
       'vavbox2.swVal.u',
       'vavbox2.vavDamper.y',
       'vavbox3.swVal.u',
       'vavbox3.vavDamper.y'
       ]
# MVs = ['controlUnit.EOF',
#        'controlUnit.yOAD',
#        'controlUnit.ySAD',
#        'controlUnit.yRAD',
#        'controlUnit.yEAD',
#        'controlUnit.yHeating',
#        'controlUnit.yCooling',
#        'vavbox.PID_H.y',
#        'vavbox.PID_C.y',
#        'vavbox2.PID_H.y',
#        'vavbox2.PID_C.y',
#        'vavbox3.PID_H.y',
#        'vavbox3.PID_C.y']
       
# dictionary with MVs as keys, values are booleans, 
# if True, means the corresponding MV is an on/off switch and should use PAA
# n_seg: number of segments for PAA conversion
# n_seg = 22
# isOnOff = {'controlUnit.EOF' : True,
#            'controlUnit.yOAD' : True,
#            'controlUnit.ySAD' : True,
#            'controlUnit.yRAD' : True,
#            'controlUnit.yEAD' : True,
#            'controlUnit.yHeating' : False,
#            'controlUnit.yCooling' : False,
#            }

# ncp = 8640 # number of communication points for JModelica
# n_sec = int(86400/ncp) # one sample per n_sec seconds
# start_step = 2*360
# # estimate the number of samples
# T = 360*22 # 22 hours
# t = 360*22 # 22 hours
# i_step = 6*60 # 60 min
# n_samples = math.floor((T-t)/i_step) + 1


# 3room model
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
ncp = 4320 # number of communication points for JModelica
n_sec = int(86400/ncp) # one sample per n_sec seconds
start_step = int((24-n_seg) * 60*60/n_sec) #2*180
# estimate the number of samples
T = int(60*60/n_sec * n_seg) #180*22 # 22 hours
t = int(60*60/n_sec * n_seg) #180*22 # 22 hours
i_step = int(60/n_sec * 60) #3*60 # 60 min
n_samples = math.floor((T-t)/i_step) + 1

# ------------------------------------------------------------------------------

# color list:
color_list = ['gold', 'darkcyan','slateblue', 'hotpink', 'indigo', 'firebrick', 'skyblue', 'coral', 'sandybrown', 'mediumpurple',  'forestgreen', 'magenta', 'seagreen', 'greenyellow', 'roaylblue', 'gray', 'lightseagreen']


# paths:
root_folder = 'L:\\HVAC_ModelicaModel_Data\\'
training_dataset = '210_HVACv6a_3room_Boston+LargeOffice_Workday'

# list of test data folder names:

# testdata_names = ['120_HVACv4a_Boston+SmallOffice_Weekday',
#                   '121_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault1',
#                   '122_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault2',
#                   '123_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault3',
#                   '124_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault5',
#                   '125_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault6',
#                   '126_HVACv4a_Weather_Boston+SmallOffice_Weekday_random',
#                   '127_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault1_OAD',
#                   '128_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault3_orifice',
#                   '129_HVACv4a_Weather_Boston+SmallOffice_Weekday_Fault6_2'
#                  ]

# testdata_names = ['130_HVACv4a_Boston+SmallOffice_Workday',
#                   '131_HVACv4a_Boston+SmallOffice_Workday_random',
#                   '132_HVACv4a_Boston+SmallOffice_Workday_Fault1',
#                   '133_HVACv4a_Boston+SmallOffice_Workday_Fault2',
#                   '134_HVACv4a_Boston+SmallOffice_Workday_Fault3',
#                   '135_HVACv4a_Boston+SmallOffice_Workday_Fault5',
#                   '136_HVACv4a_Boston+SmallOffice_Workday_Fault6',
#                   '137_HVACv4a_Boston+SmallOffice_Workday_Fault1_OAD',
#                   '138_HVACv4a_Boston+SmallOffice_Workday_Fault3_orifice',
#                   '139_HVACv4a_Boston+SmallOffice_Workday_Fault6_2'
#                  ]
                 
# testdata_names = ['140_HVACv4a_SF+SmallOffice_Workday',
#                   '141_HVACv4a_SF+SmallOffice_Workday_random',
#                   '142_HVACv4a_SF+SmallOffice_Workday_Fault1',
#                   '143_HVACv4a_SF+SmallOffice_Workday_Fault2',
#                   '144_HVACv4a_SF+SmallOffice_Workday_Fault3',
#                   '145_HVACv4a_SF+SmallOffice_Workday_Fault5',
#                   '146_HVACv4a_SF+SmallOffice_Workday_Fault6',
#                   '147_HVACv4a_SF+SmallOffice_Workday_Fault1_OAD',
#                   '148_HVACv4a_SF+SmallOffice_Workday_Fault3_orifice',
#                   '149_HVACv4a_SF+SmallOffice_Workday_Fault6_2'
#                  ]           

# testdata_names = ['150_HVACv4a_SF+LargeOffice_Workday',
#                   '151_HVACv4a_SF+LargeOffice_Workday_random',
#                   '152_HVACv4a_SF+LargeOffice_Workday_Fault1',
#                   '153_HVACv4a_SF+LargeOffice_Workday_Fault2',
#                   '154_HVACv4a_SF+LargeOffice_Workday_Fault3',
#                   '155_HVACv4a_SF+LargeOffice_Workday_Fault5',
#                   '156_HVACv4a_SF+LargeOffice_Workday_Fault6',
#                   '157_HVACv4a_SF+LargeOffice_Workday_Fault1_OAD',
#                   '158_HVACv4a_SF+LargeOffice_Workday_Fault3_orifice',
#                   '159_HVACv4a_SF+LargeOffice_Workday_Fault6_2'
#                  ]         

# testdata_names = ['160_HVACv4a_Boston+LargeOffice_Workday',
#                   '161_HVACv4a_Boston+LargeOffice_Workday_random',
#                   '162_HVACv4a_Boston+LargeOffice_Workday_Fault1',
#                   '163_HVACv4a_Boston+LargeOffice_Workday_Fault2',
#                   '164_HVACv4a_Boston+LargeOffice_Workday_Fault3',
#                   '165_HVACv4a_Boston+LargeOffice_Workday_Fault5',
#                   '166_HVACv4a_Boston+LargeOffice_Workday_Fault6',
#                   '167_HVACv4a_Boston+LargeOffice_Workday_Fault1_OAD',
#                   '168_HVACv4a_Boston+LargeOffice_Workday_Fault3_orifice',
#                   '169_HVACv4a_Boston+LargeOffice_Workday_Fault6_2'
#                   ]


# testdata_names = ['201_HVACv6a_3room_Boston+SmallOffice_Workday_random',
#                   '202_HVACv6a_3R_Boston+SmallOffice_Fault1',
#                   '203_HVACv6a_3R_Boston+SmallOffice_Fault2',
#                   '204_HVACv6a_3R_Boston+SmallOffice_Fault3',
#                   '205_HVACv6a_3R_Boston+SmallOffice_Fault4',
#                   '206_HVACv6a_3R_Boston+SmallOffice_Fault5'
#                   ]
                  
testdata_names = ['211_HVACv6a_3room_Boston+LargeOffice_Workday_random',
                  '212_HVACv6a_3room_Boston+LargeOffice_Fault1',
                  '213_HVACv6a_3room_Boston+LargeOffice_Fault2',
                  '214_HVACv6a_3room_Boston+LargeOffice_Fault3',
                  '215_HVACv6a_3room_Boston+LargeOffice_Fault4',
                  '216_HVACv6a_3room_Boston+LargeOffice_Fault5'
                  ]

# testdata_names = ['221_HVACv6a_3room_SF+SmallOffice_Workday_random',
#                   '222_HVACv6a_3room_SF+SmallOffice_Fault1',
#                   '223_HVACv6a_3room_SF+SmallOffice_Fault2',
#                   '224_HVACv6a_3room_SF+SmallOffice_Fault3',
#                   '225_HVACv6a_3room_SF+SmallOffice_Fault4',
#                   '226_HVACv6a_3room_SF+SmallOffice_Fault5'
                  ]

# testdata_names = ['231_HVACv6a_3room_SF+LargeOffice_Workday_random',
#                   '232_HVACv6a_3room_SF+LargeOffice_Fault1',
#                   '233_HVACv6a_3room_SF+LargeOffice_Fault2',
#                   '234_HVACv6a_3room_SF+LargeOffice_Fault3',
#                   '235_HVACv6a_3room_SF+LargeOffice_Fault4',
#                   '236_HVACv6a_3room_SF+LargeOffice_Fault5'
#                   ]


# load training data: these become global data
weather_ts,MVs_ts = load_training_data(root_folder,training_dataset)

# load rank methods: these are global lists of funtions and names
# rank_methods = [rank_high_low,
#                 rank_euclidean,
#                 rank_abs,
#                 rank_SAX
#                ]
# rank_methods_names = ['High-low','Euclidean','Absolute','SAX']
rank_methods = [rank_high_low,
                rank_euclidean
               ]
rank_methods_names = ['High-low','Euclidean']

# contamination levels:
# contam_values = np.arange(0.025,0.225,0.025)
contam_values = np.array([0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,
                          0.020,0.040,0.080,0.100,0.200,0.300,0.400,0.500])
# contam_values = np.array([0.01,0.02,0.04,0.06,0.08])
# contam_values = np.array([0.01])
# contam_values = np.array([0.1]) # default

# save figure
savefig_ = False # True


# output paths:
fig_loc = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+LargeOffice'
result_loc = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+LargeOffice'

# for each contamination values
for contamination in contam_values:
    fig_loc2 = fig_loc + '\\contamination_{}'.format(contamination)
    result_loc2 = result_loc + '\\contamination_{}'.format(contamination)
    # for each rank methods, load test data and run anomaly tests:
    for rank_method_index in range(len(rank_methods)):
        for testdata_name in testdata_names:
            test_EVs_ts,test_MVs_ts = load_test_data(root_folder,testdata_name)
            predArr_lof,predArr_iForest = anomaly_detection(testdata_name,rank_method_index,
                                                            test_EVs_ts,test_MVs_ts,fig_loc2,result_loc2,
                                                            contamination,savefig_=savefig_)
            # anomaly_detection(testdata_name,rank_method_index,test_EVs_ts,test_MVs_ts)
            # print('{}\n{}'.format(testdata_name,rank_methods_names[rank_method_index]))
        



# rank_methods = [rank_methods[-1]]
# rank_methods_names = [rank_methods_names[-1]]
# testdata_names = testdata_names[3:]





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

## Parse results

def parse_result(file):
    with open(file,'r') as f:
        content = f.read()
    lines = content.split('\n')
    fd_rate = lines[0].split('\t ')[1]
    nd_rate = lines[1].split('\t ')[1]
    ld_rate = lines[2].split('\t ')[1]
    # convert to float
    fd_rate = float(fd_rate[:-1])
    nd_rate = float(nd_rate[:-1])
    ld_rate = float(ld_rate[:-1])
    
    return([fd_rate,nd_rate,ld_rate])
## Parse and export to csv

# fileLoc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday'

root_loc = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+LargeOffice'

# for contam in os.listdir(root_loc):
for contam in [s for s in os.listdir(root_loc) if os.path.isdir(root_loc+'\\'+s)]:
    fileLoc = root_loc + '\\' + contam

    rank_methods_names = [dir for dir in os.listdir(fileLoc) if os.path.isdir(fileLoc+'\\'+dir)]
    subdirs = [fileLoc+'\\'+dir for dir in os.listdir(fileLoc) if os.path.isdir(fileLoc+'\\'+dir)]
    
    # N = len(subdirs)
    table = []
    dfs = [] # list of pandas dataframes
    excelWriter = pd.ExcelWriter(fileLoc + '\\All_results.xlsx') # pandas excel writer
    
    for i,subdir in enumerate(subdirs):
        print(rank_methods_names[i])
        
        table_cols = []
        for subsubdir in os.listdir(subdir):
            resultFile = subdir + '\\' + subsubdir + '\\' + 'results.txt'
            if os.path.exists(resultFile):
                print(subsubdir)
                print(parse_result(resultFile))
                rates = parse_result(resultFile)
                rates.insert(0,subsubdir)
                table_cols.append(np.array(rates))
                
        table_cols = np.array(table_cols)
        # save
        table_cols_df = pd.DataFrame(table_cols)
        table_cols_df.columns = ['Experiment','Fault detection rate',
                                'Normal operation rate','Lack of data rate']
        table_cols_df.to_csv(fileLoc+'\\'+ rank_methods_names[i] + '_results.csv')
        
        # Save to excel sheet
        table_cols_df.to_excel(excelWriter,rank_methods_names[i])
        dfs.append(table_cols_df)   
        
        # np.savetxt(fileLoc+'\\'+ rank_methods_names[i] + '_results.csv',table_cols,
        #            delimiter=',',fmt='%0.4f')
    
        table.append(table_cols)
    
    # construct header:
    header = [''] # initialize
    for subdir in subdirs:
        header.append('')
        header.append(os.path.basename(subdir)) # os.path.basename returns the folder name
        
    # Put all sheets together into a new sheet
    first_col = table_cols_df['Experiment']
    df = first_col
    
    for sheet in dfs:
        df = pd.concat((df,sheet[['Fault detection rate','Normal operation rate']]),axis=1)
    # df.to_excel(excelWriter,'All',header=header)
    df.to_excel(excelWriter,'All') # write df to worksheet
    
    
    # Manually add additional row as header
    all_worksheet = excelWriter.sheets['All'] # select worksheet
    all_worksheet.insert_rows(1) # insert row
    for c,val in enumerate(header): # write values to cells
        all_worksheet.cell(1,c+1,val)
        
    
    excelWriter.save() # Save excel file


## Convert excel files to csv files

def xls2csv(file,save_file,sheet_name):
    '''
    uses packages: pandas, xlrd
    '''
    import pandas as pd
    df = pd.read_excel(file,header=None)
    df.to_csv(save_file,index=None,header=None)
    print('{} has saved to {}'.format(file,save_file))


## Combine all 'All_results.xlsx' files

root_loc = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+LargeOffice'

folders = [s for s in os.listdir(root_loc) if os.path.isdir(root_loc+'\\'+s)]

contams = []
all_arr = []
for folder in folders:
    contam = folder.split('_')[-1]
    contams.append(contam)
    
    file_loc = root_loc + '\\' + folder + '\\All_results.xlsx'
    df = pd.read_excel(file_loc,sheet_name = 'All',header = None)
    arr = np.array(df)
    all_arr.append(arr[:,2:])
index_col = arr[:,1]

stackedArr = np.empty((all_arr[0].shape[0]+2 , all_arr[0].shape[1]*len(all_arr)+1),dtype=np.object)
stackedArr[2:,0] = index_col
stackedArr[0,0] = 'Contamination'
stackedArr[1,0] = 'Distance measure'
stackedArr[2,0] = 'Rates'
for n,i in enumerate(range(1,stackedArr.shape[1],all_arr[0].shape[1])):
    stackedArr[1:3,i:i+all_arr[0].shape[1]] = all_arr[n][0:2]
    stackedArr[3,i:i+all_arr[0].shape[1]] = ''
    stackedArr[4:,i:i+all_arr[0].shape[1]] = all_arr[n][2:]
    stackedArr[0,i:i+all_arr[0].shape[1]] = contams[n]
    
np.savetxt(root_loc + '\\all_contamination_results.csv',stackedArr,delimiter=',',fmt='%s')

# No longer need to manual make adjustments for this version
# '''
# Manually make adjustments in excel after previous step:
# 1. shift one row for Experiments
# 2. add column names
# 
# This would be much faster than coding
# '''

# Load pivot table:
# test_file = r'N:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+SmallOffice_Workday\\all_contamination_results.csv'
test_file = root_loc + '\\' + 'all_contamination_results.csv'
df = parse_pivot_from_file(test_file,data_row = 4,data_col = 1, mode=0)

# separate IsolationForest and LOF Experiment labels:
# df = df.reset_index(level=0,drop=True)

# indices
aa = [] # anomaly algorithms
ex = [] # experiments
for index in df.index:
    ss = index[0].split('_')
    aa.append(ss[-1])
    ex.append(index[0][:-len(ss[-1])-1])
aa = pd.Series(aa,name='Anomaly algorithm')
ex = pd.Series(ex,name='Experiment')

df.index = pd.MultiIndex.from_arrays([aa,ex],names = [aa.name,ex.name])

new_df = df.unstack().stack(0)
new_df.columns = new_df.columns.swaplevel(0,2)
new_df.columns = new_df.columns.swaplevel(1,2)

# new_df.to_csv(r'N:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+SmallOffice_Workday\all_contamination_classified.csv')
new_df.to_csv(root_loc + '\\' + 'all_contamination_classified.csv')





## Load data

# Stacked Data
data_loc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\AllDataStacked.csv'
df = pd.read_csv(data_loc)
# pivot table
df_pivot = df.pivot_table(values=['Fault detection rate','Normal operation rate'],
               index=['Anomaly algorithm','contamination','rank method'],
               columns = ['Fault group']
              )
df2 = df_pivot.xs(('LOF','Euclidean'),level=[0,2])

df2.columns = df2.columns.swaplevel(0,1) # swap MultiIndex cloumn levels

TPR = 100-df2[df2.columns[1]] # True Postives Rate


FPRs = []
for col in df2.columns:
    if col[1] == 'Fault detection rate': FPRs.append(df2[col[0]]['Fault detection rate'])
    # print(col[0])
    # print(df2[col[0]])
    # print(df2[col[0]].shape)
FPRs = FPRs[2:] # remove first 2 TP datasets

# plot
plt.figure()
for i,FPR in enumerate(FPRs):
    index = 420 + i + 1
    ax = plt.subplot(index)
    
    # plt.plot((100-FPR)/100,TPR/100,color = my_colors[i])
    # plt.plot([0,1],[0,1],color='gray',linestyle=':')
    plt.plot(TPR/FPR,color = my_colors[i],linestyle=':')
plt.show()

## practice loading pivot table from file
# df2.to_csv(r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\pivot.csv')
df3 = pd.read_csv(r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\test.csv',header=None)

# reconstruct pivot table from csv file:
arr = np.array(df3)
data_arr = arr[4:,2:] # data values

# multi index columns
cols_names = list(arr[:2,1])
cols_names.append('Rates')

contams = [x for x in np.array(arr[0][2:],dtype=float) if not np.isnan(x)]
rank_methods = [x for x in arr[1][2:] if type(x)==str]
rank_methods = list(set(rank_methods))
rank_methods.sort()
rates = list(set(arr[2][2:]))
rates.sort()

micol_arr =np.empty((3,len(contams)*len(rank_methods)*len(rates)),dtype=np.object)
for i,contam in enumerate(contams):
    n1 = len(rank_methods)*len(rates)
    s1 = i*n1
    e1 = (i+1)*n1
    micol_arr[0,s1:e1] = contam
    for j,rank_method in enumerate(rank_methods):
        n2 = len(rates)
        s2 = s1 + j*n2
        e2 = e1 + (j+1)*n2
        micol_arr[1,s2:e2] = rank_method
        for k,rate in enumerate(rates):
            s3 = s2 + k
            e3 = e2 + k
            micol_arr[2,s3:e3] = rate
micolumns = pd.MultiIndex.from_arrays(micol_arr,names=cols_names)

# index
row_names = arr[3:,1]

# recovered data frame
df_load = pd.DataFrame(data_arr,index = row_names,columns=micolumns)
df_load.index.name = 'Experiment'


## Pivot table parsing function

def parse_pivot_from_file(file,data_row,data_col, mode = 0):
    '''
    inputs:
        file: file location path
        data_row: data content starting row
        data_col: data content starting column
        mode: the format of pivot table in file,
              if column names are stacked at the end of index(row) names, use mode = 0(default)
              if column names are stacked at the start of index(row) names, use mode = 1
              For pandas saved pivot_table in csv files, use mode = 0
    outputs:
        df_load: recovered pivot table loaded from file
    '''
    import numpy as np
    import pandas as pd
    
    y_e = data_row - 1  # ending col name position
    x_e = data_col - 1  # ending row name position
    
    df = pd.read_csv(file,header = None) 
    
    # reconstruct pivot table from csv file:
    arr = np.array(df)
    data_arr = arr[data_row:,data_col:] # data content values

    # multi index rows
    # locate row names
    for x_s in range(x_e,-1,-1):
        if str(arr[y_e,x_s]) == '' or str(arr[y_e,x_s]) == 'nan':
            x_s += x_s
            break
    row_names = arr[y_e,x_s:x_e+1]
    
    # generate levels
    multirow_shape = (arr.shape[0] - data_row,len(row_names))
    mirow_arr = np.empty(multirow_shape,dtype=np.object)
    
    for col,row_name in enumerate(row_names):
        row = [x for x in arr[data_row:,col] if not (str(x)=='' or str(x)=='nan')]
        n = int(multirow_shape[0]/len(row))
        
        for i in range(len(row)):
            s = i*n
            e = s + n
            mirow_arr[s:e,col] = np.array([row[i] for x in range(n)])
    
    miindex = pd.MultiIndex.from_arrays(mirow_arr.T ,names=row_names) 


    # multi index columns
    # locate col names
    x_loc = x_s if mode==0 else x_e # mode
    for y_s in range(y_e,-1,-1):
        if str(arr[y_s,x_loc]) == '' or str(arr[y_s,x_loc]) == 'nan':
            y_s += y_s
            break
    col_names = arr[y_s:y_e,x_loc]
    
    # generate levels
    multicol_shape = (len(col_names),arr.shape[1] - data_col)
    micol_arr = np.empty(multicol_shape,dtype=np.object)
    
    for row,col_name in enumerate(col_names):
        col = [x for x in arr[row,data_col:] if not (str(x)=='' or str(x)=='nan')]
        n = int(multicol_shape[1]/len(col))
        
        for i in range(len(col)):
            s = i*n
            e = s + n
            micol_arr[row,s:e] = np.array([col[i] for x in range(n)])
            
    micolumns = pd.MultiIndex.from_arrays(micol_arr,names=col_names)   
        
    # cols_names = list(arr[:data_row-1,data_col-1])
    # row_names = arr[data_row:,col_e]
    
    # recovered data frame
    df_load = pd.DataFrame(data_arr,index = miindex,columns=micolumns)
    # df_load = pd.DataFrame(data_arr,index = row_names,columns=micolumns)
    # df_load.index.name = arr[data_row-1,data_col-1]
    
    return(df_load)

## test parsing saved pivot_table csv files    

test_file = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\test2.csv'
df2 = parse_pivot_from_file(test_file,data_row = 4,data_col = 2, mode=1)

test_file = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\test3.csv'
df3 = parse_pivot_from_file(test_file,data_row = 4,data_col = 1, mode=0) # both modes are ok
df3 = parse_pivot_from_file(test_file,data_row = 4,data_col = 1, mode=1)

test_file = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\test5.csv'
df5 = parse_pivot_from_file(test_file,data_row = 3,data_col = 2, mode=0)


## stack anomaly algorithms by adding index to multiindex structure
# df_stack = df.stack(0).unstack(0)
# df_stack.to_csv(r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\test3.csv')

df_if = df2.iloc[::2]
df_if.reset_index(level=0,drop=True,inplace = True)
index_if = pd.Series(['IsolationForest' for i in range(10)],name = 'Anomaly algorithm')
df_if.index = pd.MultiIndex.from_arrays([index_if,df_if.index],names=['Anomaly algorithm','Experiment'])


df_lof = df2.iloc[1::2]
df_lof.reset_index(level=0,drop=True,inplace=True)
index_lof = pd.Series(['LocalOutlierFactor' for i in range(10)],name = 'Anomaly algorithm')
df_lof.index = pd.MultiIndex.from_arrays([index_lof,df_lof.index],names=['Anomaly algorithm','Experiment'])


df = pd.concat([df_if,df_lof])
df.index

# df_if = df_if.unstack()
# df_if.index = pd.Series(['Isolation Forest' for i in range(10)],name = 'Anomaly algorithm')
# df_if = df_if.stack().unstack(0)

df.to_csv(r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\df.csv')

## Separate IsolationForest and LOF Experiment labels
# load file
test_file = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\test2.csv'
df = parse_pivot_from_file(test_file,data_row = 4,data_col = 2, mode=1)


new_df = df2.reset_index(level=0,drop=True)

# indices
aa = [] # anomaly algorithms
ex = [] # experiments
for index in new_df.index:
    ss = index.split('_')
    aa.append(ss[-1])
    ex.append(index[:-len(ss[-1])-1])
aa = pd.Series(aa,name='Anomaly algorithm')
ex = pd.Series(ex,name='Experiment')

new_df.index = pd.MultiIndex.from_arrays([aa,ex],names = [aa.name,ex.name])

new_df.to_csv(r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday\new_df.csv')






## Set parameters





## Compute classification results







## Get TP, FN, FP, TN values















## Compute TPR and FPR












## Get AUC(area under curve)


































