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


## Parse and export to csv

# fileLoc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday'

root_loc = r'L:\HVAC_ModelicaModel_Data\Fault_diagnosis_227_HVACv6a_3room_SF+SmallOffice_Fault3_2'

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

## Load data

# file = r'L:\HVAC_ModelicaModel_Data\Fault Diagnosis\Method1_normal_operating_rates.csv'
file = r'L:\HVAC_ModelicaModel_Data\Fault Diagnosis\Method2_normal_rates.csv'
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
new_df.to_csv(r'L:\HVAC_ModelicaModel_Data\Fault Diagnosis\new_df.csv')


## Reload data

file = r'N:\HVAC_ModelicaModel_Data\Fault Diagnosis\new_df2.csv'
df = parse_pivot_from_file(file,data_row=3,data_col=2, mode = 0)

# separate anomaly detection methods:
df_lof = df.loc['LOF']
df_if = df.loc['IsolationForest']


## plot radar/spider/star chart


data = df_lof.values[:,0] # input data, np.array. (N * 1)
var_labels = ['Normal',
              'Fault 1',
              'Fault 2',
              'Fault 3',
              'Fault 4',
              'Fault 5',
              'Fault 6',
              ]

# min_val = 0
max_val = 100

n_angles = len(data) # number of angles
angles = [(2*math.pi/n_angles)*i for i in range(n_angles)] # list of angles

# repeat first data point at end to close the loop:
data = list(data)
data.append(data[0])
angles.append(angles[0])
#
angles = np.array(angles)
radii = np.array(data,dtype=np.float)

# plot
plt.figure()
ax = plt.subplot(111, polar=True)
# ax.scatter(angles,radii)
ax.plot(angles,radii)
ax.fill(angles,radii,alpha = 0.2)
plt.xticks(angles,var_labels,size=7)
plt.yticks(np.linspace(0,max_val,6),color='gray',size=7)

plt.show()




## radar chart functions
def plot_radar(data,var_labels,max_val = 100):
    '''
    Inputs:
        data: input data, np.array. (n_angles,)
        var_labels: labels for each angle
        max_val: max value
    '''
    n_angles = data.shape[0] # number of angles
    angles = [(2*math.pi/n_angles)*i for i in range(n_angles)] # list of angles
    
    # n_overlay = data.shape[1]
    
    # repeat first data point at end to close the loop:
    data = list(data)
    data.append(data[0])
    angles.append(angles[0])
    #
    angles = np.array(angles)
    radii = np.array(data,dtype=np.float)
    
    # plot
    # plt.figure()
    ax = plt.subplot(111, polar=True)
    # ax.scatter(angles,radii)
    ax.plot(angles,radii)
    ax.fill(angles,radii,alpha = 0.2)
    # plt.xticks(angles,var_labels,size=7)
    # plt.yticks(np.linspace(0,max_val,6),color='gray',size=7)
    # plt.show()
    

def plot_radar_chart(data,var_labels,max_val = 100):
    '''
    Uses plot_radar() to plot overlays.
    Must have n_overlays > 1, if n_overlays == 1 then just use  plot_radar()
    ----------
    Inputs:
        data: input data, np.array. (n_angles,n_overlays)
        var_labels: labels for each angle
        max_val: max value
    
    '''
    
    n_overlays = data.shape[1]
    
    plt.figure()
    
    for i in range(n_overlays):
        data_col = data[:,i]
        plot_radar(data_col,var_labels,max_val)
    
    
    plt.xticks(angles,var_labels,size=7)
    plt.yticks(np.linspace(0,max_val,6),color='gray',size=6)
    # plt.show()
    
    
    
## radar chart demos

data = df_lof.values # df_if.values
plot_radar_chart(data,var_labels,max_val = 100)

# add legends
legend_labels = ['Fault 1',
                 'Fault 2',
                 'Fault 3',
                 'Fault 4',
                 'Fault 5',
                 'Fault 6',
                ]
for i,label in enumerate(legend_labels):
    plt.plot([],[],color=my_colors[i],label=label)
plt.legend(bbox_to_anchor=(1.05, 1))


plt.show()


## plot corresponding bar plots


plt.figure()



for i,val in enumerate(data.T):
    plt.bar(xpos,val,bottom=0)


ticks = var_labels
# ticks = legend_labels
xpos = range(data.shape[0])
plt.xticks(xpos,ticks)

# plt.ylim([0,20])
plt.show()

##

# set plot df
df_plot = df_lof
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
    plt.plot([],[],linewidth = 8,label = fault_list[1:][c],
             color = my_colors[c],alpha=0.8)
    # plt.plot([],[],linewidth = 8,label = df.columns.levels[0][c],
    #          color = my_colors[c],alpha=0.8)

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






