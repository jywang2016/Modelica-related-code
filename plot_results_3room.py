'''
Run data analysis on exported contamination results
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


## Function

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
## Load data

file = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room_Boston+SmallOffice\all_contamination_classified.csv'
data_row = 4
data_col = 2

df = parse_pivot_from_file(file,data_row,data_col, mode = 0)

# rows
algorithms = df.index.levels[0] # 'IsolationForest', 'LOF'
contam_level = df.index.levels[1] # '0.001', ... etc

# columns
experiments = df.columns.levels[0] # 130_HVACv4a_Boston+SmallOffice_Workday... etc
dist_measures = df.columns.levels[1] # 'Euclidean', 'High-low'
rates = df.columns.levels[2] # 'Fault detection rate', 'Normal operation rate'

## TPR, FPRs
# set anomaly algorithm, experiment(fault type), and distance measure
norm_exp_index = 0
TPR = df.loc[algorithms[1]][experiments[norm_exp_index]][dist_measures[0]][rates[1]]
FPR = df.loc[algorithms[1]][experiments[3]][dist_measures[0]][rates[1]]
contams = list(TPR.index)

TPR = list(TPR)
FPR = list(FPR)

TPR.insert(0,0)
TPR.append(100)
FPR.insert(0,0)
FPR.append(100)
contams.insert(0,0)
contams.append(100)

coords = np.array([FPR,TPR,contams],dtype=float).T
# coords.sort(axis=0)

# sort with numpy using structured array
dtype = [('FPR',float),('TPR',float),('contamination',float)]
coords_struct = np.empty(len(TPR),dtype)
coords_struct['TPR'] = TPR
coords_struct['FPR'] = FPR
coords_struct['contamination'] = contams
coords_struct.sort(order='FPR')

# sort with pandas
coords_df = pd.DataFrame(coords,columns = ['FPR','TPR','contaminations'])
coords_sorted = coords_df.sort_values(by=['FPR'])

# plot
plt.figure()
plt.scatter(FPR,TPR)
# plt.plot(coords[:,0],coords[:,1])
plt.plot(coords_struct['FPR'],coords_struct['TPR'])
plt.plot([0,100],[0,100],color = 'gray',linestyle=':')
# add contamination label
pre_x, pre_y = np.nan,np.nan # x,y coordinates of previous step
for i in range(1,len(TPR)-1):
    # plt.text(coords[i,0],coords[i,1],coords_sorted['contaminations'][i])
    
    # plot label text only if coords changed to avoid text overlays
    if not (pre_x == coords_struct['FPR'][i] and pre_y == coords_struct['TPR'][i]):
        plt.text(coords_struct['FPR'][i],coords_struct['TPR'][i],coords_sorted['contaminations'][i])
        pre_x = coords_struct['FPR'][i]
        pre_y = coords_struct['TPR'][i]

plt.xlabel('FPR(%)')
plt.ylabel('TPR(%)')
plt.xlim(-5,105)
plt.ylim(-5,105)
plt.show()

##

# exp_list = experiments[[3,4,5,6,8,9]]
exp_list = experiments
# rename the experiments for plots only
exp_names = ['Normal',
             'Fault 1',
             'Fault 2',
             'Fault 3',
             'Fault 4',
             'Fault 5',
            ]
            
# plot subplots
for e,experiment in enumerate(exp_list):
    # plt.figure()
    fig,axes = plt.subplots(2,2,sharex='all', sharey='all')
    for d,d_measure in enumerate(dist_measures):
        for a,aa in enumerate(algorithms):
            TPR = df.loc[algorithms[a]][experiments[norm_exp_index]][dist_measures[d]][rates[1]]
            FPR = df.loc[algorithms[a]][experiment][dist_measures[d]][rates[1]]
            contams = list(TPR.index)
            
            TPR = list(TPR)
            FPR = list(FPR)
            # add starting and ending BCs
            TPR.insert(0,0)
            TPR.append(100)
            FPR.insert(0,0)
            FPR.append(100)
            contams.insert(0,0)
            contams.append(100)
            
            # coordinate array
            coords = np.array([FPR,TPR,contams],dtype=float).T
            
            # sort with numpy using structured array
            dtype = [('FPR',float),('TPR',float),('contamination',float)]
            coords_struct = np.empty(len(TPR),dtype)
            coords_struct['TPR'] = TPR
            coords_struct['FPR'] = FPR
            coords_struct['contamination'] = contams
            coords_struct.sort(order='FPR')
            
            # plot
            ax = axes[a,d]
            ax.scatter(coords_struct['FPR'],coords_struct['TPR'])
            ax.plot(coords_struct['FPR'],coords_struct['TPR'])
            # ax.plot(coords[:,0],coords[:,1])
            ax.plot([0,100],[0,100],color = 'gray',linestyle=':')
            # # add contamination label
            # for i in range(1,len(TPR)-1):
            #     ax.text(coords[i,0],coords[i,1],coords_sorted['contaminations'][i])
            ax.set_xlim(-5,105)
            ax.set_ylim(-5,105)
            ax.set_xlabel('FPR(%)')
            ax.set_ylabel('TPR(%)')
            ax.set_title('{} with {} distance'.format(aa,d_measure))
    # fig.set_tight_layout('tight')
    fig.suptitle('{}'.format(exp_names[e]))
    plt.show()


# plot overlay plots
for e,experiment in enumerate(exp_list):
    plt.figure()
    # fig,axes = plt.subplots(2,2,sharex='all', sharey='all')
    for d,d_measure in enumerate(dist_measures):
        for a,aa in enumerate(algorithms):
            TPR = df.loc[algorithms[a]][experiments[norm_exp_index]][dist_measures[d]][rates[1]]
            FPR = df.loc[algorithms[a]][experiment][dist_measures[d]][rates[1]]
            contams = list(TPR.index)
            
            TPR = list(TPR)
            FPR = list(FPR)
            # add starting and ending BCs
            TPR.insert(0,0)
            TPR.append(100)
            FPR.insert(0,0)
            FPR.append(100)
            contams.insert(0,0)
            contams.append(100)
            
            # coordinate array
            coords = np.array([FPR,TPR,contams],dtype=float).T
            
            # sort with numpy using structured array
            dtype = [('FPR',float),('TPR',float),('contamination',float)]
            coords_struct = np.empty(len(TPR),dtype)
            coords_struct['TPR'] = TPR
            coords_struct['FPR'] = FPR
            coords_struct['contamination'] = contams
            coords_struct.sort(order='FPR')
            
            # plot
            
            plt.scatter(coords_struct['FPR'],coords_struct['TPR'],
                        label='{} with {} distance'.format(aa,d_measure))
            plt.plot(coords_struct['FPR'],coords_struct['TPR'])
            
            plt.plot([0,100],[0,100],color = 'gray',linestyle=':')
            # # add contamination label
            # for i in range(1,len(TPR)-1):
            #     ax.text(coords[i,0],coords[i,1],coords_sorted['contaminations'][i])
            
            # ax.set_title('{} with {} distance'.format(aa,d_measure))
    plt.xlim(-5,105)
    plt.ylim(-5,105)
    plt.xlabel('FPR(%)')
    plt.ylabel('TPR(%)')
    plt.title('{}'.format(exp_names[e]))
    plt.legend()
    plt.show()



# plot subplots of overlay plots 
fig,axes = plt.subplots(3,2,sharex='all', sharey='all')
for e,experiment in enumerate(exp_list):
    for d,d_measure in enumerate(dist_measures):
        for a,aa in enumerate(algorithms):
            TPR = df.loc[algorithms[a]][experiments[norm_exp_index]][dist_measures[d]][rates[1]]
            FPR = df.loc[algorithms[a]][experiment][dist_measures[d]][rates[1]]
            contams = list(TPR.index)
            
            TPR = list(TPR)
            FPR = list(FPR)
            # add starting and ending BCs
            TPR.insert(0,0)
            TPR.append(100)
            FPR.insert(0,0)
            FPR.append(100)
            contams.insert(0,0)
            contams.append(100)
            
            # coordinate array
            coords = np.array([FPR,TPR,contams],dtype=float).T
            
            # sort with numpy using structured array
            dtype = [('FPR',float),('TPR',float),('contamination',float)]
            coords_struct = np.empty(len(TPR),dtype)
            coords_struct['TPR'] = TPR
            coords_struct['FPR'] = FPR
            coords_struct['contamination'] = contams
            coords_struct.sort(order='FPR')
            
            # plot
            ax = axes.reshape(6,)[e]
            ax.scatter(coords_struct['FPR'],coords_struct['TPR'],
                       label='{} with {} distance'.format(aa,d_measure))
            ax.plot(coords_struct['FPR'],coords_struct['TPR'])
            # ax.plot(coords[:,0],coords[:,1])
            ax.plot([0,100],[0,100],color = 'gray',linestyle=':')
            # # add contamination label
            # for i in range(1,len(TPR)-1):
            #     ax.text(coords[i,0],coords[i,1],coords_sorted['contaminations'][i])
            
    # fig.set_tight_layout('tight')
    ax.set_xlim(-5,105)
    ax.set_ylim(-5,105)
    if e in [4,5]: ax.set_xlabel('FPR(%)')
    ax.set_ylabel('TPR(%)')
    ax.set_title('{}'.format(exp_names[e]))
    if e==1: ax.legend()
# plt.legend(loc = 'best') # bbox (x, y, width, height)
# fig.suptitle('AUROC')
plt.show()












