## Functions
# Load all functions to JModelica.org first
'''
# Read in selected variables. 
# Input: fileName, Output: list of variable names
'''
def SelectedVars(fileName):
    with open(fileName + '.txt') as f:
        read_data = f.read()
    f.closed
    variables = read_data.split('\n')
    return(variables)

'''
# Export selected variables. 
# Input: res(model.simulation result), variables(list of variable names), fileName
# Saves selected variables' data to csv file
'''
def ExportVars(res,variables,fileName):
    dataArr = np.zeros((len(variables),len(res[variables[0]])+1),dtype = np.object)
    varArr = list()
    
    for i in range(len(variables)):
        varArr.append(variables[i])
        dataArr[i,1:] = res[variables[i]]
    
    dataArr[:,0] = np.array(varArr)
    np.savetxt(fileName + '.csv', dataArr.transpose(),fmt = '%s',delimiter = ',')
    print(fileName + '.csv' + ' has been saved.\n')

'''
This script is used to modify the values of TimeTable component, WeatherData, in HVACv3a_weather.mo
For CombiTimeTable doesn't work in this model for some reason(don't ask me why).
# Changes weatherData in the model
'''
def LoadWeatherData(model,weather_file,day = 123): # day starts from 1 NOT 0
    # load data
    weatherData = np.loadtxt(open(weather_file, "rb"), delimiter=",", skiprows=1,dtype = np.object)
    weatherData[-1,-1] = 0 # last cell is empty(missing data)
    weatherData = np.array(weatherData[:,1:],dtype = float)
    
    print(weather_file + ' loaded, \nnow parsing...')
    
    # day = 123 # weatherData[:,day]
    t = np.arange(0,3600*24,3600) # time 
    mat = np.concatenate((t,weatherData[:,day-1]))
    mat = mat.reshape((24,2),order = 'F')
    '''
    # Note: putting weather data in such format is because we set the WeatherData's(TimeTable component)
    # WeatherData.table with a value of a matrix with a [24,2] dimension.
    # The value we set is a place holder, must comply to its matrix dimension to use this method,
    # for the WeatherData.table vairable is already compiled into a FMU
    '''
    
    # Change the WeatherData parameter after loading the FMU(before model.simulate)
    '''
    # This part is used to check the variable format
    filePath = 'D:'
    fileName = 'modelVars.txt'
    file = filePath + '\\' + fileName
    
    var = model.get_model_variables()
    varArr = np.array(var.keys())
    np.savetxt(file,varArr,fmt='%s')
    '''
    # The matrix variable is saved as individual variables when in FMU(Don't ask me why)
    # Thus, we have to change the matrix values element by elemnt in np.array class type
    # e.g. WeatherData.table[11,2] = np.array[285]
    
    
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            WD = 'WeatherData.table[' + str(i+1) + ',' + str(j+1) + ']'
            WD_val = np.array(mat[i,j])
            model.set(WD,WD_val)
    print('---Weather data set---')
    
'''
Input: weather csv file(from NOAA_Data_export.py
Output: weather data shape
'''
def WeatherDataShape(weather_file):
    weatherData = np.loadtxt(open(weather_file, "rb"), delimiter=",", skiprows=1,dtype = np.object)
    return(weatherData.shape)

'''
Input: weather csv file(from NOAA_Data_export.py, day(integer)
Output: corresponding date of day
'''
def WeatherDataDate(weather_file,day):
    weatherData = np.loadtxt(open(weather_file, "rb"), delimiter=",", dtype = np.object)
    date = weatherData[0,day]
    return(date)


'''
This script is used to modify the values of TimeTable component, RoomLoadData, in HVACv3a_weather_load.mo
For CombiTimeTable doesn't work in this model for some reason(don't ask me why).
# Changes loadData in the model
'''
def LoadHeatLoadData(model,load_file,day = 123): # day starts from 1 NOT 0
    # load data
    loadData = np.loadtxt(open(load_file, "rb"), delimiter=",", skiprows=1,dtype = np.object)
    loadData[-1,-1] = 0 # last cell is empty(missing data)
    loadData = np.array(loadData[:,1:],dtype = float)
    
    print(load_file + ' loaded, \nnow parsing...')
    
    # day = 123 # loadData[:,day]
    t = np.arange(0,3600*24,3600) # time 
    mat = np.concatenate((t,loadData[:,day-1]))
    mat = mat.reshape((24,2),order = 'F')
    '''
    # Note: putting weather data in such format is because we set the RoomLoadData's(TimeTable component)
    # RoomLoadData.table with a value of a matrix with a [24,2] dimension.
    # The value we set is a place holder, must comply to its matrix dimension to use this method,
    # for the RoomLoadData.table vairable is already compiled into a FMU
    '''
    
    # Change the RoomLoadData parameter after loading the FMU(before model.simulate)
    '''
    # This part is used to check the variable format
    filePath = 'D:'
    fileName = 'modelVars.txt'
    file = filePath + '\\' + fileName
    
    var = model.get_model_variables()
    varArr = np.array(var.keys())
    np.savetxt(file,varArr,fmt='%s')
    '''
    # The matrix variable is saved as individual variables when in FMU(Don't ask me why)
    # Thus, we have to change the matrix values element by elemnt in np.array class type
    # e.g. RoomLoadData.table[11,2] = np.array[285]
    
    
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            LD = 'RoomLoadData.table[' + str(i+1) + ',' + str(j+1) + ']'
            LD_val = np.array(mat[i,j])
            model.set(LD,LD_val)
    print('---Heat load data set---')


'''
This script is used to modify the values of TimeTable component, 
    RoomLoadData, RoomLoadData2, and RoomLoadData3, in HVACv6_3room.mo
    length of load_files,days, and RoomLoadData parameters have to be the same
    
For CombiTimeTable doesn't work in this model for some reason(don't ask me why).
# Changes loadData in the model
'''
def LoadMultiHeatLoadData(model,load_files,days = [1,2,3],param_names = ['RoomLoadData','RoomLoadData2','RoomLoadData3'],scale_factor = 0.3): # day starts from 1 NOT 0
    # load data
    loadData_list = []
    for load_file in load_files:
        loadData = np.loadtxt(open(load_file, "rb"), delimiter=",", skiprows=1,dtype = np.object)
        loadData[-1,-1] = 0 # last cell is empty(missing data)
        loadData = np.array(loadData[:,1:],dtype = float) * scale_factor
        loadData_list.append(loadData)
        print(load_file + ' loaded')
    print('All heat load files loaded, now parsing...')
    
    
    t = np.arange(0,3600*24,3600) # time 
    
    for index,loadData in enumerate(loadData_list):
        day = days[index]
        mat = np.concatenate((t,loadData[:,day-1]))
        mat = mat.reshape((24,2),order = 'F')
        '''
        # Note: putting weather data in such format is because we set the RoomLoadData's(TimeTable component)
        # RoomLoadData.table with a value of a matrix with a [24,2] dimension.
        # The value we set is a place holder, must comply to its matrix dimension to use this method,
        # for the RoomLoadData.table vairable is already compiled into a FMU
        '''
        
        # Change the RoomLoadData parameter after loading the FMU(before model.simulate)
        '''
        # This part is used to check the variable format
        filePath = 'D:'
        fileName = 'modelVars.txt'
        file = filePath + '\\' + fileName
        
        var = model.get_model_variables()
        varArr = np.array(var.keys())
        np.savetxt(file,varArr,fmt='%s')
        '''
        # The matrix variable is saved as individual variables when in FMU(Don't ask me why)
        # Thus, we have to change the matrix values element by elemnt in np.array class type
        # e.g. RoomLoadData.table[11,2] = np.array[285]
    
        param_name = param_names[index]
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                # LD = 'RoomLoadData.table[' + str(i+1) + ',' + str(j+1) + ']'
                LD = param_name + '.table[' + str(i+1) + ',' + str(j+1) + ']'
                LD_val = np.array(mat[i,j])
                model.set(LD,LD_val)
        print('Heat load data for {} set'.format(param_name))



'''
Use neighboring days instead of random days for heatload
This function is to make sure the days are all weekdays
Input:
    - wdays: given weather days
    - max_d: if the corresponding wday isn't a weekday, then a random day will be assigned
             to for the heat load day within a distance of max_d
    - weekends: a list of integers, defining the weekends.
Output:
    - hldays: an array of heat load days
'''
def neighbor_days(wdays,max_d,max_days = 360,weekends=[0,1]):
    # # excluding same heatload days
    # d = np.random.randint(1,max_d+1,size = wdays.shape) # difference
    # pm = np.random.randint(2,size = wdays.shape) # plus minus sign
    # pm[pm==0] = -1 # change 0 values to -1
    # hldays = wdays + d*pm
    
    # # including same heatload days
    # hldays = np.random.randint(2*max_d+1,size = wdays.shape) - max_d + wdays
    
    # avoid weekdays # make sure the days are all weekdays
    N = max_days # wdays.shape[0]
    weekdays = [x for x in [x for x in range(N) if (x%7!=weekends[0])] if (x%7!=weekends[1])]
    hldays = np.empty(wdays.shape,dtype=int)
    for i,day in enumerate(wdays):
        hldays[i] = wdays[i] + np.random.randint(2*max_d+1) - max_d
        while not hldays[i] in weekdays: # if not weekdays, resample until it's a weekday
            hldays[i] = wdays[i] + np.random.randint(2*max_d+1) - max_d
    
    # make sure no minus days or days greater than N
    hldays = hldays % N
    return(hldays)


'''
Use neighboring days instead of random days for heatload
This function is to make sure the days are all workdays
Input:
    - wdays: given weather days
    - max_d: if the corresponding wday isn't a weekday, then a random day will be assigned
             to for the heat load day within a distance of max_d
    - non_workdays: a list of integers, defining the weekends and holidays.
Output:
    - hldays: an array of heat load days
'''
def neighbor_days2(wdays,non_workdays,max_d,max_days = 360):
    # avoid weekdays # make sure the days are all weekdays
    N = max_days # wdays.shape[0]
   
    hldays = np.empty(wdays.shape,dtype=int)
    for i,day in enumerate(wdays):
        hldays[i] = wdays[i] + np.random.randint(2*max_d+1) - max_d
        # if is non_workdays, resample until it's a workday and 1<=hldays[i]<=N
        while hldays[i] in non_workdays or hldays[i]<1 or hldays[i]>N:
            hldays[i] = wdays[i] + np.random.randint(2*max_d+1) - max_d
            # make sure no minus days or days greater than N
            hldays[i] = hldays[i] - 1
            hldays[i] = hldays[i] % N + 1
    return(hldays)



## Simulation

from pymodelica import compile_fmu
from pyfmi import load_fmu
import numpy as np

# Normal model
modelList = ['HVACv3a_weather_load',
             'TestSys.HVACv4_weather_load',
             'TestSys.HVACv4a_weather_load',
             'TestSys.HVACv6a_3room'
            ]
# # Faulty model            
# modelList = ['TestSys.HVACv6a_3R_Fault1',
#              'TestSys.HVACv6a_3R_Fault2',
#              'TestSys.HVACv6a_3R_Fault3',
#              'TestSys.HVACv6a_3R_Fault4',
#              'TestSys.HVACv6a_3R_Fault5',
#              'TestSys.HVACv6a_3R_Fault3_2'
#             ]


# Model files
model_name = modelList[3]
mo_file1 = 'C:\\Users\\James\\OneDrive\\Documents\\Berkeley\\HVAC\\Modelica\\Test\\TestSys\\TestSys'
mo_file2 = 'C:\\Users\\James\\Desktop\\Buildings 4.0.0'
mo_files = mo_file1 + ',' + mo_file2

# File path
filePath = 'C:\\Users\\Public\\Documents\\JModelica.org\\'
fileName = (model_name).replace('.','_')

# Compile FMU, can skip if already compiled before
# fmu = compile_fmu(model_name,mo_files)

# Load compiled FMU
fmu = fileName + '.fmu'

# Load weather_file
w_filePath = 'L:\\HVAC_ModelicaModel_Data\\NOAA_WeatherData'
w_fileName = 'SF2010_TemperatureData.csv' # 'Boston2010_TemperatureData.csv'
weather_file = w_filePath + '\\' + w_fileName

# # Load load_file: This is the room heat load data
# l_filePath = 'L:\\HVAC_ModelicaModel_Data\\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States'
# l_fileName = 'SF_LargeOfficeNew2004.csv' # 'SF_SmallOfficeNew2004.csv' # 'SF_LargeOfficeNew2004.csv'
# load_file = l_filePath + '\\' + l_fileName

# Load multiple load_files:
l_filePath = 'L:\\HVAC_ModelicaModel_Data\\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States'
l_fileNames = ['SF_LargeOfficeNew2004.csv','SF_LargeOfficeNew2004.csv','SF_LargeOfficeNew2004.csv']#['SF_SmallOfficeNew2004.csv','SF_LargeOfficeNew2004.csv','SF_PrimarySchoolNew2004.csv']
load_files = []
for l_fileName in l_fileNames:
    load_file = l_filePath + '\\' + l_fileName
    load_files.append(load_file)


# Load selected variables
s_filePath = 'C:\\Users\\James\\OneDrive\\Documents\\Berkeley\\HVAC\\Modelica\\Test'
s_fileName = 'selected_variable_list_for_HVACv6a_3room' #'selected_variable_list'
selected_variable_list = s_filePath + '\\' + s_fileName

# Set parameter
# param = 'TemperatureSetpoint.k'
# param_range = np.linspace(273.15+20,273.15+30,6)

# Run time
start_time = 0.
final_time = 86400.
data_points = 4320#8640


# Run simulations over random combination of weather and heat load in dataset
N = 110 # number of combinations
max_days = WeatherDataShape(weather_file)[1] # number of days in weather dataset
wdays = np.random.randint(1,max_days,N) # list of days, days start from 1 (NOT 0) to end


# Using a list to exclude non-workdays for heatload data
non_workdays_file = r'L:\HVAC_ModelicaModel_Data\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States\SF_smalloffice_weekends+holidays.csv'
non_workdays = np.loadtxt(non_workdays_file)

# hldays = neighbor_days2(wdays,non_workdays,5,363)
hlparam_names = ['RoomLoadData','RoomLoadData2','RoomLoadData3']
n_rooms = len(hlparam_names)
hldays_set = []
for i in range(n_rooms):
    hldays = neighbor_days2(wdays,non_workdays,max_d=5,max_days = max_days)
    hldays_set.append(hldays) 


for i,day in enumerate(wdays):
    model = load_fmu(fmu) # if fmu already compiled, can use model = load_fmu(fileName+'.fmu')
    LoadWeatherData(model,weather_file,day = day) # set weather data
    # LoadHeatLoadData(model,load_file,day = hldays[day]) # set room heat load data
    multi_hldays = [hldays_set[j][i] for j in range(n_rooms)] # set multiple room heat load data
    LoadMultiHeatLoadData(model,load_files,days = multi_hldays,param_names = hlparam_names,scale_factor=0.7)
    opts = model.simulate_options()
    opts['ncp'] = data_points # Changing the number of communication points
    res = model.simulate(start_time = start_time, final_time = final_time, options=opts)
    
    # export selected variables
    exportPath = 'L:\\HVAC_ModelicaModel_Data\\231_HVACv6a_3room_SF+LargeOffice_Workday_random\\'
    variables = SelectedVars(selected_variable_list)
    ExportVars(res,variables,exportPath+fileName + '_' + WeatherDataDate(weather_file,day) + '_' + str(multi_hldays))



