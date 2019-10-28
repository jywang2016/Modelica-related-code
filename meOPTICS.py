# # Get this current script file's directory:
# import os,inspect
# loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# # Set working directory
# os.chdir(loc)


import numpy as np


## class
class DataPoint:
    def __init__(self,index):
        self.core_dist = None # core distance
        self.r_dist = None # reachability distance
        self.processed = False # flag for processed
        # index of point, need indexing because we would be dealing with time-series,
        # may only have a distance matrix and don't have the coordinates
        self.index = index
        self.clusterID = None # cluster ID (label)

class meOPTICS:
    def __init__(self,coords,eps,eps2,MinPts,D = None,xi = 0.05):
        '''
        inputs:
            coords: data matrix of coordinates, in NF format (N by F)
            eps: the maximum distance (radius) to consider
            eps2: parameter epsilon prime < epsilon in OPTICS
            MinPts: parameter of min points used for LOF, default is 10
            D: distance matrix (N by N), if not provided, will generate one)
            xi: parameter for xi-steep points, 0 < xi < 1, default is set to 0.05
        ------------------------------------
        Initializes meOPTICS
        needs numpy and scipy
        '''
        self.coords = coords
        self.eps = eps
        self.eps2 = eps2
        self.MinPts = MinPts
        if D is None:
            from scipy.spatial import distance
            dist = distance.minkowski
            D = self.gen_dist_mat(coords,dist)
        self.D = D
        self.xi = xi
        
        # initialize data points
        DPs = [] # list of data points
        for i,datapoint in enumerate(coords):
            p = DataPoint(i)
            DPs.append(p)
        self.DPs = DPs
        
        # initialize nearest neighbors
        self.NN, self.NN_dists = nearest_neighbors(None,MinPts,D)
    
    
    def fit(self):
        '''
        Runs OPTICS
        ----------------------
        outputs:
            order_list: returns the order_list with cluster ID/label for the DataPoints(class)
        '''
        order_list = self.get_order()
        order_list = self.cluster(order_list)
        return(order_list)
        
        
        
    
    def get_order(self):
        '''
        inputs from class attributes: 
            DPs: list of Data points(class DataPoints)
            D: distance matrix (N by N)
            eps: the radius parameter epsilon for OPTICS
            MinPts: parameter of min points used for OPTICS
        outputs:
            order_list: list of DataPoints(class) with OPTICS' ordering
        '''
        # initialize parameters
        D = self.D
        DPs = self.DPs
        eps = self.eps
        MinPts = self.MinPts
        NN_dists = self.NN_dists
        # initialize order_list
        order_list = []
        
        # NN,NN_dists = nearest_neighbors(None,MinPts,D)
        
        for p in DPs:
            if not p.processed:
                neighbor_index = get_neighbors(p.index,eps,D)
                number_of_neighbors = neighbor_index.shape[0]
                p.processed = True
                order_list.append(p)
                
                # if core distance is not defined, means reachability distance is not defined as well,
                # and the point is not a core object
                # expand the cluster order only if the point is a core object
                if core_distance(p,NN_dists,number_of_neighbors) != None:
                    seeds = [] # initialize orderseeds
                    seeds = self.update_seeds(seeds,p,neighbor_index,D)
                    
                    while len(seeds)>0: # while seeds is not empty
                        # the smallest reachability-distance in the seed-list is selected by the method OrderSeeds:next().
                        # c = seeds[0] # current object(datapoint) // OrderSeeds.Next()
                        c = seeds.pop(0) # current object(datapoint) // OrderSeeds.Next()
                        c_neighbors = get_neighbors(c.index,eps,D)
                        c.processed = True
                        c.core_dist = core_distance(c,NN_dists,c_neighbors.shape[0])
                        order_list.append(c)
                        
                        if not c.core_dist is None:
                            seeds = self.update_seeds(seeds,c,c_neighbors,D)
                        
        return(order_list)
    
                    
    def update_seeds(self,seeds,p,neighbors,D):
        '''
        inputs:
            seeds: list of the order seeds
            p: the datapoint
            neighbors: list of neighbor indices
            D: distance matrix (N by N)
        outputs:
            seeds: list of the updated order seeds
        '''
        # initialize parameters
        NN_dists = self.NN_dists
        DPs = self.DPs
        
        c_dist = core_distance(p,NN_dists,neighbors.shape[0])
        
        for o_index in neighbors:
            o = DPs[o_index]
            
            if not o.processed:
                new_r_dist = np.max([c_dist,D[p.index,o.index]])
                if o.r_dist is None:
                    o.r_dist = new_r_dist
                    seeds.append(o)
                else: # object already in seeds
                    if new_r_dist < o.r_dist:
                        o.r_dist = new_r_dist
                        
                        
        # OrderSeeds are sorted by their reachability-distance
        # sort seeds wrt r_dist, use structured np.array
        
        # numpy sort doesn't support object type
        #
        # dtype = [('r_dist',float),('datapoint',object)]
        # N = len(seeds)
        # seedsArr = np.empty((N,),dtype=dtype)
        # seedsArr['datapoint'] = np.array(seeds)
        # for i,ob in enumerate(seeds):
        #     seedsArr['r_dist'][i] = seeds[i].r_dist
        # seedsArr = np.sort(seedsArr,order='r_dist')
        # # seeds sorted wrt reachability-distance
        # seeds = list(seedsArr['datapoint'])
        
        dtype = [('r_dist',float),('index',int)]
        N = len(seeds)
        seedsArr = np.empty((N,),dtype=dtype)
        seedsArr['index'] = np.arange(N)
        for i,ob in enumerate(seeds):
            seedsArr['r_dist'][i] = seeds[i].r_dist
        seedsArr = np.sort(seedsArr,order='r_dist')
        # seeds sorted wrt reachability-distance
        seeds = list(np.array(seeds)[seedsArr['index']])
                    
        return(seeds)
        
    
    def cluster(self,order_list):
        '''
        Clustering by assigning a eps2 parameter, works as DBSCAN, also called ExtractDBSCAN-Clustering
        inputs:
            order_list: list of DataPoints(class) with OPTICS' ordering
        outputs:
            order_list: returns the order_list with cluster ID/label for the DataPoints(class)
        '''
        # initialize parameters
        eps2 = self.eps2
        MinPts = self.MinPts
        
        # clusterID = -1 # noise
        clusterID = 0
        
        for o in order_list:
            # assume UNDEFINED to be greater than any defined distance
            r_dist = np.inf if o.r_dist is None else o.r_dist
            c_dist = np.inf if o.core_dist is None else o.core_dist
            
            if r_dist > eps2:
                if c_dist <= eps2:
                    clusterID += 1 # next clusterID
                    o.clusterID = clusterID
                else:
                    o.clusterID = -1 # noise
            else:
                o.clusterID = clusterID
        return(order_list)
        
    
    def auto_cluster(self,order_list):
    # def auto_cluster(order_list):
        '''
        Automatically cluster data points using steep point extract cluster algorithm
        inputs:
            order_list: list of DataPoints(class) with OPTICS' ordering
        outputs:
            #order_list: returns the order_list with cluster ID/label for the DataPoints(class)
            clusters: a list of cluster areas [start,end] indices wrt to order_list
        ---------------------------------------------------------------------------------------
        Note: This outputs a hierachical list of clusters!
        '''
        # initialize parameter xi
        xi = self.xi
        MinPts = self.MinPts
        
        # find the steep upward/downward areas
        # SUAset,SDAset = max_steep_area(order_list,MinPts)
        SUAset,SDAset = self.max_steep_area(order_list)
        SUAset = np.array(SUAset) # row: steep upward area, col = start/end indices
        SDAset = np.array(SDAset) # row: steep downward area, col = start/end indices
        
        
        # initialize
        index = 1
        mib_g = 0 # global max in between
        N = len(order_list)
        SDAlist = [] # list of the wanted steep down areas(SetOfSteepDownAreas in paper)
        miblist = [] # list of steep down areas' mibs
        clusters = [] # set of clusters
        # lastSA = None # last found steep upward or downward area 
        
        while index < N-1:
            o = order_list[index]
            # max between end of last steep upward or downward area and current index
            # mib_g = np.max([mib_g , o.r_dist]) 
            mib_g = np.max([mib_g , o.r_dist]) if not o.r_dist is None else mib_g
            
            # # end of last steep upward or downward area 
            # if not lastSA is None:
            #     eoLast = order_list[lastSA[0][1]]
            #     mib_g = np.max([eoLast.r_dist , o.r_dist])
            # print('index:{}, mib_g:{}'.format(index,mib_g))
            
            if index in SDAset[:,0]: # start of a steep down area at index
                # find the SDA in SDAset
                SDA = SDAset[SDAset[:,0]== index]
                
                # update mib values: max between end of steep down region and current index
                for i,iSDA in enumerate(SDAlist):
                    eoSDA = iSDA[0][1] # end of steep down area index
                    ps = order_list[eoSDA:index] # all points between end of steep down area and current index
                    rs = [p.r_dist for p in ps] # reachability-distances
                    miblist[i] = np.max(rs)
                
                # # filter all steep down areas whose start*(1-xi) < mib_g
                # filter_indices = []
                # for i,iSDA in enumerate(SDAset):
                #     # "reachability-distance" of start of steep down area
                #     soSDA = order_list[iSDA[0]].r_dist
                #     if soSDA*(1-xi) < mib_g:
                #         filter_indices.append(i)
                # SDAset = np.delete(SDAset,filter_indices,axis = 0)
                        
                
                # Set local mib = 0
                miblist.append(0)
                # Add SDA to SDAlist
                SDAlist.append(SDA)
                # update index and mib_g
                index = SDA[0][1] + 1
                mib_g = order_list[index].r_dist # end of last steep upward or downward area 
                
                
                # last steep upward or downward area
                # lastSA = SDA
                
            elif index in SUAset[:,0]: # start of a steep up area at index
                # find the SUA in SUAset
                SUA = SUAset[SUAset[:,0]== index]
                
                # update mib values: max between end of steep down region and current index
                for i,iSDA in enumerate(SDAlist):
                    eoSDA = iSDA[0][1] # end of steep down area index
                    ps = order_list[eoSDA:index] # all points between end of steep down area and current index
                    rs = [p.r_dist for p in ps] # reachability-distances
                    miblist[i] = np.max(rs)
                
                # # filter all steep down areas whose start*(1-xi) < mib_g
                # filter_indices = []
                # for i,iSDA in enumerate(SDAset):
                #     # "reachability-distance" of start of steep down area
                #     soSDA = order_list[iSDA[0]].r_dist
                #     if soSDA*(1-xi) < mib_g:
                #         filter_indices.append(i)
                # SDAset = np.delete(SDAset,filter_indices,axis = 0)
                
                # update index and mib_g
                index = SUA[0][1] + 1
                mib_g = order_list[index].r_dist # end of last steep upward or downward area 
                
                for i,SDA in enumerate(SDAlist):
                    # check combiniation of U and D is valid
                    # find SDA's corresponing mib: just use enumerate
                    
                    # i = SDAlist.index(SDA)
                    # for i,iSDA in SDAlist:
                    #     if iSDA == SDA: break
                    mib = miblist[i]
                    
                    # compare: "reachability-distance" of end of SUA*(1-xi) >= mib
                    eoSUA = order_list[SUA[0][1]].r_dist
                    if eoSUA*(1-xi) >= mib:
                        
                        # cluster condition 4:
                        s_D = order_list[SDA[0][0]] # s_D
                        e_U = order_list[SUA[0][1]] # e_U
                        e_U1 = order_list[SUA[0][1]+1] # e_U+1
                        
                        if s_D.r_dist*(1-xi) >= e_U1.r_dist: # cluster condition 4b
                            # ps = order_list[np.arange(SDA[0][0],SDA[0][1]+1)] # all points in SDA
                            ps = order_list[SDA[0][0]:SDA[0][1]+1] # all points in SDA
                            rs = np.array([p.r_dist for p in ps]) # reachability-distances of points in SDA
                            # rs = rs[rs > e_U1.r_dist] 
                            s = ps[np.argmax(rs)] # point in SDA with max reachability-distance
                            e = e_U
                        elif e_U1.r_dist*(1-xi) >= s_D.r_dist: # cluster condition 4c
                            # ps = order_list[np.arange(SUA[0][0],SUA[0][1]+1)] # all points in SUA
                            ps = order_list[SUA[0][0]:SUA[0][1]+1] # all points in SUA
                            rs = np.array([p.r_dist for p in ps]) # reachability-distances of points in SUA
                            s = s_D
                            e = ps[np.argmin(rs)] # point in SUA with min reachability-distance
                        else: # cluster condition 4a
                            s = s_D
                            e = e_U
                        
                        # check cluster conditions 1,2,3a:
                        # condition 1: s in SDA
                        s_order_index = order_list.index(s)
                        cond1 = SDA[0][0] <= s_order_index <= SDA[0][1]
                        
                        # condition 2: e in SUA
                        e_order_index = order_list.index(e)
                        cond2 = SUA[0][0] <= e_order_index <= SUA[0][1]
                        
                        # condition 3a: e-s > MinPts
                        cond3a = e_order_index - s_order_index > MinPts
                        
                        # condition 3b is taken care by mib set up
                        
                        if (cond1 and cond2 and cond3a):
                            # clusters.append([s,e])
                            # store index wrt order_list
                            clusters.append([order_list.index(s),order_list.index(e)])
                        
                # last steep upward or downward area
                # lastSA = SUA    
                    
            else:
                index += 1        
            
        
        
        
        return(clusters)
        # return(order_list)
        
        
        
                
    def is_steep_point(self,order_list,p):
    # def is_steep_point(order_list,p):
        '''
        inputs:
            order_list: list of DataPoints(class) with OPTICS' ordering
            p: the datapoint
            parameter for xi-steep points, 0 < xi < 1
        outputs:
            verdict: 'U' if is an upward steep point, 'D' if is a downward steep point
                     'X' if is not a steep point
        ------------------------------------------------------------------------------
        Note: last point in order_list isn't defined upward or downward
        '''
        # initialize parameter xi
        xi = self.xi
        
        N = len(order_list)
        if p.index == order_list[-1].index:
            print('Last data point\'s steepness is undefined')
            return('X')
        
        order_indices = [o.index for o in order_list]
        # find p's index in order_list
        index = order_indices.index(p.index)
        # find next data point in order_list   # next_index = index + 1
        o = order_list[index + 1]
        
        verdict = 'X'
        if (not p.r_dist is None):
            if p.r_dist <= o.r_dist * (1-xi):
                verdict = 'U'
            elif o.r_dist <= p.r_dist * (1-xi):
                verdict = 'D'
            # else:
            #     verdict = 'X'
        
        return(verdict)
    
    def is_steep_area(self,order_list,s,e):
    # def is_steep_area(order_list,s,e,MinPts):
        '''
        Checks the first 3 conditions:
        1. s and e are steep upward/downward points
        2. reachability-distances are monotonically increasing/decreasing
        3. doesn't contain more than MinPts of consecutive non-steep points
        -----------------------------------------------------------------------
        inputs:
            order_list: list of DataPoints(class) with OPTICS' ordering
            s: starting data point in area
            e: ending data point in area
        outputs:
            verdict: 'UA' if is an upward steep area, 'DA' if is a downward steep area
                     'XA' if is not a steep point
        '''
        # initialize paramters
        MinPts = self.MinPts
        is_steep_point = self.is_steep_point
        
        # find start, end indices in order_list
        order_indices = [o.index for o in order_list]
        start_index = order_indices.index(s.index)
        end_index = order_indices.index(e.index)
        
        # check upward area
        cond1 =  is_steep_point(order_list,s) == 'U' and is_steep_point(order_list,e) == 'U'
        cond2 = True
        count = 0 # counter for condition 3: number of consecutive points that are not steep upward
        for i in range(start_index,end_index):
            cond2 = cond2 and (order_list[i].r_dist <= order_list[i+1].r_dist)
            if is_steep_point(order_list,order_list[i]) != 'U': count += 1
        cond3 = ( count < MinPts )
        
        # count = 0 # counter for condition 3: number of consecutive points that are not steep upward
        # for i in range(start_index,end_index):
        #     if is_steep_point(order_list,order_list[i]) != 'U': count += 1
        # cond3 = ( count < MinPts )
        
        upward = cond1 and cond2 and cond3
                
        # check downward area
        cond1 =  is_steep_point(order_list,s) == 'D' and is_steep_point(order_list,e) == 'D'
        cond2 = True
        count = 0 # counter for condition 3: number of consecutive points that are not steep downward
        for i in range(start_index,end_index):
            cond2 = cond2 and (order_list[i].r_dist >= order_list[i+1].r_dist)
            if is_steep_point(order_list,order_list[i]) != 'D': count += 1
        cond3 = ( count < MinPts )
        
        downward = cond1 and cond2 and cond3
        
        # assign verdict
        if upward:
            verdict = 'UA'
        elif downward:
            verdict = 'DA'
        else:
            verdict = 'XA'
        
        return(verdict)
        
    # def is_max_steep_area(self,order_list,s,e):    
    # def max_steep_area(order_list,s,e,MinPts):
    # def is_max_steep_area(self,order_list): 
    def max_steep_area(self,order_list):
        '''
        Checks the 4th condition: steep area is maximal
        -----------------------------------------------------------------------
        inputs:
            order_list: list of DataPoints(class) with OPTICS' ordering
            # s: starting data point in area
            # e: ending data point in area
        outputs:
            [USA,DSA]:
            - USA: list of upward steep areas
            - DSA: list of downward steep areas
                areas are defined by [starting index, ending index], indices wrt to order_list, not coords
        '''
        # initialize paramters
        MinPts = self.MinPts
        is_steep_point = self.is_steep_point
        is_steep_area = self.is_steep_area
        
        # # find start, end indices in order_list
        # order_indices = [o.index for o in order_list]
        # start_index = order_indices.index(s.index)
        # end_index = order_indices.index(e.index)
        
        # Get list of steep points
        steep_points = [is_steep_point(order_list,order_list[i]) for i in range(len(order_list)-1)]
        steep_points = np.array(steep_points)
        upward_index = np.arange(steep_points.shape[0])[steep_points == 'U']
        downward_index = np.arange(steep_points.shape[0])[steep_points == 'D']
        
        # I = None
        # # check upward areas
        # for i in upward_index:
        #     for j in upward_index:
        #         if I is None: I = [i,j] # if empty, assign an area
        #         # is upward area
        #         if (is_steep_area(order_list,order_list[i],order_list[j],MinPts) == 'UA'):
        #             # if area bigger, then assign to I
        #             if (i <= I[0] and j >= I[1]): I = [i,j]
        # 
        # 
        # I = None
        # # check downward areas
        # for i in downward_index:
        #     for j in downward_index:
        #         if I is None: I = [i,j] # if empty, assign an area
        #         # is downward area
        #         if (is_steep_area(order_list,order_list[i],order_list[j],MinPts) == 'DA'):
        #             # if area bigger, then assign to I
        #             if (i <= I[0] and j >= I[1]): I = [i,j]
        
        
        # find all upward areas
        USA = []
        for i,ui in enumerate(upward_index):
            for j,uj in enumerate(upward_index[i:]):
                # USA.append([ui,uj])
                # if (is_steep_area(order_list,order_list[ui],order_list[uj],MinPts) == 'UA'): USA.append([ui,uj])
                if (is_steep_area(order_list,order_list[ui],order_list[uj]) == 'UA'): USA.append([ui,uj])
        # include only max areas
        i = 0
        while i < len(USA):
            flag = False
            ui = USA[i]
            for j,uj in enumerate(USA):
                if ((uj[0] < ui[0] and uj[1] >= ui[1]) or (uj[0] <= ui[0] and uj[1] > ui[1])):
                    USA.pop(i)
                    flag = True
                    break
            if not flag: i += 1
        
        # find all downward areas
        DSA = []
        for i,ui in enumerate(downward_index):
            for j,uj in enumerate(downward_index[i:]):
                # if (is_steep_area(order_list,order_list[ui],order_list[uj],MinPts) == 'DA'): DSA.append([ui,uj])
                if (is_steep_area(order_list,order_list[ui],order_list[uj]) == 'DA'): DSA.append([ui,uj])
        # include only max areas
        i = 0
        while i < len(DSA):
            flag = False
            ui = DSA[i]
            for j,uj in enumerate(DSA):
                if ((uj[0] < ui[0] and uj[1] >= ui[1]) or (uj[0] <= ui[0] and uj[1] > ui[1])):
                    DSA.pop(i)
                    flag = True
                    break
            if not flag: i += 1
        
        return(USA,DSA)
        
                
        
        
        


    def gen_dist_mat(self,X,dist_func=None,print_ = False):
        '''
        inputs:
            X: data matrix in NT(or NF) format
            dist_func: distance measure used, if not specified, will use Euclidean distance
            print_: if set to True, will print out progress during computations
        Outputs:
            D: distance matrix (N by N)
        ---------------------------------------------------------
        # Generate distance matrix (N*N)
        # uses Euclidean distance if not assigned
        # format should be NT
        # T: number of time steps in the time series
        # N: number of time series samples
        '''
        # import numpy as np
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


    def nearest_neighbors(self,coords,k,D=None):
        '''
        inputs:
            coords: data coordinates in NF format, ignored if distance matrix D is provided
            k: Parameter MinPts, the k-nearest neighbors
            D: distance matrix, if not given, will use gen_dist_mat to generate one
        Outputs:
            NN_dists: k nearest neighbors distances matrix, np.array, (N by k)
            NN: k nearest neighbors matrix, np.array, (N by k)
                Contains the indices of coords, NOT the coordinates themselves
        '''
        # import numpy as np
        
        if D is None:
            from scipy.spatial import distance
            # from myFunctions import gen_dist_mat
            dist = distance.minkowski
            D = gen_dist_mat(coords,dist)
        
        N = D.shape[0]
        # initialize nearest neighbors
        NN_dists = np.empty((N,k),dtype=float)
        NN = np.empty((N,k),dtype=int)
        
        for i in range(N):
            # use numpy's structured array for sorting
            dtype = [('distance',float),('index',int)]
            structure_dist = np.empty((N,),dtype=dtype)
            structure_dist['distance'] = D[i]
            structure_dist['index'] = np.arange(N)
            structure_dist = np.sort(structure_dist,order='distance')
            
            # starts from 1 to remove itself, since the distance to itself is always 0
            NN_dists[i] = structure_dist['distance'][1:k+1] 
            NN[i] = structure_dist['index'][1:k+1] 
        
        return([NN,NN_dists])


    def get_neighbors(self,p_index,eps,D):
        '''
        inputs:
            p_index: data point index
            eps: the maximum distance (radius) to consider
            D: distance matrix
        Outputs:
            neighbor_index: a list of neighboring point indices with distance < eps
        '''
        eps = self.eps
        D = self.D
        
        N = D.shape[0]
        # initialize
        neighbor_index = []
        
        for i in range(N):
            if p_index != i: # exclude itself
                if D[p_index,i] < eps:
                    neighbor_index.append(i)
        
        neighbor_index = np.array(neighbor_index)
        return(neighbor_index)












## pure functions

def gen_dist_mat(X,dist_func=None,print_ = False):
    '''
    inputs:
        X: data matrix in NT(or NF) format
        dist_func: distance measure used, if not specified, will use Euclidean distance
        print_: if set to True, will print out progress during computations
    Outputs:
        D: distance matrix (N by N)
    ---------------------------------------------------------
    # Generate distance matrix (N*N)
    # uses Euclidean distance if not assigned
    # format should be NT
    # T: number of time steps in the time series
    # N: number of time series samples
    '''
    # import numpy as np
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
    
    

def k_dist(D,k = 4):
    '''
    inputs:
        D: distance matrix(N by N)
        k: k-th neighbor distance, default is 4
    '''
    # import numpy as np
    D = np.array(D)
    N = D.shape[0]
    # initialize k_dist vector
    k_dist = np.zeros((N,1))
    for i in range(N):
        row = list(D[i,:])
        for j in range(k): # remove min(row) k times, not k-1 times, because closest is always itself!
            row.remove(min(row))
        k_dist[i] = min(row)
    return(k_dist)


# def r_dist(DPs,D,k_distances,dist=None):
def r_dist(DPs,D,k_distances):
    '''
    inputs:
        # coords: other data points compared to p, in NF format, np.array((N,F))
        DPs: list of data points
        D: precomputed distance matrix(N by N)
        k_distances: a list of precomputed k-distances.
        #dist: distance function
    Outputs:
        r_dists: reachability distance matrix (p,o), distance of p(rows) from o(cols), (N by N)
    '''
    # import numpy as np
    # if dist is None:
    #     from scipy.spatial import distance
    #     dist = distance.minkowski
    
    # k_distances = k_dist(D,k=k)
    # reachability distances
    N = D.shape[0]
    r_dists = np.empty((N,N),dtype = float)
    
    for p in DPs:
        for o in DPs:
            r_dists[p.index,o.index] = np.max([k_distances[o.index],D[p.index,o.index]])
    # for i,p in enumerate(coords):
    #     for j,o in enumerate(coords):
    #         r_dists[i,j] = np.max([k_distances[j],dist(p,o)])
    
    return(r_dists)



def nearest_neighbors(coords,k,D=None):
    '''
    inputs:
        coords: data coordinates in NF format
        k: Parameter MinPts, the k-nearest neighbors
        D: distance matrix, if not given, will use gen_dist_mat to generate one
    Outputs:
        NN_dists: k nearest neighbors distances matrix, np.array, (N by k)
        NN: k nearest neighbors matrix, np.array, (N by k)
            Contains the indices of coords, NOT the coordinates themselves
    '''
    import numpy as np
    
    if D is None:
        from scipy.spatial import distance
        from myFunctions import gen_dist_mat
        dist = distance.minkowski
        D = gen_dist_mat(coords,dist)
    
    N = D.shape[0]
    # initialize nearest neighbors
    NN_dists = np.empty((N,k),dtype=float)
    NN = np.empty((N,k),dtype=int)
    
    for i in range(N):
        # use numpy's structured array for sorting
        dtype = [('distance',float),('index',int)]
        structure_dist = np.empty((N,),dtype=dtype)
        structure_dist['distance'] = D[i]
        structure_dist['index'] = np.arange(N)
        structure_dist = np.sort(structure_dist,order='distance')
        
        # starts from 1 to remove itself, since the distance to itself is always 0
        NN_dists[i] = structure_dist['distance'][1:k+1] 
        NN[i] = structure_dist['index'][1:k+1] 
    
    return([NN,NN_dists])
    

def get_neighbors(p_index,eps,D):
    '''
    inputs:
        p_index: data point index
        eps: the maximum distance (radius) to consider
        D: distance matrix (N by N)
    Outputs:
        neighbor_index: a list of neighboring point indices with distance < eps
    '''
    N = D.shape[0]
    # initialize
    neighbor_index = []
    
    for i in range(N):
        if p_index != i: # exclude itself
            if D[p_index,i] < eps:
                neighbor_index.append(i)
    
    neighbor_index = np.array(neighbor_index)
    return(neighbor_index)
    
def core_distance(p,NN_dists,number_of_neighbors):
    '''
    inputs:
        p: the datapoint
        NN_dists: k nearest neighbors distances matrix, np.array, (N by k)
        number_of_neighbors: number of neighboring points with distances < eps 
    Outputs:
       core_dist: the core-distance of datapoint p
    '''
    # MinPts: parameter of min points used for LOF, default is 10
    MinPts = NN_dists.shape[1] # NN_dists is (N by MinPts)
    
    if number_of_neighbors < MinPts:
        core_dist = None
    else:
        core_dist = NN_dists[p.index][-1]
    
    return(core_dist)
    
    
def get_order(DPs,D,eps,MinPts,NN_dists):
    '''
    inputs:
        DPs: list of Data points(class DataPoints)
        D: distance matrix (N by N)
        eps: the radius parameter epsilon for OPTICS
        MinPts: parameter of min points used for OPTICS
        NN_dists: k nearest neighbors distances matrix, np.array, (N by k=MinPts)
    outputs:
        order_list: list of DataPoints(class) with OPTICS' ordering
    '''
       
    order_list = []
    
    # NN,NN_dists = nearest_neighbors(None,MinPts,D)
    
    for p in DPs:
        if not p.processed:
            neighbor_index = get_neighbors(p.index,eps,D)
            number_of_neighbors = neighbor_index.shape[0]
            p.processed = True
            order_list.append(p)
            
            # if core distance is not defined, means reachability distance is not defined as well,
            # and the point is not a core object
            # expand the cluster order only if the point is a core object
            if core_distance(p,NN_dists,number_of_neighbors) != None:
                seeds = [] # initialize orderseeds
                seeds = update_seeds(DPs,seeds,p,neighbor_index,D,NN_dists)
                
                while len(seeds)>0: # while seeds is not empty
                    # the smallest reachability-distance in the seed-list is selected by the method OrderSeeds:next().
                    # c = seeds[0] # current object(datapoint) // OrderSeeds.Next()
                    c = seeds.pop(0) # current object(datapoint) // OrderSeeds.Next()
                    c_neighbors = get_neighbors(c.index,eps,D)
                    c.processed = True
                    c.core_dist = core_distance(c,NN_dists,c_neighbors.shape[0])
                    order_list.append(c)
                    
                    if not c.core_dist is None:
                        seeds = update_seeds(DPs,seeds,c,c_neighbors,D,NN_dists)
                    
    return(order_list)

                
def update_seeds(DPs,seeds,p,neighbors,D,NN_dists):
    '''
    inputs:
        seeds: list of the order seeds
        p: the datapoint
        neighbors: list of neighbor indices
        D: distance matrix (N by N)
    outputs:
        seeds: list of the updated order seeds
    '''
    c_dist = core_distance(p,NN_dists,neighbors.shape[0])
    
    for o_index in neighbors:
        o = DPs[o_index]
        
        if not o.processed:
            new_r_dist = np.max([c_dist,D[p.index,o.index]])
            if o.r_dist is None:
                o.r_dist = new_r_dist
                seeds.append(o)
            else: # object already in seeds
                if new_r_dist < o.r_dist:
                    o.r_dist = new_r_dist
                    
                    
    # OrderSeeds are sorted by their reachability-distance
    # sort seeds wrt r_dist, use structured np.array
    
    # numpy sort doesn't support object type
    #
    # dtype = [('r_dist',float),('datapoint',object)]
    # N = len(seeds)
    # seedsArr = np.empty((N,),dtype=dtype)
    # seedsArr['datapoint'] = np.array(seeds)
    # for i,ob in enumerate(seeds):
    #     seedsArr['r_dist'][i] = seeds[i].r_dist
    # seedsArr = np.sort(seedsArr,order='r_dist')
    # # seeds sorted wrt reachability-distance
    # seeds = list(seedsArr['datapoint'])
    
    dtype = [('r_dist',float),('index',int)]
    N = len(seeds)
    seedsArr = np.empty((N,),dtype=dtype)
    seedsArr['index'] = np.arange(N)
    for i,ob in enumerate(seeds):
        seedsArr['r_dist'][i] = seeds[i].r_dist
    seedsArr = np.sort(seedsArr,order='r_dist')
    # seeds sorted wrt reachability-distance
    seeds = list(np.array(seeds)[seedsArr['index']])
                
    return(seeds)
    

def cluster(order_list,eps2,MinPts):
    '''
    Clustering by assigning a eps2 parameter, works as DBSCAN, also called ExtractDBSCAN-Clustering
    inputs:
        order_list: list of DataPoints(class) with OPTICS' ordering
        eps2: parameter epsilon prime < epsilon in OPTICS
        MinPts: parameter of min points used for OPTICS
    outputs:
        order_list: returns the order_list with cluster ID/label for the DataPoints(class)
    '''
    
    # clusterID = -1 # noise
    clusterID = 0
    
    for o in order_list:
        # assume UNDEFINED to be greater than any defined distance
        r_dist = np.inf if o.r_dist is None else o.r_dist
        c_dist = np.inf if o.core_dist is None else o.core_dist
        
        if r_dist > eps2:
            if c_dist <= eps2:
                clusterID += 1 # next clusterID
                o.clusterID = clusterID
            else:
                o.clusterID = -1 # noise
        else:
            o.clusterID = clusterID
    return(order_list)
    
    

# def auto_cluster(order_list):
#     '''
#     Automatically cluster data points using steep point extract cluster algorithm
#     inputs:
#         order_list: list of DataPoints(class) with OPTICS' ordering
#     outputs:
#         clusters: a list of cluster areas [start,end] indices wrt to order_list
#     '''
#     # initialize parameter xi
#     # xi = self.xi
#     
#     # find the steep upward/downward areas
#     SUAset,SDAset = max_steep_area(order_list,MinPts)
#     SUAset = np.array(SUAset) # row: steep upward area, col = start/end indices
#     SDAset = np.array(SDAset) # row: steep downward area, col = start/end indices
#     
#     
#     # initialize
#     index = 1
#     mib_g = 0 # global max in between
#     N = len(order_list)
#     SDAlist = [] # list of the wanted steep down areas(SetOfSteepDownAreas in paper)
#     miblist = [] # list of steep down areas' mibs
#     clusters = [] # set of clusters
#     
#     while index < N-1:
#         o = order_list[index]
#         mib_g = np.max([mib_g , o.r_dist]) 
#         
#         if index in SDAset[:,0]: # start of a steep down area at index
#             # find the SDA in SDAset
#             SDA = SDAset[SDAset[:,0]== index]
#             
#             # filter all steep down areas whose start*(1-xi) < mib_g
#             for i,iSDA in enumerate(SDAset): 
#                 if iSDA[0]*(1-xi) < mib_g:
#                     SDAset = np.delete(SDAset,i,axis = 0)
#             
#             # Set local mib = 0
#             miblist.append(0)
#             # Add SDA to SDAlist
#             SDAlist.append(SDA)
#             # update index and mib_g
#             index = SDA[0][1] + 1
#             mib_g = order_list[index].r_dist
#             
#         elif index in SUAset[:,0]: # start of a steep up area at index
#             # find the SUA in SUAset
#             SUA = SUAset[SUAset[:,0]== index]
#             
#             # filter all steep down areas whose start*(1-xi) < mib_g
#             for i,iSDA in enumerate(SDAset): 
#                 if iSDA[0]*(1-xi) < mib_g:
#                     SDAset = np.delete(SDAset,i,axis = 0)
#             
#             # update index and mib_g
#             index = SUA[0][1] + 1
#             mib_g = order_list[index].r_dist
#             
#             for i,SDA in enumerate(SDAlist):
#                 # check combiniation of U and D is valid
#                 # find SDA's corresponing mib: just use enumerate
#                 
#                 # i = SDAlist.index(SDA)
#                 # for i,iSDA in SDAlist:
#                 #     if iSDA == SDA: break
#                 mib = miblist[i]
#                 
#                 # compare: end of SUA*(1-xi) >= mib
#                 if SUA[0][1]*(1-xi) >= mib:
#                     # check cluster conditions 1,2,3a
#                     s_D = order_list[SDA[0][0]] # s_D
#                     e_U = order_list[SUA[0][1]] # e_U
#                     e_U1 = order_list[SUA[0][1]+1] # e_U+1
#                     
#                     if s_D.r_dist*(1-xi) >= e_U1.r_dist: # cluster condition 4b
#                         # ps = order_list[np.arange(SDA[0][0],SDA[0][1]+1)] # all points in SDA
#                         ps = order_list[SDA[0][0]:SDA[0][1]+1] # all points in SDA
#                         rs = np.array([p.r_dist for p in ps]) # reachability-distances of points in SDA
#                         # rs = rs[rs > e_U1.r_dist] 
#                         s = ps[np.argmax(rs)] # point in SDA with max reachability-distance
#                         e = e_U
#                     elif e_U1.r_dist*(1-xi) >= s_D.r_dist: # cluster condition 4c
#                         # ps = order_list[np.arange(SUA[0][0],SUA[0][1]+1)] # all points in SUA
#                         ps = order_list[SUA[0][0]:SUA[0][1]+1] # all points in SUA
#                         rs = np.array([p.r_dist for p in ps]) # reachability-distances of points in SUA
#                         s = s_D
#                         e = ps[np.argmin(rs)] # point in SUA with min reachability-distance
#                     else: # cluster condition 4a
#                         s = s_D
#                         e = e_U
#                     
#                     # clusters.append([s,e])
#                     clusters.append([order_list.index(s),order_list.index(e)]) # store index wrt order_list
#         else:
#             index += 1        
#         
#     return(clusters)

def auto_cluster(order_list):
    '''
    Automatically cluster data points using steep point extract cluster algorithm
    inputs:
        order_list: list of DataPoints(class) with OPTICS' ordering
    outputs:
        #order_list: returns the order_list with cluster ID/label for the DataPoints(class)
        clusters: a list of cluster areas [start,end] indices wrt to order_list
    '''
    # initialize parameter xi
    # xi = self.xi
    
    # find the steep upward/downward areas
    SUAset,SDAset = max_steep_area(order_list,MinPts)
    SUAset = np.array(SUAset) # row: steep upward area, col = start/end indices
    SDAset = np.array(SDAset) # row: steep downward area, col = start/end indices
    
    
    # initialize
    index = 1
    mib_g = 0 # global max in between
    N = len(order_list)
    SDAlist = [] # list of the wanted steep down areas(SetOfSteepDownAreas in paper)
    miblist = [] # list of steep down areas' mibs
    clusters = [] # set of clusters
    # lastSA = None # last found steep upward or downward area 
    
    while index < N-1:
        o = order_list[index]
        # max between end of last steep upward or downward area and current index
        mib_g = np.max([mib_g , o.r_dist]) 
        

        if index in SDAset[:,0]: # start of a steep down area at index
            # find the SDA in SDAset
            SDA = SDAset[SDAset[:,0]== index]
            
            # update mib values: max between end of steep down region and current index
            for i,iSDA in enumerate(SDAlist):
                eoSDA = iSDA[0][1] # end of steep down area index
                ps = order_list[eoSDA:index] # all points between end of steep down area and current index
                rs = [p.r_dist for p in ps] # reachability-distances
                miblist[i] = np.max(rs)
            
  
            
            # Set local mib = 0
            miblist.append(0)
            # Add SDA to SDAlist
            SDAlist.append(SDA)
            # update index and mib_g
            index = SDA[0][1] + 1
            mib_g = order_list[index].r_dist # end of last steep upward or downward area 
          
          

        elif index in SUAset[:,0]: # start of a steep up area at index
            # find the SUA in SUAset
            SUA = SUAset[SUAset[:,0]== index]
            
            # update mib values: max between end of steep down region and current index
            for i,iSDA in enumerate(SDAlist):
                eoSDA = iSDA[0][1] # end of steep down area index
                ps = order_list[eoSDA:index] # all points between end of steep down area and current index
                rs = [p.r_dist for p in ps] # reachability-distances
                miblist[i] = np.max(rs)
            
   
            # update index and mib_g
            index = SUA[0][1] + 1
            mib_g = order_list[index].r_dist # end of last steep upward or downward area 
            
            for i,SDA in enumerate(SDAlist):
                # check combiniation of U and D is valid
                # find SDA's corresponing mib: just use enumerate
                
                # i = SDAlist.index(SDA)
                # for i,iSDA in SDAlist:
                #     if iSDA == SDA: break
                mib = miblist[i]
                
                # compare: "reachability-distance" of end of SUA*(1-xi) >= mib
                eoSUA = order_list[SUA[0][1]].r_dist
                if eoSUA*(1-xi) >= mib:
                    
                    # cluster condition 4:
                    s_D = order_list[SDA[0][0]] # s_D
                    e_U = order_list[SUA[0][1]] # e_U
                    e_U1 = order_list[SUA[0][1]+1] # e_U+1
                    
                    if s_D.r_dist*(1-xi) >= e_U1.r_dist: # cluster condition 4b
                        # ps = order_list[np.arange(SDA[0][0],SDA[0][1]+1)] # all points in SDA
                        ps = order_list[SDA[0][0]:SDA[0][1]+1] # all points in SDA
                        rs = np.array([p.r_dist for p in ps]) # reachability-distances of points in SDA
                        # rs = rs[rs > e_U1.r_dist] 
                        s = ps[np.argmax(rs)] # point in SDA with max reachability-distance
                        e = e_U
                    elif e_U1.r_dist*(1-xi) >= s_D.r_dist: # cluster condition 4c
                        # ps = order_list[np.arange(SUA[0][0],SUA[0][1]+1)] # all points in SUA
                        ps = order_list[SUA[0][0]:SUA[0][1]+1] # all points in SUA
                        rs = np.array([p.r_dist for p in ps]) # reachability-distances of points in SUA
                        s = s_D
                        e = ps[np.argmin(rs)] # point in SUA with min reachability-distance
                    else: # cluster condition 4a
                        s = s_D
                        e = e_U
                    
                    # check cluster conditions 1,2,3a:
                    # condition 1: s in SDA
                    s_order_index = order_list.index(s)
                    cond1 = SDA[0][0] <= s_order_index <= SDA[0][1]
                    
                    # condition 2: e in SUA
                    e_order_index = order_list.index(e)
                    cond2 = SUA[0][0] <= e_order_index <= SUA[0][1]
                    
                    # condition 3a: e-s > MinPts
                    cond3a = e_order_index - s_order_index > MinPts
                    
                    # condition 3b is taken care by mib set up
                    
                    if (cond1 and cond2 and cond3a):
                        # clusters.append([s,e])
                        # store index wrt order_list
                        clusters.append([order_list.index(s),order_list.index(e)])
                    
  
                
        else:
            index += 1 



def is_steep_point(order_list,p,xi):
    '''
    inputs:
        order_list: list of DataPoints(class) with OPTICS' ordering
        p: the datapoint
        parameter for xi-steep points, 0 < xi < 1
    outputs:
        verdict: 'U' if is an upward steep point, 'D' if is a downward steep point
                    'X' if is not a steep point
    ------------------------------------------------------------------------------
    Note: last point in order_list isn't defined upward or downward
    '''
    # initialize parameter xi
    # xi = self.xi
    
    N = len(order_list)
    if p.index == order_list[-1].index:
        print('Last data point\'s steepness is undefined')
        return('X')
    
    order_indices = [o.index for o in order_list]
    # find p's index in order_list
    index = order_indices.index(p.index)
    # find next data point in order_list   # next_index = index + 1
    o = order_list[index + 1]
    
    verdict = 'X'
    if (not p.r_dist is None):
        if p.r_dist <= o.r_dist * (1-xi):
            verdict = 'U'
        elif o.r_dist <= p.r_dist * (1-xi):
            verdict = 'D'
        # else:
        #     verdict = 'X'
    
    return(verdict)


def is_steep_area(order_list,s,e,MinPts):
    '''
    Checks the first 3 conditions:
    1. s and e are steep upward/downward points
    2. reachability-distances are monotonically increasing/decreasing
    3. doesn't contain more than MinPts of consecutive non-steep points
    -----------------------------------------------------------------------
    inputs:
        order_list: list of DataPoints(class) with OPTICS' ordering
        s: starting data point in area
        e: ending data point in area
    outputs:
        verdict: 'UA' if is an upward steep area, 'DA' if is a downward steep area
                    'XA' if is not a steep point
    '''
    # initialize paramters
    # MinPts = self.MinPts
    
    # find start, end indices in order_list
    order_indices = [o.index for o in order_list]
    start_index = order_indices.index(s.index)
    end_index = order_indices.index(e.index)
    
    # check upward area
    cond1 =  is_steep_point(order_list,s) == 'U' and is_steep_point(order_list,e) == 'U'
    cond2 = True
    count = 0 # counter for condition 3: number of consecutive points that are not steep upward
    for i in range(start_index,end_index):
        cond2 = cond2 and (order_list[i].r_dist <= order_list[i+1].r_dist)
        if is_steep_point(order_list,order_list[i]) != 'U': count += 1
    cond3 = ( count < MinPts )
    
    # count = 0 # counter for condition 3: number of consecutive points that are not steep upward
    # for i in range(start_index,end_index):
    #     if is_steep_point(order_list,order_list[i]) != 'U': count += 1
    # cond3 = ( count < MinPts )
    
    upward = cond1 and cond2 and cond3
            
    # check downward area
    cond1 =  is_steep_point(order_list,s) == 'D' and is_steep_point(order_list,e) == 'D'
    cond2 = True
    count = 0 # counter for condition 3: number of consecutive points that are not steep downward
    for i in range(start_index,end_index):
        cond2 = cond2 and (order_list[i].r_dist >= order_list[i+1].r_dist)
        if is_steep_point(order_list,order_list[i]) != 'D': count += 1
    cond3 = ( count < MinPts )
    
    downward = cond1 and cond2 and cond3
    
    # assign verdict
    if upward:
        verdict = 'UA'
    elif downward:
        verdict = 'DA'
    else:
        verdict = 'XA'
    
    return(verdict)
    

def max_steep_area(order_list,MinPts):
    '''
    Checks the 4th condition: steep area is maximal
    -----------------------------------------------------------------------
    inputs:
        order_list: list of DataPoints(class) with OPTICS' ordering
        # s: starting data point in area
        # e: ending data point in area
    outputs:
        [USA,DSA]:
        - USA: list of upward steep areas
        - DSA: list of downward steep areas
            areas are defined by [starting index, ending index], indices wrt to order_list, not coords
    '''
    # initialize paramters
    # MinPts = self.MinPts
    
    # # find start, end indices in order_list
    # order_indices = [o.index for o in order_list]
    # start_index = order_indices.index(s.index)
    # end_index = order_indices.index(e.index)
    
    # Get list of steep points
    steep_points = [is_steep_point(order_list,order_list[i]) for i in range(len(order_list)-1)]
    steep_points = np.array(steep_points)
    upward_index = np.arange(steep_points.shape[0])[steep_points == 'U']
    downward_index = np.arange(steep_points.shape[0])[steep_points == 'D']
    

    # find all upward areas
    USA = []
    for i,ui in enumerate(upward_index):
        for j,uj in enumerate(upward_index[i:]):
            # USA.append([ui,uj])
            if (is_steep_area(order_list,order_list[ui],order_list[uj],MinPts) == 'UA'): USA.append([ui,uj])
    # include only max areas
    i = 0
    while i < len(USA):
        flag = False
        ui = USA[i]
        for j,uj in enumerate(USA):
            if ((uj[0] < ui[0] and uj[1] >= ui[1]) or (uj[0] <= ui[0] and uj[1] > ui[1])):
                USA.pop(i)
                flag = True
                break
        if not flag: i += 1
    
    # find all downward areas
    DSA = []
    for i,ui in enumerate(downward_index):
        for j,uj in enumerate(downward_index[i:]):
            if (is_steep_area(order_list,order_list[ui],order_list[uj],MinPts) == 'DA'): DSA.append([ui,uj])
    # include only max areas
    i = 0
    while i < len(DSA):
        flag = False
        ui = DSA[i]
        for j,uj in enumerate(DSA):
            if ((uj[0] < ui[0] and uj[1] >= ui[1]) or (uj[0] <= ui[0] and uj[1] > ui[1])):
                DSA.pop(i)
                flag = True
                break
        if not flag: i += 1
    
    return(USA,DSA)






