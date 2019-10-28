
folders = ['165_HVACv4a_Boston+LargeOffice_Workday_Fault5',
           '166_HVACv4a_Boston+LargeOffice_Workday_Fault6',
           '167_HVACv4a_Boston+LargeOffice_Workday_Fault1_OAD',
           '168_HVACv4a_Boston+LargeOffice_Workday_Fault3_orifice',
           '169_HVACv4a_Boston+LargeOffice_Workday_Fault6_2'
           ]


modelList = ['TestSys.HVACv4a_WL_Fault5',
             'TestSys.HVACv4a_WL_Fault6',
             'TestSys.HVACv4a_WL_Fault1_OAD',
             'TestSys.HVACv4a_WL_Fault3_orifice',
             'TestSys.HVACv4a_WL_Fault6_2'
            ]

for i,model_i in enumerate(modelList):
    # Model files
    model_name = model_i
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
    
    
    for day in range(N):
        model = load_fmu(fmu) # if fmu already compiled, can use model = load_fmu(fileName+'.fmu')
        LoadWeatherData(model,weather_file,day = wdays[day]) # set weather data
        LoadHeatLoadData(model,load_file,day = hldays[day]) # set room heat load data
        opts = model.simulate_options()
        opts['ncp'] = data_points # Changing the number of communication points
        res = model.simulate(start_time = start_time, final_time = final_time, options=opts)
        
        # export selected variables
        exportPath = 'N:\\HVAC_ModelicaModel_Data\\' + folders[i] + '\\'
        variables = SelectedVars(selected_variable_list)
        ExportVars(res,variables,exportPath+fileName + '_' + str(wdays[day]) + '_' + str(hldays[day]))


# Model files
model_name = 'TestSys.HVACv4a_weather_load'
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
l_fileName = 'SF_LargeOfficeNew2004.csv' # 'SF_SmallOfficeNew2004.csv' # 'SF_PrimarySchoolNew2004.csv'
load_file = l_filePath + '\\' + l_fileName

# Load selected variables
s_filePath = 'C:\\Users\\James\\OneDrive\\Documents\\Berkeley\\HVAC\\Modelica\\Test'
s_fileName = 'selected_variable_list'
selected_variable_list = s_filePath + '\\' + s_fileName


# Run time
start_time = 0.
final_time = 86400.
data_points = 8640


# Run simulations over days in dataset
days = WeatherDataShape(weather_file)[1] # number of days in the dataset
days = np.arange(1,days) # list(range(1,days)) # list of days, days start from 1 (NOT 0) to end
# hldays = check_weekday(days,max_d=2,weekends=[0,1])

# Using a list to exclude non-workdays for heatload data
non_workdays_file = r'N:\HVAC_ModelicaModel_Data\Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States\SF_smalloffice_weekends+holidays.csv'
non_workdays = np.loadtxt(non_workdays_file)
hldays = check_workday(days,non_workdays,max_d=2)


for i,day in enumerate(days):
    model = load_fmu(fmu) # if fmu already compiled, can use model = load_fmu(fileName+'.fmu')
    LoadWeatherData(model,weather_file,day = day) # set weather data
    LoadHeatLoadData(model,load_file,day = hldays[i]) # set room heat load data
    opts = model.simulate_options()
    opts['ncp'] = data_points # Changing the number of communication points
    res = model.simulate(start_time = start_time, final_time = final_time, options=opts)
    
    # export selected variables
    exportPath = 'N:\\HVAC_ModelicaModel_Data\\160_HVACv4a_Boston+LargeOffice_Workday\\'
    variables = SelectedVars(selected_variable_list)
    ExportVars(res,variables,exportPath+fileName + WeatherDataDate(weather_file,day) + '_' + str(hldays[i]))











