within TestSys;

model HVACv2
  // v2:
  // Using HeatingLoop_v3 and CoolingLoop_v4 (AHUwithHeating_v3 and AHUwithCooling_v3 setup)
  package air = Buildings.Media.Air "Medium air";
  package water = Buildings.Media.Water "Medium water";
  Buildings.Fluid.MixingVolumes.MixingVolume Room(redeclare package Medium = air, T_start = system.T_ambient - 25, V = 10 * 10 * 3, m_flow_nominal = 1, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {84, -24}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexHeatingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.8, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {35, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  TestSys.AHU ahu1(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {-19, 53}, extent = {{-15, -15}, {15, 15}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp damperSignal(duration = 20, height = 0.6, offset = 0.3) annotation(
    Placement(visible = true, transformation(origin = {-60, 22}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Sources.Step fanSignal(height = 800, startTime = 5) annotation(
    Placement(visible = true, transformation(origin = {-60, 40}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
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
  TestSys.CoolingLoop_v4 coolingLoop_v4 annotation(
    Placement(visible = true, transformation(origin = {73, 21}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
  TestSys.FlowSwitchValve switchValHeating(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {12, 64}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction junHeating(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {44, 70}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Sources.Sine sine1(amplitude = 0.5, freqHz = 0.0005, offset = 0.5, phase = 4.71239)  annotation(
    Placement(visible = true, transformation(origin = {-4, 84}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  TestSys.FlowSwitchValve swValCooling(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {58, 76}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction junCooling(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {82, 72}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Sources.Cosine cosine1(amplitude = 0.5, freqHz = 0.0005, offset = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {34, 84}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
equation
  connect(cosine1.y, swValCooling.u) annotation(
    Line(points = {{38, 84}, {58, 84}, {58, 84}, {58, 84}}, color = {0, 0, 127}));
  connect(sine1.y, switchValHeating.u) annotation(
    Line(points = {{0, 84}, {12, 84}, {12, 72}, {12, 72}}, color = {0, 0, 127}));
  connect(junCooling.port_2, Room.ports[1]) annotation(
    Line(points = {{86, 72}, {88, 72}, {88, -6}, {74, -6}, {74, -24}, {74, -24}}, color = {0, 127, 255}));
  connect(junCooling.port_3, hexCoolingCoil.port_b1) annotation(
    Line(points = {{82, 68}, {82, 58}}, color = {0, 127, 255}));
  connect(swValCooling.port_b1, junCooling.port_1) annotation(
    Line(points = {{64, 81}, {71, 81}, {71, 72}, {78, 72}}, color = {0, 127, 255}));
  connect(swValCooling.port_b2, hexCoolingCoil.port_a1) annotation(
    Line(points = {{64, 71}, {64, 58}}, color = {0, 127, 255}));
  connect(junHeating.port_2, swValCooling.port_a) annotation(
    Line(points = {{48, 70}, {49.5, 70}, {49.5, 76}, {50, 76}}, color = {0, 127, 255}));
  connect(coolingLoop_v4.port_a, hexCoolingCoil.port_b2) annotation(
    Line(points = {{64, 33}, {64, 33}, {64, 47}, {64, 47}}, color = {0, 127, 255}));
  connect(coolingLoop_v4.port_b, hexCoolingCoil.port_a2) annotation(
    Line(points = {{82, 33}, {82, 33}, {82, 47}, {82, 47}}, color = {0, 127, 255}));
  connect(const_yPower.y, coolingLoop_v4.yCooling) annotation(
    Line(points = {{14.5, 25}, {18.5, 25}, {18.5, 5}, {46.5, 5}, {46.5, 21}, {61, 21}}, color = {0, 0, 127}));
  connect(senToutside.T, coolingLoop_v4.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 90}, {60, 90}, {60, 31.5}}, color = {0, 0, 127}));
  connect(const_yPower.y, heatingLoop_v3.yBoilerPower) annotation(
    Line(points = {{14.5, 25}, {22.5, 25}, {22.5, 23}, {22.5, 23}}, color = {0, 0, 127}));
  connect(heatingLoop_v3.port_a, hexHeatingCoil.port_b2) annotation(
    Line(points = {{26, 33}, {26, 33}, {26, 47}, {26, 47}}, color = {0, 127, 255}));
  connect(heatingLoop_v3.port_b, hexHeatingCoil.port_a2) annotation(
    Line(points = {{44, 33.3}, {44, 33.3}, {44, 47.3}, {44, 47.3}}, color = {0, 127, 255}));
  connect(switchValHeating.port_b2, hexHeatingCoil.port_a1) annotation(
    Line(points = {{18, 59}, {26, 59}, {26, 59}, {26, 59}}, color = {0, 127, 255}));
  connect(hexHeatingCoil.port_b1, junHeating.port_3) annotation(
    Line(points = {{44, 58.4}, {44, 58.4}, {44, 66.4}, {44, 66.4}}, color = {0, 127, 255}));
  connect(senToutside.T, heatingLoop_v3.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 90}, {22, 90}, {22, 34}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, switchValHeating.port_a) annotation(
    Line(points = {{-6, 58}, {4, 58}, {4, 64}}, color = {0, 127, 255}));
  connect(switchValHeating.port_b1, junHeating.port_1) annotation(
    Line(points = {{18, 69}, {40, 69}, {40, 69}, {40, 69}}, color = {0, 127, 255}));
  connect(Room.ports[2], ahu1.port_RA) annotation(
    Line(points = {{74, -24}, {2, -24}, {2, 49}, {-7, 49}}, color = {0, 127, 255}));
  connect(OutsideTemp.y, Outside.T_in) annotation(
    Line(points = {{-85, 91}, {-74, 91}, {-74, 80}}, color = {0, 0, 127}));
  connect(damperSignal.y, ahu1.y_SA) annotation(
    Line(points = {{-53.4, 22}, {-3.4, 22}, {-3.4, 76}, {-14, 76}, {-14, 66}}, color = {0, 0, 127}));
  connect(damperSignal.y, ahu1.y_OA) annotation(
    Line(points = {{-53.4, 22}, {-41.4, 22}, {-41.4, 76}, {-26, 76}, {-26, 66}}, color = {0, 0, 127}));
  connect(damperSignal.y, ahu1.y_RA) annotation(
    Line(points = {{-53.4, 22}, {-15, 22}, {-15, 48.5}}, color = {0, 0, 127}));
  connect(damperSignal.y, ahu1.y_EA) annotation(
    Line(points = {{-53.4, 22}, {-26, 22}, {-26, 40}}, color = {0, 0, 127}));
  connect(fanSignal.y, ahu1.y_fanRA) annotation(
    Line(points = {{-53.4, 40}, {-45.4, 40}, {-45.4, 10}, {-7, 10}, {-7, 40}}, color = {0, 0, 127}));
  connect(fanSignal.y, ahu1.y_fanOA) annotation(
    Line(points = {{-53.4, 40}, {-45.4, 40}, {-45.4, 64}, {-30, 64}, {-30, 65}}, color = {0, 0, 127}));
  connect(senToutside.port_b, ahu1.port_OA) annotation(
    Line(points = {{-48, 58}, {-30, 58}}, color = {0, 127, 255}));
  connect(ahu1.port_EA, Outside.ports[2]) annotation(
    Line(points = {{-31, 49.1}, {-81, 49.1}, {-81, 57.1}, {-79, 57.1}}, color = {0, 127, 255}));
  connect(Outside.ports[1], senToutside.port_a) annotation(
    Line(points = {{-78, 58}, {-60, 58}}, color = {0, 127, 255}));
end HVACv2;
