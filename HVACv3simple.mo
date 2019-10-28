within TestSys;

model HVACv3simple
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
  TestSys.ControlUnit controlUnit1 annotation(
    Placement(visible = true, transformation(origin = {-52, 16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senRAT(redeclare package Medium = air, T(start = Room.T_start), TAmb = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {20, -24}, extent = {{6, -6}, {-6, 6}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senSAT(redeclare package Medium = air, TAmb = system.T_ambient, T_start = system.T_ambient, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {-4, 58}, extent = {{-6, 6}, {6, -6}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T hSource(redeclare package Medium = water, T = 273.15 + 80, m_flow = 1, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {44, 32}, extent = {{-6, -6}, {6, 6}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT hSink(redeclare package Medium = water, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {25, 31}, extent = {{-5, -5}, {5, 5}}, rotation = 90)));
  Buildings.Fluid.Sources.MassFlowSource_T cSource(redeclare package Medium = water, T = 273.15 + 8, m_flow = 1, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {82, 32}, extent = {{-6, -6}, {6, 6}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT cSink(redeclare package Medium = water, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {65, 33}, extent = {{-5, -5}, {5, 5}}, rotation = 90)));
equation
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
  connect(controlUnit1.yCooling, swValCooling.u) annotation(
    Line(points = {{-44, 8}, {54, 8}, {54, 68}, {58, 68}}, color = {0, 0, 127}));
  connect(switchValHeating.port_b2, junHeating.port_1) annotation(
    Line(points = {{18, 70}, {40, 70}, {40, 70}, {40, 70}}, color = {0, 127, 255}));
  connect(senSAT.port_b, switchValHeating.port_a) annotation(
    Line(points = {{2, 58}, {4, 58}, {4, 64}}, color = {0, 127, 255}));
  connect(controlUnit1.yHeating, switchValHeating.u) annotation(
    Line(points = {{-44, 10}, {2, 10}, {2, 56}, {12, 56}}, color = {0, 0, 127}));
  connect(controlUnit1.yEAD, ahu1.y_EA) annotation(
    Line(points = {{-44, 18}, {-36, 18}, {-36, 40}, {-36, 40}}, color = {0, 0, 127}));
  connect(controlUnit1.yRAD, ahu1.y_RA) annotation(
    Line(points = {{-44, 20}, {-24, 20}, {-24, 48}, {-26, 48}}, color = {0, 0, 127}));
  connect(controlUnit1.ySAD, ahu1.y_SA) annotation(
    Line(points = {{-44, 22}, {-10, 22}, {-10, 74}, {-24, 74}, {-24, 66}, {-24, 66}}, color = {0, 0, 127}));
  connect(controlUnit1.yOAD, ahu1.y_OA) annotation(
    Line(points = {{-44, 24}, {-46, 24}, {-46, 74}, {-36, 74}, {-36, 66}, {-36, 66}}, color = {0, 0, 127}));
  connect(controlUnit1.yFan, ahu1.y_fanOA) annotation(
    Line(points = {{-44, 14}, {-40, 14}, {-40, 66}, {-40, 66}}, color = {0, 0, 127}));
  connect(controlUnit1.yFan, ahu1.y_fanRA) annotation(
    Line(points = {{-44, 14}, {-16, 14}, {-16, 40}, {-16, 40}, {-16, 40}}, color = {0, 0, 127}));
  connect(senRAT.T, controlUnit1.uRAT) annotation(
    Line(points = {{20, -18}, {20, -18}, {20, -8}, {-66, -8}, {-66, 18}, {-58, 18}, {-58, 18}}, color = {0, 0, 127}));
  connect(senSAT.T, controlUnit1.uSAT) annotation(
    Line(points = {{-4, 52}, {-4, 52}, {-4, -2}, {-62, -2}, {-62, 14}, {-58, 14}, {-58, 14}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, senSAT.port_a) annotation(
    Line(points = {{-16, 58}, {-10, 58}}, color = {0, 127, 255}));
  connect(ahu1.port_EA, Outside.ports[2]) annotation(
    Line(points = {{-41, 49}, {-81, 49}, {-81, 57.1}, {-79, 57.1}}, color = {0, 127, 255}));
  connect(senToutside.port_b, ahu1.port_OA) annotation(
    Line(points = {{-48, 58}, {-41, 58}}, color = {0, 127, 255}));
  connect(senRAT.port_b, ahu1.port_RA) annotation(
    Line(points = {{14, -24}, {-2, -24}, {-2, 49}, {-17, 49}}, color = {0, 127, 255}));
  connect(senToutside.T, controlUnit1.uOAT) annotation(
    Line(points = {{-54, 64}, {-64, 64}, {-64, 24}, {-58, 24}, {-58, 24}}, color = {0, 0, 127}));
  connect(Room.ports[2], senRAT.port_a) annotation(
    Line(points = {{74, -24}, {26, -24}}, color = {0, 127, 255}));
  connect(junCooling.port_2, Room.ports[1]) annotation(
    Line(points = {{86, 72}, {88, 72}, {88, -6}, {74, -6}, {74, -24}, {74, -24}}, color = {0, 127, 255}));
  connect(junCooling.port_3, hexCoolingCoil.port_b1) annotation(
    Line(points = {{82, 68}, {82, 58}}, color = {0, 127, 255}));
  connect(OutsideTemp.y, Outside.T_in) annotation(
    Line(points = {{-85, 91}, {-74, 91}, {-74, 80}}, color = {0, 0, 127}));
  connect(Outside.ports[1], senToutside.port_a) annotation(
    Line(points = {{-78, 58}, {-60, 58}}, color = {0, 127, 255}));
end HVACv3simple;
