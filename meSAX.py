'''
My iSAX implementation

Existing packages that has SAX:
saxpy, pysax, tslearn

But no iSAX python implementation as of today 2018-07
'''

## General imports
import numpy as np

## Class

class iSAX:
    def __init__(self,ts,n_segments,init_cardinality=8):
        self.raw_ts = ts
        self.n_seg = n_segments # homogeneous segments
        self.card = init_cardinality
        
        
    # Calculates raw_ts's Piece-wise Aggregation Approximation
    # if original_length=True, gives out the same length of the input TS
    def PAA(self,original_length=False):
        n_seg = self.n_seg # number of segments
        ts = np.array(self.raw_ts)
        if original_length:
            paa = np.empty((len(ts),),dtype=float)
        else:
            paa = np.empty((n_seg,),dtype=float)
        
        seg_size = len(ts)/n_seg # segment size
        if not seg_size.is_integer(): # pad number if segment size is not conformable
            seg_size = int(np.ceil(seg_size))
            ts = np.pad(ts,pad_width = seg_size*n_seg-len(ts),mode='constant',constant_values = ts[-1])
            print('Segment size not conformable to sequence, last segment will be padded.')
        seg_size = int(seg_size)
        
        
        for i in range(n_seg):
            if original_length:
                paa[i*seg_size:(i+1)*seg_size] = np.mean(ts[i*seg_size:(i+1)*seg_size])
            else:
                paa[i] = np.mean(ts[i*seg_size:(i+1)*seg_size])
        
        return(paa)
            
    # Calculates normal SAX with fixed cardinality
    def SAX(self,range_min,range_max,original_length=False):
        # n_seg = self.n_seg # number of segments
        # ts = np.array(self.raw_ts)
        # if original_length:
        #     sax = np.empty((len(ts),),dtype=float)
        # else:
        #     sax = np.empty((n_seg,),dtype=float)
        # 
        # seg_size = len(ts)/n_seg # segment size
        # if not seg_size.is_integer(): # pad number if segment size is not conformable
        #     seg_size = int(np.ceil(seg_size))
        #     ts = np.pad(ts,pad_width = seg_size*n_seg-len(ts),mode='constant',constant_values = ts[-1])
        #     print('Segment size not conformable to sequence, last segment will be padded.')
        # seg_size = int(seg_size)
        ts = self.PAA(original_length)
        ts_min = range_min # np.min(ts)
        ts_max = range_max # np.max(ts)
        
        card = self.card # cardinality
        n_splits = card - 1 #2**card-1 # number of splitters
        split_unit = (ts_max - ts_min)/(n_splits+1)
        splits = [split_unit*(i+1)+ts_min for i in range(n_splits)]
        splits.append(ts_max)
        splits = np.array(splits)
    
        
        sax = np.empty(ts.shape,dtype=np.int)
        for i,x in enumerate(ts):
            if x > ts_max: # greater than max
                sax[i] = n_splits
                print('{} exceeded given max {}'.format(x,ts_max))
                continue
            elif x < ts_min: # less than min
                sax[i] = 0
                print('{} exceeded given min {}'.format(x,ts_min))
                continue
                
            for j,s in enumerate(splits):
                if x <= s:
                    sax[i] = j
                    break
                
        
        return(sax)


## Functions

def PAA(ts,n_seg,original_length=False,print_ = True):
    ts = np.array(ts)
    if original_length:
        paa = np.empty((len(ts),),dtype=float)
    else:
        paa = np.empty((n_seg,),dtype=float)
    
    seg_size = len(ts)/n_seg # segment size
    if not seg_size.is_integer(): # pad number if segment size is not conformable
        seg_size = int(np.ceil(seg_size))
        ts = np.pad(ts,pad_width = seg_size*n_seg-len(ts),mode='constant',constant_values = ts[-1])
        if print_: print('Segment size not conformable to sequence, last segment will be padded.')
    seg_size = int(seg_size)
    
    
    for i in range(n_seg):
        if original_length:
            paa[i*seg_size:(i+1)*seg_size] = np.mean(ts[i*seg_size:(i+1)*seg_size])
        else:
            paa[i] = np.mean(ts[i*seg_size:(i+1)*seg_size])
    
    return(paa)
        
# Calculates normal SAX with fixed cardinality
def SAX(ts,n_seg,cardinality,range_min,range_max,original_length=False,print_ = True):
    ts = PAA(ts,n_seg,original_length)
    ts_min = range_min # np.min(ts)
    ts_max = range_max # np.max(ts)
    
    n_splits = cardinality-1 # 2**cardinality-1 # number of splitters
    split_unit = (ts_max - ts_min)/(n_splits+1)
    splits = [split_unit*(i+1)+ts_min for i in range(n_splits)]
    splits.append(ts_max)
    splits = np.array(splits)
    
    sax = np.empty(ts.shape,dtype=np.int)
    for i,x in enumerate(ts):
        if x > ts_max: # greater than max
            sax[i] = n_splits
            if print_: print('{} exceeded given max {}'.format(x,ts_max))
            continue
        elif x < ts_min: # less than min
            sax[i] = 0
            if print_: print('{} exceeded given min {}'.format(x,ts_min))
            continue
            
        for j,s in enumerate(splits):
            if x <= s:
                sax[i] = j
                break
    
    return(sax)

# Returns the splits
def SAX_split_intervals(ts,n_seg,cardinality,range_min,range_max,original_length=False,withMinMax = False):
    ts = PAA(ts,n_seg,original_length)
    ts_min = range_min # np.min(ts)
    ts_max = range_max # np.max(ts)
    
    # card = self.card # cardinality
    n_splits = cardinality-1 # 2**cardinality-1 # number of splitters
    split_unit = (ts_max - ts_min)/(n_splits+1)
    splits = [split_unit*(i+1)+ts_min for i in range(n_splits)]
    if withMinMax:
        splits.append(ts_max)
        splits.insert(0,ts_min)
    
    return(splits)

# Returns the area blocks
def SAX_bounds(ts,n_seg,cardinality,range_min,range_max,original_length=False):
    sax = SAX(ts,n_seg,cardinality,range_min,range_max,original_length)
    splits = SAX_split_intervals(ts,n_seg,cardinality,range_min,range_max,original_length,True)
    
    lower = np.empty((len(sax),1))
    upper = np.empty((len(sax),1))
    
    for i in range(len(sax)):
        lower[i] = splits[sax[i]]
        upper[i] = splits[sax[i]+1]
    
     
    return(np.concatenate((lower,upper),axis = 1))
























