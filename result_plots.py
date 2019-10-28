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

# file = r'N:\HVAC_ModelicaModel_Data\python_figs\HVACv4a+PAA_results\All_results_pivot.csv'
# df = parse_pivot_from_file(file,data_row=3,data_col=1, mode = 0)

file = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room\All_results_contam001.csv'
df = parse_pivot_from_file(file,data_row=3,data_col=1, mode = 0)


## Separate IsolationForest and LOF Experiment labels

# new_df = df.reset_index(level=0,drop=True)
new_df = df

# indices
aa = [] # anomaly algorithms
ex = [] # experiments
for index in new_df.index:
    ss = index[0].split('_')
    aa.append(ss[-1])
    ex.append(index[0][:-len(ss[-1])-1])
aa = pd.Series(aa,name='Anomaly algorithm')
ex = pd.Series(ex,name='Experiment')

new_df.index = pd.MultiIndex.from_arrays([aa,ex],names = [aa.name,ex.name])
new_df = new_df.sort_index()
new_df.to_csv(r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room\new_df.csv')

'''
Manually delete unwanted experiments
'''


## Reload data

# file = r'N:\HVAC_ModelicaModel_Data\python_figs\HVACv4a+PAA_results\new_df.csv'
file = r'L:\HVAC_ModelicaModel_Data\python_figs\HVACv6a_3room\new_df.csv'
df = parse_pivot_from_file(file,data_row=3,data_col=2, mode = 0)

# 


# separate anomaly detection methods:
df_lof = df.loc['LOF']
df_if = df.loc['IsolationForest']
# normal operation rates:
df_lof_norm = df_lof.iloc[0::7]
df_if_norm = df_if.iloc[0::7]
df_lof_norm.columns = df_lof_norm.columns.swaplevel(0,1)
df_if_norm.columns = df_if_norm.columns.swaplevel(0,1)
df_lof_norm = df_lof_norm['Normal operation rate']
df_if_norm = df_if_norm['Normal operation rate']
# faults:
df_lof_fault = df_lof.loc[df_lof.index.drop(df_lof_norm.index)]
df_lof_fault.columns = df_lof_fault.columns.swaplevel(0,1)
df_lof_fault = df_lof_fault['Fault detection rate']
df_if_fault = df_if.loc[df_if.index.drop(df_if_norm.index)]
df_if_fault.columns = df_if_fault.columns.swaplevel(0,1)
df_if_fault = df_if_fault['Fault detection rate']
# (normal + fault)'s Fault detection rate:
df_lof_NF = df_lof
df_lof_NF.columns = df_lof_NF.columns.swaplevel(0,1)
df_lof_NF = df_lof_NF['Fault detection rate']
df_if_NF = df_if
df_if_NF.columns = df_if_NF.columns.swaplevel(0,1)
df_if_NF = df_if_NF['Fault detection rate']



# Plots:
# Style sheet
# plt.style.use('default')
# plt.style.use('fivethirtyeight')
# plt.style.use('ggplot')
# plt.style.use('seaborn-colorblind')
# plt.style.use('bmh')
plt.style.use('tableau-colorblind10')


# reset color list for style sheet
default_color_list = []
for obj in matplotlib.rcParams['axes.prop_cycle']:
    default_color_list.append(obj['color'])
# combine the two color lists
my_colors =  default_color_list

# set plot df
df_plot = df_lof_NF 
# df_plot = df_if_NF

# label settings
input_set = 0
input_data_set = ['Boston - Small Office(weekday)',
                  'Boston - Small Office',
                  'SF - Small Office',
                  'SF - Large Office',
                  'Boston - Large Office'
                  ]
fault_list = ['Normal',
              'Fault 1',
              'Fault 2',
              'Fault 3',
              'Fault 4',
              'Fault 5',
              'Fault 6',
              ]
n_faults = len(fault_list)

n_group = len(df_plot.index)
dist_measures = list(df.columns.levels[0])
group_size = len(dist_measures)

set_index = input_set*n_faults

x_in_groups = range(group_size)
x_between_groups = [x*(group_size+1) for x in range(n_group)] # each experiment has a group

# LOF
plt.figure()
# # add in normal operation
# for j,x in enumerate(x_in_groups):
#     plt.bar(x,float(df_lof_norm.iloc[set_index][j]),width = 1,bottom = 0,
#             color=my_colors[j],edgecolor='black',alpha=0.8)

# plot faults
for i,xg in enumerate(x_between_groups[set_index:set_index+n_faults]):
    for j,x in enumerate(x_in_groups):
        plt.bar(x+xg,float(df_plot.iloc[i+set_index][j]),width = 1,bottom = 0,
                color=my_colors[j],edgecolor='white',alpha=0.8)
# set up legends
for c in range(group_size):
    plt.plot([],[],linewidth = 8,label = df.columns.levels[0][c],
             color = my_colors[c],alpha=0.8)

ticks = fault_list
# ticks.insert(0,'Normal')
xpos = [x+1.5 for x in x_between_groups[set_index:set_index+n_faults]]
# xpos.insert(0,1.5)
plt.xticks(xpos,ticks)
plt.ylabel('Fault detection rate[%]')
plt.tight_layout()
plt.title('{}'.format(input_data_set[input_set]))
plt.legend()
plt.show()


##

def plot_FDR(df_plot,input_set):
    input_data_set = ['Boston - Small Office(weekday)',
                    'Boston - Small Office',
                    'SF - Small Office',
                    'SF - Large Office',
                    'Boston - Large Office'
                    ]
    fault_list = ['Normal',
                'Fault 1',
                'Fault 2',
                'Fault 3',
                'Fault 4',
                'Fault 5',
                'Fault 6',
                ]
    n_faults = len(fault_list)
    
    n_group = len(df_plot.index)
    dist_measures = list(df.columns.levels[0])
    group_size = len(dist_measures)
    
    set_index = input_set*n_faults
    
    x_in_groups = range(group_size)
    x_between_groups = [x*(group_size+1) for x in range(n_group)] # each experiment has a group
    
    # LOF
    plt.figure()
    # # add in normal operation
    # for j,x in enumerate(x_in_groups):
    #     plt.bar(x,float(df_lof_norm.iloc[set_index][j]),width = 1,bottom = 0,
    #             color=my_colors[j],edgecolor='black',alpha=0.8)
    
    # plot faults
    for i,xg in enumerate(x_between_groups[set_index:set_index+n_faults]):
        for j,x in enumerate(x_in_groups):
            plt.bar(x+xg,float(df_plot.iloc[i+set_index][j]),width = 1,bottom = 0,
                    color=my_colors[j],edgecolor='white',alpha=0.8)
    # set up legends
    for c in range(group_size):
        plt.plot([],[],linewidth = 8,label = df.columns.levels[0][c],
                color = my_colors[c],alpha=0.8)
    
    ticks = fault_list
    # ticks.insert(0,'Normal')
    xpos = [x+1.5 for x in x_between_groups[set_index:set_index+n_faults]]
    # xpos.insert(0,1.5)
    plt.xticks(xpos,ticks)
    plt.ylabel('Fault detection rate[%]')
    plt.tight_layout()
    plt.title('{}'.format(input_data_set[input_set]))
    plt.legend()
    plt.show()


for i in range(5):
    plot_FDR(df_lof_NF,input_set = i)
    # plot_FDR(df_if_NF,input_set = i)




# # IsolationForest
# plt.figure()
# 
# # plot faults
# for i,xg in enumerate(x_between_groups[set_index:set_index+set_size]):
#     for j,x in enumerate(x_in_groups):
#         plt.bar(x+xg,float(df_if_NF.iloc[i][j]),width = 1,bottom = 0,
#                 color=my_colors[j],edgecolor='white',alpha=0.8)
# # set up legends
# for c in range(group_size):
#     plt.plot([],[],linewidth = 8,label = df.columns.levels[0][c],
#              color = my_colors[c],alpha=0.8)
# 
# ticks = fault_list
# # ticks.insert(0,'Normal')
# xpos = [x+1.5 for x in x_between_groups[:set_size]]
# # xpos.insert(0,1.5)
# plt.xticks(xpos,ticks)
# plt.ylabel('Fault detection rate[%]')
# plt.tight_layout()
# plt.legend()
# plt.show()


## 

def plot_FDR_3room(df_plot,input_set):
    input_data_set = ['Boston - Small Office',
                      'Boston - Large Office',
                      'SF - Small Office',
                      'SF - Large Office'
                    ]
    fault_list = ['Normal',
                  'Fault 1',
                  'Fault 2',
                  'Fault 3',
                  'Fault 4',
                  'Fault 5',
                  ]
    n_faults = len(fault_list)
    
    n_group = len(df_plot.index)
    dist_measures = list(df.columns.levels[0])
    group_size = len(dist_measures)
    
    set_index = input_set*n_faults
    
    x_in_groups = range(group_size)
    x_between_groups = [x*(group_size+1) for x in range(n_group)] # each experiment has a group
    
    # LOF
    plt.figure()
    # # add in normal operation
    # for j,x in enumerate(x_in_groups):
    #     plt.bar(x,float(df_lof_norm.iloc[set_index][j]),width = 1,bottom = 0,
    #             color=my_colors[j],edgecolor='black',alpha=0.8)
    
    # plot faults
    for i,xg in enumerate(x_between_groups[set_index:set_index+n_faults]):
        for j,x in enumerate(x_in_groups):
            plt.bar(x+xg,float(df_plot.iloc[i+set_index][j]),width = 1,bottom = 0,
                    color=my_colors[j],edgecolor='white',alpha=0.8)
    # set up legends
    for c in range(group_size):
        plt.plot([],[],linewidth = 8,label = df.columns.levels[0][c],
                color = my_colors[c],alpha=0.8)
    
    ticks = fault_list
    # ticks.insert(0,'Normal')
    xpos = [x+1.5 for x in x_between_groups[set_index:set_index+n_faults]]
    # xpos.insert(0,1.5)
    plt.xticks(xpos,ticks)
    plt.ylabel('Fault detection rate[%]')
    plt.tight_layout()
    # plt.title('{}'.format(input_data_set[input_set]))
    plt.legend()
    plt.show()


for i in range(4):
    # plot_FDR_3room(df_lof_NF,input_set = i)
    plot_FDR_3room(df_if_NF,input_set = i)
























