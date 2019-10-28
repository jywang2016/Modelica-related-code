within TestSys;

model HVACv4a_WL_Fault1
  // v4a_WL_Fault1
  // Add in fault1: Stuck/clogged SAD simulated by limiting the ySAD signal
  // v4a_weather_load
  // Use ControlUnitType3
  // v4_weather_load
  // Use CoolingLoop_v5, which adds in safetybox to prevent water freezing
  // v3a_weather_load:
  // Add in energy load in room. Data source:
  // https://openei.org/doe-opendata/dataset/commercial-and-residential-hourly-load-profiles-for-all-tmy3-locations-in-the-united-states
  // https://openei.org/datasets/files/961/pub/
  // v3a_weather:
  // Add in real weather data with TimeTable component, CombiTimeTable doesn't work for some unknown reason
  // v3a:
  // Use controller type 2
  // v3:
  // Add in controlling unit
  // v2:
  // Using HeatingLoop_v3 and CoolingLoop_v4 (AHUwithHeating_v3 and AHUwithCooling_v3 setup)
  package air = Buildings.Media.Air "Medium air";
  package water = Buildings.Media.Water "Medium water";
  Buildings.Fluid.MixingVolumes.MixingVolume Room(redeclare package Medium = air, T_start = system.T_ambient - 25, V = 10 * 10 * 3, m_flow_nominal = 1, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {84, -24}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexHeatingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.8, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {35, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  TestSys.AHU ahu1(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {-29, 53}, extent = {{-15, -15}, {15, 15}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senToutside(redeclare package Medium = air, TAmb = system.T_ambient, T_start = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {-54, 58}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT Outside(redeclare package Medium = air, nPorts = 2, use_T_in = true) annotation(
    Placement(visible = true, transformation(origin = {-78, 68}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Constant OutsideTemp(k = 288.15) annotation(
    Placement(visible = true, transformation(origin = {-91, 91}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient(displayUnit = "K") = OutsideTemp.k, T_start = OutsideTemp.k) annotation(
    Placement(visible = true, transformation(origin = {-80, -22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const_yPower(k = 1) annotation(
    Placement(visible = true, transformation(origin = {9, 25}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexCoolingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {73, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  TestSys.HeatingLoop_v3 heatingLoop_v3 annotation(
    Placement(visible = true, transformation(origin = {35, 21}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
  TestSys.CoolingLoop_v5 coolingLoop_v5 annotation(
    Placement(visible = true, transformation(origin = {73, 21}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
  TestSys.FlowSwitchValve swValHeating(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {12, 64}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction junHeating(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {44, 70}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  TestSys.FlowSwitchValve swValCooling(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {58, 76}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction junCooling(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {82, 72}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  TestSys.ControlUnitType3 controlUnit(kd = 0, ki = 9.26e-4, kp = 0.25, maxPower = 1, minPower = 0.005, setSAT = false, uFan = 2000) annotation(
    Placement(visible = true, transformation(origin = {-52, 16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senRAT(redeclare package Medium = air, T(start = Room.T_start), TAmb = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {20, -24}, extent = {{6, -6}, {-6, 6}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senSAT(redeclare package Medium = air, TAmb = system.T_ambient, T_start = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {86, 8}, extent = {{-6, 6}, {6, -6}}, rotation = -90)));
  Modelica.Blocks.Sources.Constant TemperatureSetpoint(k = 273.15 + 22) annotation(
    Placement(visible = true, transformation(origin = {-80, 8}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable WeatherData(table = [0, 286.45; 3600, 286.35; 7200, 286.05; 10800, 285.95; 14400, 285.95; 18000, 286.55; 21600, 287.95; 25200, 289.25; 28800, 290.35; 32400, 291.45; 36000, 292.65; 39600, 293.65; 43200, 294.05; 46800, 293.95; 50400, 293.45; 54000, 292.65; 57600, 291.75; 61200, 290.55; 64800, 289.15; 68400, 288.05; 72000, 287.55; 75600, 287.25; 79200, 286.95; 82800, 286.75]) annotation(
    Placement(visible = true, transformation(origin = {-61, 91}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable RoomLoadData(table = [0, 287.77; 3600, 287.77; 7200, 287.77; 10800, 299.99; 14400, 349.36; 18000, 385.26; 21600, 500.73; 25200, 1104.99; 28800, 1162.74; 32400, 1199.23; 36000, 1295.34; 39600, 1280.87; 43200, 1339.25; 46800, 1339.58; 50400, 1342.11; 54000, 1392.05; 57600, 1282.42; 61200, 1077.97; 64800, 1060.96; 68400, 958.38; 72000, 903.05; 75600, 349.36; 79200, 299.99; 82800, 287.77])  annotation(
    Placement(visible = true, transformation(origin = {39, -9}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Buildings.HeatTransfer.Sources.PrescribedHeatFlow HeatLoad annotation(
    Placement(visible = true, transformation(origin = {57, -9}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Nonlinear.Limiter limiter1(uMax = 0.5, uMin = 0.4)  annotation(
    Placement(visible = true, transformation(origin = {-15, 81}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
equation
  connect(limiter1.y, ahu1.y_SA) annotation(
    Line(points = {{-21, 81}, {-24, 81}, {-24, 66}}, color = {0, 0, 127}));
  connect(controlUnit.ySAD, limiter1.u) annotation(
    Line(points = {{-44, 22}, {-6, 22}, {-6, 81}, {-9, 81}}, color = {0, 0, 127}));
  connect(RoomLoadData.y, HeatLoad.Q_flow) annotation(
    Line(points = {{45, -9}, {52, -9}}, color = {0, 0, 127}));
  connect(HeatLoad.port, Room.heatPort) annotation(
    Line(points = {{62, -9}, {84, -9}, {84, -14}}, color = {191, 0, 0}));
  connect(senToutside.T, heatingLoop_v3.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 90}, {22, 90}, {22, 34}}, color = {0, 0, 127}));
  connect(heatingLoop_v3.port_b, hexHeatingCoil.port_a2) annotation(
    Line(points = {{44, 33}, {44, 47.3}}, color = {0, 127, 255}));
  connect(heatingLoop_v3.port_a, hexHeatingCoil.port_b2) annotation(
    Line(points = {{26, 33}, {26, 47}}, color = {0, 127, 255}));
  connect(const_yPower.y, heatingLoop_v3.yBoilerPower) annotation(
    Line(points = {{14.5, 25}, {22, 25}}, color = {0, 0, 127}));
  connect(WeatherData.y, Outside.T_in) annotation(
    Line(points = {{-66, 92}, {-74, 92}, {-74, 80}, {-74, 80}}, color = {0, 0, 127}));
  connect(senSAT.port_b, Room.ports[1]) annotation(
    Line(points = {{86, 2}, {86, 2}, {86, -6}, {74, -6}, {74, -24}, {74, -24}}, color = {0, 127, 255}));
  connect(junCooling.port_2, senSAT.port_a) annotation(
    Line(points = {{86, 72}, {86, 72}, {86, 14}, {86, 14}}, color = {0, 127, 255}));
  connect(senSAT.T, controlUnit.uSAT) annotation(
    Line(points = {{79, 8}, {79, -2}, {-62, -2}, {-62, 14}, {-58, 14}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, swValHeating.port_a) annotation(
    Line(points = {{-16, 58}, {-4, 58}, {-4, 64}, {4, 64}, {4, 64}}, color = {0, 127, 255}));
  connect(TemperatureSetpoint.y, controlUnit.uSP) annotation(
    Line(points = {{-72, 8}, {-58, 8}, {-58, 8}, {-58, 8}}, color = {0, 0, 127}));
  connect(swValCooling.port_b2, junCooling.port_1) annotation(
    Line(points = {{64, 82}, {72, 82}, {72, 72}, {78, 72}, {78, 72}}, color = {0, 127, 255}));
  connect(swValCooling.port_b1, hexCoolingCoil.port_a1) annotation(
    Line(points = {{64, 72}, {64, 72}, {64, 58}, {64, 58}}, color = {0, 127, 255}));
  connect(junHeating.port_2, swValCooling.port_a) annotation(
    Line(points = {{48, 70}, {49.5, 70}, {49.5, 76}, {50, 76}}, color = {0, 127, 255}));
  connect(controlUnit.yCooling, swValCooling.u) annotation(
    Line(points = {{-44, 8}, {54, 8}, {54, 68}, {58, 68}}, color = {0, 0, 127}));
  connect(swValHeating.port_b2, junHeating.port_1) annotation(
    Line(points = {{18, 70}, {40, 70}, {40, 70}, {40, 70}}, color = {0, 127, 255}));
  connect(swValHeating.port_b1, hexHeatingCoil.port_a1) annotation(
    Line(points = {{18, 60}, {26, 60}, {26, 58}, {26, 58}}, color = {0, 127, 255}));
  connect(controlUnit.yHeating, swValHeating.u) annotation(
    Line(points = {{-44, 10}, {2, 10}, {2, 56}, {12, 56}}, color = {0, 0, 127}));
  connect(controlUnit.yEAD, ahu1.y_EA) annotation(
    Line(points = {{-44, 18}, {-36, 18}, {-36, 40}, {-36, 40}}, color = {0, 0, 127}));
  connect(controlUnit.yRAD, ahu1.y_RA) annotation(
    Line(points = {{-44, 20}, {-24, 20}, {-24, 48}, {-26, 48}}, color = {0, 0, 127}));
  connect(controlUnit.yOAD, ahu1.y_OA) annotation(
    Line(points = {{-44, 24}, {-46, 24}, {-46, 74}, {-36, 74}, {-36, 66}, {-36, 66}}, color = {0, 0, 127}));
  connect(controlUnit.yFan, ahu1.y_fanOA) annotation(
    Line(points = {{-44, 14}, {-40, 14}, {-40, 66}, {-40, 66}}, color = {0, 0, 127}));
  connect(controlUnit.yFan, ahu1.y_fanRA) annotation(
    Line(points = {{-44, 14}, {-16, 14}, {-16, 40}, {-16, 40}, {-16, 40}}, color = {0, 0, 127}));
  connect(senRAT.T, controlUnit.uRAT) annotation(
    Line(points = {{20, -18}, {20, -18}, {20, -8}, {-66, -8}, {-66, 18}, {-58, 18}, {-58, 18}}, color = {0, 0, 127}));
  connect(ahu1.port_EA, Outside.ports[2]) annotation(
    Line(points = {{-41, 49}, {-81, 49}, {-81, 57.1}, {-79, 57.1}}, color = {0, 127, 255}));
  connect(senToutside.port_b, ahu1.port_OA) annotation(
    Line(points = {{-48, 58}, {-41, 58}}, color = {0, 127, 255}));
  connect(senRAT.port_b, ahu1.port_RA) annotation(
    Line(points = {{14, -24}, {-2, -24}, {-2, 49}, {-17, 49}}, color = {0, 127, 255}));
  connect(senToutside.T, controlUnit.uOAT) annotation(
    Line(points = {{-54, 64}, {-64, 64}, {-64, 24}, {-58, 24}, {-58, 24}}, color = {0, 0, 127}));
  connect(Room.ports[2], senRAT.port_a) annotation(
    Line(points = {{74, -24}, {26, -24}}, color = {0, 127, 255}));
  connect(junCooling.port_3, hexCoolingCoil.port_b1) annotation(
    Line(points = {{82, 68}, {82, 58}}, color = {0, 127, 255}));
  connect(coolingLoop_v5.port_a, hexCoolingCoil.port_b2) annotation(
    Line(points = {{64, 33}, {64, 33}, {64, 47}, {64, 47}}, color = {0, 127, 255}));
  connect(coolingLoop_v5.port_b, hexCoolingCoil.port_a2) annotation(
    Line(points = {{82, 33}, {82, 33}, {82, 47}, {82, 47}}, color = {0, 127, 255}));
  connect(const_yPower.y, coolingLoop_v5.yCooling) annotation(
    Line(points = {{14.5, 25}, {18.5, 25}, {18.5, 5}, {46.5, 5}, {46.5, 21}, {61, 21}}, color = {0, 0, 127}));
  connect(senToutside.T, coolingLoop_v5.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 90}, {60, 90}, {60, 31.5}}, color = {0, 0, 127}));
  connect(hexHeatingCoil.port_b1, junHeating.port_3) annotation(
    Line(points = {{44, 58.4}, {44, 58.4}, {44, 66.4}, {44, 66.4}}, color = {0, 127, 255}));
  connect(Outside.ports[1], senToutside.port_a) annotation(
    Line(points = {{-78, 58}, {-60, 58}}, color = {0, 127, 255}));
end HVACv4a_WL_Fault1;
