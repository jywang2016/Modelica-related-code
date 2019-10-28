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

# # Normal model
# modelList = ['HVACv3a_weather_load',
#              'TestSys.HVACv4_weather_load',
#              'TestSys.HVACv4a_weather_load'
#             ]
# Faulty model            
modelList = ['TestSys.HVACv4a_WL_Fault1',
             'TestSys.HVACv4a_WL_Fault2',
             'TestSys.HVACv4a_WL_Fault3',
             'TestSys.HVACv4a_WL_Fault5',
             'TestSys.HVACv4a_WL_Fault6',
             'TestSys.HVACv4a_WL_Fault1_OAD',
             'TestSys.HVACv4a_WL_Fault3_orifice',
             'TestSys.HVACv4a_WL_Fault6_2'
            ]


# Model files
model_name = modelList[7]
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
w_filePath = 'N:\\HVAC_ModelicaModel_Data\\NOAA_WeatherData'
w_fileName = 'Boston2010_TemperatureData.csv' # 'SF2010_TemperatureData.csv'
weather_file = w_filePath + '\\' + w_fileName

# Load load_file: This is the room heat load data
l_filePath = 'N:\\HVAC_ModelicaModel_Data\\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States'
l_fileName = 'SF_LargeOfficeNew2004.csv' # 'SF_SmallOfficeNew2004.csv' # 'SF_LargeOfficeNew2004.csv'
load_file = l_filePath + '\\' + l_fileName

# Load selected variables
s_filePath = 'C:\\Users\\James\\OneDrive\\Documents\\Berkeley\\HVAC\\Modelica\\Test'
s_fileName = 'selected_variable_list'
selected_variable_list = s_filePath + '\\' + s_fileName

# Set parameter
# param = 'TemperatureSetpoint.k'
# param_range = np.linspace(273.15+20,273.15+30,6)

# Run time
start_time = 0.
final_time = 86400.
data_points = 8640


# Run simulations over random combination of weather and heat load in dataset
N = 110 # number of combinations
wdays = WeatherDataShape(weather_file)[1] # number of days in weather dataset
wdays = np.random.randint(1,wdays,N) # list of days, days start from 1 (NOT 0) to end
# hldays = WeatherDataShape(load_file)[1] # number of days in heatload dataset
# hldays = np.random.randint(1,hldays,N) 
# hldays = neighbor_days(wdays,5,363,[0,1])

non_workdays_file = r'N:\HVAC_ModelicaModel_Data\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States\SF_smalloffice_weekends+holidays.csv'
non_workdays = np.loadtxt(non_workdays_file)
hldays = neighbor_days2(wdays,non_workdays,5,363)
 

# days = list(range(1,3))
for day in range(N):
    model = load_fmu(fmu) # if fmu already compiled, can use model = load_fmu(fileName+'.fmu')
    LoadWeatherData(model,weather_file,day = wdays[day]) # set weather data
    LoadHeatLoadData(model,load_file,day = hldays[day]) # set room heat load data
    opts = model.simulate_options()
    opts['ncp'] = data_points # Changing the number of communication points
    res = model.simulate(start_time = start_time, final_time = final_time, options=opts)
    
    # export selected variables
    exportPath = 'N:\\HVAC_ModelicaModel_Data\\169_HVACv4a_Boston+LargeOffice_Workday_Fault6_2\\'
    variables = SelectedVars(selected_variable_list)
    ExportVars(res,variables,exportPath+fileName + '_' + str(wdays[day]) + '_' + str(hldays[day]))



