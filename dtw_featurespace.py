'''
Need to have DTW functions: 1. dtw 2. fastdtw package

'''
##

# This is just a dtw(X,Y) wrapper, to change the return values and order
def standard_dtw(X,Y):
    from dtw import dtw
    p,C,D = dtw(X,Y)
    return(D[-1,-1],p)

# This function is to transform the data format from NTF to FNT
# data is a list of matrices
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

# This function is to transform the data format from FNT to NTF
# data is a list of matrices
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
Input: new_sample, a new sample with TF formatted matrix
       referenceData, the reference sample in TF format
       new_sample and referenceData should have the same dimension (T,F)

Output: distVec, a vector of distance with dimenson F

'''
def dtw_distances(new_sample,referenceData,mode = 'fast'):
    import numpy as np
    from dtw import dtw
    from fastdtw import fastdtw
    # Set up DTW function, default is 3rd party's fastdtw
    if mode == 'fast':
        dtw_dist = fastdtw
    elif mode == 'standard':
        dtw_dist = standard_dtw
    
    new_sample = np.array(new_sample)
    referenceData = np.array(referenceData)
    # check shape
    T = new_sample.shape[0]
    F = new_sample.shape[1]
    # initialize
    distVec = np.zeros((F,))
    
    for f in range(F):
        distVec[f],p = dtw_dist(new_sample[:,f],referenceData[:,f])
    
    return(distVec)



    
'''
Input: data, a list of np.arrays

-- format: F: # of features
           N: # of samples
           T: # time series sampling frequency, length in time
           supported format: 'FNT'(default) and 'NTF'

Output: a dictionary of DTW distance matrices, with its keys as reference index
        and values as the corresponding DTW distance matrix
        D_dict[N_referenceIndex] = D[N,F]
'''
def dtw_train_distances(data,mode = 'fast',format = 'FNT'):
    import numpy as np
    from dtw import dtw
    from fastdtw import fastdtw
    # Set up DTW function, default is 3rd party's fastdtw
    if mode == 'fast':
        dtw_dist = fastdtw
    elif mode == 'standard':
        dtw_dist = standard_dtw
    
    # Check data format:
    if format == 'NTF':
        data = transform_NTF2FNT(data)
        print('Data format transformed from NTF to FNT')
    elif format == 'FNT':
        print('Data format: FNT')

    # Read data, data is a list of feature matrices, e.g. data = [X,Y,Z,...]
    # Feature matrix should be N by T (N,T)
    # Length in N and F should be consistent(fixed), T is arbitrary
    
    # FNT format:
    # data = np.array(data)
    F = len(data)
    N = data[0].shape[0]
    T = data[0].shape[1]
    
    
    # Build distance dictionary of matrices
    D_dict = {} # dictionary
    D_train = np.zeros((N,F)) # distance matrix place holder
    for ref_index in range(N):
        # Set up base reference: 
        f_ref = np.zeros((F,T)) # feature references
        for f in range(F):
            featureData = data[f]
            f_ref[f] = featureData[ref_index,:]
        # xref = X[ref_index,:]
        # yref = Y[ref_index,:]
        # cref = c[ref_index,:]
        
        
        
        # Set up feature distances
        f_dist = np.zeros((F,1)) # feature distances
        # calculate (N-1) distances
        for i in range(N):
            if i == ref_index: # comparing itself
                for f in range(F):
                    f_dist[f] = 0.
                # x_dist = y_dist = c_dist = 0.
                # D_train[i,0] = dist
            elif i < ref_index: # calculated before
                D_temp = D_dict[i]
                for f in range(F):
                    f_dist[f] = D_temp[ref_index,f]
                # x_dist = D_temp[ref_index,0]
                # y_dist = D_temp[ref_index,1]
                # c_dist = D_temp[ref_index,2]
            else:
                for f in range(F):
                    f_dist[f],p = dtw_dist(f_ref[f],featureData[i,:])
                # x_dist,p = fastdtw(xref,X[i,:])
                # y_dist,p = fastdtw(yref,Y[i,:])
                # c_dist,p = fastdtw(cref,c[i,:])
            
            # update distance matrix
            for f in range(F):
                D_train[i,f] = f_dist[f]
            # D_train[i,0] = x_dist
            # D_train[i,1] = y_dist
            # D_train[i,2] = c_dist
        
        # update dictionary
        D_dict[ref_index] = D_train.copy() # use copy, or else is only a reference
        print('Computing {} of {}...'.format(ref_index+1,N))
    
    return(D_dict)
    
    
    
    
    
    
    
    
    
    
    