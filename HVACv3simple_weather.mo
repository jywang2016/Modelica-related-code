within TestSys;

model HVACv3simple_weather
  // v3simple_weather:
  // Add in real weather data with TimeTable component, CombiTimeTable doesn't work for some unknown reason
  // v3simple:
  // Simplified by taking out real cooling and heating sub-systems
  // v3a:
  // Use controller type 2
  // v3:
  // Add in controlling unit
  // v2:
  // Using HeatingLoop_v3 and CoolingLoop_v4 (AHUwithHeating_v3 and AHUwithCooling_v3 setup)
  package air = Buildings.Media.Air "Medium air";
  package water = Buildings.Media.Water "Medium water";
  Buildings.Fluid.MixingVolumes.MixingVolume Room(redeclare package Medium = air, T_start = OutsideTemp.k - 25, V = 10 * 10 * 3, m_flow_nominal = 1, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {84, -24}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexHeatingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.8, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {35, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  TestSys.AHU ahu1(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {-29, 53}, extent = {{-15, -15}, {15, 15}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senToutside(redeclare package Medium = air, TAmb = system.T_ambient, T_start = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {-54, 58}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT Outside(redeclare package Medium = air, nPorts = 2, use_T_in = true) annotation(
    Placement(visible = true, transformation(origin = {-78, 68}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  inner Modelica.Fluid.System system(T_ambient(displayUnit = "degC") = OutsideTemp.k, T_start = OutsideTemp.k) annotation(
    Placement(visible = true, transformation(origin = {-80, -22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexCoolingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {73, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  TestSys.FlowSwitchValve switchValHeating(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {12, 64}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction junHeating(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {44, 70}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  TestSys.FlowSwitchValve swValCooling(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {58, 76}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction junCooling(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {82, 72}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  TestSys.ControlUnitType2 controlUnit(kd = 0, kp = 0.8, setSAT = true)  annotation(
    Placement(visible = true, transformation(origin = {-52, 16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senRAT(redeclare package Medium = air, T(start = Room.T_start), TAmb = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {20, -24}, extent = {{6, -6}, {-6, 6}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senSAT(redeclare package Medium = air, TAmb = system.T_ambient, T_start = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {92, 8}, extent = {{-6, 6}, {6, -6}}, rotation = -90)));
  Buildings.Fluid.Sources.MassFlowSource_T hSource(redeclare package Medium = water, T = 273.15 + 80, m_flow = 1, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {44, 32}, extent = {{-6, -6}, {6, 6}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT hSink(redeclare package Medium = water, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {25, 31}, extent = {{-5, -5}, {5, 5}}, rotation = 90)));
  Buildings.Fluid.Sources.MassFlowSource_T cSource(redeclare package Medium = water, T = 273.15 + 8, m_flow = 1, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {82, 32}, extent = {{-6, -6}, {6, 6}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT cSink(redeclare package Medium = water, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {65, 33}, extent = {{-5, -5}, {5, 5}}, rotation = 90)));
  Modelica.Blocks.Sources.Constant TemperatureSetpoint(k = 273.15 + 22)  annotation(
    Placement(visible = true, transformation(origin = {-84, 8}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant OutsideTemp(k = 288.15) annotation(
    Placement(visible = true, transformation(origin = {-91, 91}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable WeatherData(table = [0, 279.3; 3600, 279.3; 7200, 278.7; 10800, 278.2; 14400, 278.2; 18000, 278.2; 21600, 277.6; 25200, 277.6; 28800, 278.2; 32400, 281.5; 36000, 283.7; 39600, 285.4; 43200, 287.6; 46800, 289.3; 50400, 289.8; 54000, 290.9; 57600, 290.9; 61200, 290.4; 64800, 288.7; 68400, 287; 72000, 285.4; 75600, 284.3; 79200, 283.7; 82800, 283.2])  annotation(
    Placement(visible = true, transformation(origin = {-57, 91}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
equation
  connect(WeatherData.y, Outside.T_in) annotation(
    Line(points = {{-62, 92}, {-74, 92}, {-74, 80}, {-74, 80}}, color = {0, 0, 127}));
  connect(senSAT.port_b, Room.ports[1]) annotation(
    Line(points = {{92, 2}, {92, 2}, {92, -6}, {74, -6}, {74, -24}, {74, -24}}, color = {0, 127, 255}));
  connect(junCooling.port_2, senSAT.port_a) annotation(
    Line(points = {{86, 72}, {92, 72}, {92, 14}, {92, 14}}, color = {0, 127, 255}));
  connect(senSAT.T, controlUnit.uSAT) annotation(
    Line(points = {{85, 8}, {85, -2}, {-62, -2}, {-62, 14}, {-58, 14}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, switchValHeating.port_a) annotation(
    Line(points = {{-16, 58}, {-6, 58}, {-6, 64}, {4, 64}, {4, 64}}, color = {0, 127, 255}));
  connect(TemperatureSetpoint.y, controlUnit.uSP) annotation(
    Line(points = {{-76, 8}, {-58, 8}, {-58, 8}, {-58, 8}}, color = {0, 0, 127}));
  connect(hexCoolingCoil.port_b2, cSink.ports[1]) annotation(
    Line(points = {{64, 48}, {64, 48}, {64, 38}, {66, 38}}, color = {0, 127, 255}));
  connect(cSource.ports[1], hexCoolingCoil.port_a2) annotation(
    Line(points = {{82, 38}, {82, 38}, {82, 48}, {82, 48}}, color = {0, 127, 255}));
  connect(hexHeatingCoil.port_b2, hSink.ports[1]) annotation(
    Line(points = {{26, 48}, {26, 48}, {26, 36}, {26, 36}}, color = {0, 127, 255}));
  connect(hSource.ports[1], hexHeatingCoil.port_a2) annotation(
    Line(points = {{44, 38}, {44, 38}, {44, 48}, {44, 48}}, color = {0, 127, 255}));
  connect(hexHeatingCoil.port_b1, junHeating.port_3) annotation(
    Line(points = {{44, 58}, {44, 66.4}}, color = {0, 127, 255}));
  connect(switchValHeating.port_b1, hexHeatingCoil.port_a1) annotation(
    Line(points = {{18, 60}, {26, 60}, {26, 58}}, color = {0, 127, 255}));
  connect(swValCooling.port_b2, junCooling.port_1) annotation(
    Line(points = {{64, 82}, {72, 82}, {72, 72}, {78, 72}, {78, 72}}, color = {0, 127, 255}));
  connect(swValCooling.port_b1, hexCoolingCoil.port_a1) annotation(
    Line(points = {{64, 72}, {64, 72}, {64, 58}, {64, 58}}, color = {0, 127, 255}));
  connect(junHeating.port_2, swValCooling.port_a) annotation(
    Line(points = {{48, 70}, {49.5, 70}, {49.5, 76}, {50, 76}}, color = {0, 127, 255}));
  connect(controlUnit.yCooling, swValCooling.u) annotation(
    Line(points = {{-44, 8}, {54, 8}, {54, 68}, {58, 68}}, color = {0, 0, 127}));
  connect(switchValHeating.port_b2, junHeating.port_1) annotation(
    Line(points = {{18, 70}, {40, 70}, {40, 70}, {40, 70}}, color = {0, 127, 255}));
  connect(controlUnit.yHeating, switchValHeating.u) annotation(
    Line(points = {{-44, 10}, {2, 10}, {2, 56}, {12, 56}}, color = {0, 0, 127}));
  connect(controlUnit.yEAD, ahu1.y_EA) annotation(
    Line(points = {{-44, 18}, {-36, 18}, {-36, 40}, {-36, 40}}, color = {0, 0, 127}));
  connect(controlUnit.yRAD, ahu1.y_RA) annotation(
    Line(points = {{-44, 20}, {-24, 20}, {-24, 48}, {-26, 48}}, color = {0, 0, 127}));
  connect(controlUnit.ySAD, ahu1.y_SA) annotation(
    Line(points = {{-44, 22}, {-10, 22}, {-10, 74}, {-24, 74}, {-24, 66}, {-24, 66}}, color = {0, 0, 127}));
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
  connect(Outside.ports[1], senToutside.port_a) annotation(
    Line(points = {{-78, 58}, {-60, 58}}, color = {0, 127, 255}));
end HVACv3simple_weather;
