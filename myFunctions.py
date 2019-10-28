##
import numpy as np
import pandas as pd



## Common functions
'''
gen_FTN_data v2: added n_sec for different sampling rates
Input:
     - varNames: a list variable that has all the variable names
     - days: a list variable that lists out the days
     - n_sec: one sample per n_sec seconds
Output:
     - FTN: a dictionary with variable names as keys, and a TN format DataFrame as values
'''
def gen_FTN_data(varNames,days,filePath,fileNames,n_sec=10):
    F = len(varNames)
    N = len(days)
    # initialize output FTN dictionary with variable names as keys and empty lists as values
    FTN = dict([(i,[]) for i in varNames])
    
    for day in days:
        # read data from disk
        file = filePath + '\\' + fileNames[day]
        data = pd.read_csv(file) # TF format
        
        # get the columns we want
        df = data[varNames]
        # time increments/intervals may not be fixed, mark the indices
        # indices = data.time.round(-1).drop_duplicates().index
        indices = (data.time/n_sec).round(0).drop_duplicates().index
        # T = len(indices)
        df = df.iloc[indices]
        
        # append TS to list(NT format for now)
        for i in varNames:
            FTN[i].append(df[i])
        
        print('Finished with day {}'.format(day))    
    
    print('Preparing for data output')
    for key in FTN:
        FTN[key] = np.array(FTN[key]).T # tranpose from NT to TN format
        cols = ['day{}'.format(d) for d in days] # add column names
        FTN[key] = pd.DataFrame(FTN[key],columns = cols) # make data frame
    print('Done!')
    return(FTN)

# '''
# Input:
#      - varNames: a list variable that has all the variable names
#      - days: a list variable that lists out the days
# Output:
#      - FTN: a dictionary with variable names as keys, and a TN format DataFrame as values
# '''
# def gen_FTN_data(varNames,days,filePath,fileNames):
#     F = len(varNames)
#     N = len(days)
#     # initialize output FTN dictionary with variable names as keys and empty lists as values
#     FTN = dict([(i,[]) for i in varNames])
#     
#     for day in days:
#         # read data from disk
#         file = filePath + '\\' + fileNames[day]
#         data = pd.read_csv(file) # TF format
#         
#         # get the columns we want
#         df = data[varNames]
#         # time increments/intervals may not be fixed, mark the indices
#         indices = data.time.round(-1).drop_duplicates().index
#         # T = len(indices)
#         df = df.iloc[indices]
#         
#         # append TS to list(NT format for now)
#         for i in varNames:
#             FTN[i].append(df[i])
#         
#         print('Finished with day {}'.format(day))    
#     
#     print('Preparing for data output')
#     for key in FTN:
#         FTN[key] = np.array(FTN[key]).T # tranpose from NT to TN format
#         cols = ['day{}'.format(d) for d in days] # add column names
#         FTN[key] = pd.DataFrame(FTN[key],columns = cols) # make data frame
#     print('Done!')
#     return(FTN)

'''    
# This function is to transform the data format from NTF to FNT
# data is a list of matrices
'''
def transform_NTF2FNT(data):
    import numpy as np
    # dimensions
    N = len(data)
    T = data[0].shape[0]
    F = data[0].shape[1]
    
    # initialize
    data_transform = [] # FNT
    
    for f in range(F):
        NTmatrix = np.zeros((N,T))
        for n in range(N):
            TFmatrix = data[n] # read input NTF
            # reconstruct NT matrix
            for t in range(T):
                NTmatrix[n,t] = TFmatrix[t,f]
        # add to FNT
        data_transform.append(NTmatrix)
    
    return(data_transform)

'''
# This function is to transform the data format from FNT to NTF
# data is a list of matrices
'''
def transform_FNT2NTF(data):
    import numpy as np
    # dimensions
    F = len(data)
    N = data[0].shape[0]
    T = data[0].shape[1]
    
    # initialize
    data_transform = [] # NTF
    
    for n in range(N):
        TFmatrix = np.zeros((T,F))
        for f in range(F):
            NTmatrix = data[f] # read input FNT
            # reconstruct TF matrix
            for t in range(T):
                TFmatrix[t,f] = NTmatrix[n,t]
        # add to FNT
        data_transform.append(TFmatrix)
    
    return(data_transform)



'''
# Generate distance matrix (N*N)
# uses Euclidean distance if not assigned
# format should be NT
# T: number of time steps in the time series
# N: number of time series samples
'''
def gen_dist_mat(X,dist_func=None,print_ = False):
    import numpy as np
    from scipy.spatial import distance
    X = np.array(X)
    N,T = X.shape[0],X.shape[1]
    
    if dist_func is None:
        dist = distance.minkowski
    else:
        dist = dist_func
    
    # intialize distance matrix
    D = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if i==j: # identical
                D[i,j] = 0
            elif i > j: # distance matrix is symmetric, no need to compute twice
                D[i,j] = D[j,i]
            else:
                D[i,j] = dist(X[i,:],X[j,:])
        if print_: print('{}/{} finished'.format(i+1,N))
    return(D)


'''
Same as gen_dist_mat, but saves to hdf5 for large matrices(large N)
Distance matrix is saved in a file instead returned as variable
# Generate distance matrix (N*N)
# uses Euclidean distance if not assigned
# format should be NT
# T: number of time steps in the time series
# N: number of time series samples
# filePath: the file path for hdf5 file
# dset: the dataset name for the data in hdf5, e.g. f['dset']
'''
h5file = r'N:\HVAC_ModelicaModel_Data\DistanceMatrix\Dw_6h60m.h5'
dataset = 'Dw'


def gen_large_dist_mat(X,filePath,dset,dist_func=None,print_ = False):
    import numpy as np
    from scipy.spatial import distance
    import h5py
    # X = np.array(X)
    N,T = X.shape[0],X.shape[1]
    
    if dist_func is None:
        dist = distance.minkowski
    else:
        dist = dist_func
    
    # HDF5 file initialize
    f = h5py.File(filePath,'w')
    distMat = f.create_dataset(dset,shape=(N,N),dtype=np.float16,compression='gzip')
    # initialize row array
    row = np.empty((1,N),dtype=np.float32)
    
    # intialize distance matrix
    # D = np.empty((N,N))
    for i in range(N):
        for j in range(N):
            if i==j: # identical
                row[0,j] = 0
                # distMat[i,j] = 0
                # D[i,j] = 0
            # elif i > j: # distance matrix is symmetric, no need to compute twice
                # row[0,j] = distMat[j,i]
                # distMat[i,j] = distMat[j,i]
                # D[i,j] = D[j,i]
            else:
                row[0,j] = dist(X[i,:],X[j,:])
                # distMat = dist(X[i,:],X[j,:])
                # D[i,j] = dist(X[i,:],X[j,:])
        distMat[i,:] = row
        f.flush()
        if print_: print('{}/{} finished'.format(i+1,N))
    f.close()
    return(None)



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











