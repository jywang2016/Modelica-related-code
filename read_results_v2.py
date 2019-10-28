'''
Compare detection rate results

# On error: No module named 'openpyxl', install package
# pip install openpyxl
# openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.
'''

## General imports
import numpy as np
import pandas as pd
import os,inspect

# Get this current script file's directory:
# loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


## Functions

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

fileLoc = r'N:\HVAC_ModelicaModel_Data\python_figs\rank_Boston+SmallOffice_Workday'

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
table = np.array(table)

# np.savetxt(fileLoc+'\\results.csv',table[0],delimiter=',',fmt='%0.4f')










