within TestSys;

model AHUwithHeating_v3
  // v3:
  // AHUwithHeating_v2 is too complicated, causing the solver encountering numerical issues
  // Simplified by using HeatingLoop_v3 instead of HeatingLoop_v2
  // To control heating power, use flow bypass method instead. This is because of numerical problems.

  package air = Buildings.Media.Air "Medium air";
  package water = Buildings.Media.Water "Medium water";
  Buildings.Fluid.MixingVolumes.MixingVolume Room(redeclare package Medium = air, T_start = system.T_ambient - 25, V = 10 * 10 * 3, m_flow_nominal = 1, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {84, -8}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexHeatingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.8, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {43, 59}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
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
  TestSys.HeatingLoop_v3 heatingLoop_v3 annotation(
    Placement(visible = true, transformation(origin = {43, 29}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
  Modelica.Blocks.Sources.Constant const_yboiler(k = 1)  annotation(
    Placement(visible = true, transformation(origin = {17, 33}, extent = {{-7, -7}, {7, 7}}, rotation = 0)));
  TestSys.FlowSwitchValve flowSwitchValve1(redeclare package Medium = air) annotation(
    Placement(visible = true, transformation(origin = {18, 70}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction jun(redeclare package Medium = air, dp_nominal = {30, 30, 30}, m_flow_nominal = {0.5, -1, 0.5}) annotation(
    Placement(visible = true, transformation(origin = {64, 76}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Sources.Pulse pulse1(period = 300)  annotation(
    Placement(visible = true, transformation(origin = {47, 91}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
equation
  connect(pulse1.y, flowSwitchValve1.u) annotation(
    Line(points = {{42, 92}, {18, 92}, {18, 78}, {18, 78}}, color = {0, 0, 127}));
  connect(jun.port_2, Room.ports[1]) annotation(
    Line(points = {{68, 76}, {74, 76}, {74, -8}, {74, -8}}, color = {0, 127, 255}));
  connect(hexHeatingCoil.port_b1, jun.port_3) annotation(
    Line(points = {{52, 64}, {64, 64}, {64, 72}, {64, 72}}, color = {0, 127, 255}));
  connect(flowSwitchValve1.port_b1, jun.port_1) annotation(
    Line(points = {{24, 76}, {60, 76}, {60, 76}, {60, 76}}, color = {0, 127, 255}));
  connect(flowSwitchValve1.port_b2, hexHeatingCoil.port_a1) annotation(
    Line(points = {{24, 64}, {34, 64}, {34, 64}, {34, 64}}, color = {0, 127, 255}));
  connect(ahu1.port_SA, flowSwitchValve1.port_a) annotation(
    Line(points = {{-6, 58}, {10, 58}, {10, 70}, {10, 70}}, color = {0, 127, 255}));
  connect(const_yboiler.y, heatingLoop_v3.yBoilerPower) annotation(
    Line(points = {{24, 34}, {30, 34}, {30, 32}, {30, 32}}, color = {0, 0, 127}));
  connect(hexHeatingCoil.port_a2, heatingLoop_v3.port_b) annotation(
    Line(points = {{52, 54}, {52, 41}}, color = {0, 127, 255}));
  connect(heatingLoop_v3.port_a, hexHeatingCoil.port_b2) annotation(
    Line(points = {{34, 41}, {34, 54}}, color = {0, 127, 255}));
  connect(senToutside.T, heatingLoop_v3.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 90}, {30, 90}, {30, 42}}, color = {0, 0, 127}));
  connect(OutsideTemp.y, Outside.T_in) annotation(
    Line(points = {{-85, 91}, {-74, 91}, {-74, 80}}, color = {0, 0, 127}));
  connect(Room.ports[2], ahu1.port_RA) annotation(
    Line(points = {{74, -8}, {8, -8}, {8, 49}, {-7, 49}}, color = {0, 127, 255}));
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
end AHUwithHeating_v3;
