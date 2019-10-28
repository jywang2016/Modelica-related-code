within TestSys;

model HVACv1
  package air = Buildings.Media.Air "Medium air";
  package water = Buildings.Media.Water "Medium water";  
  
  Buildings.Fluid.MixingVolumes.MixingVolume Room(redeclare package Medium = air, T_start = system.T_ambient - 25, V = 10 * 10 * 3, m_flow_nominal = 1, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {84, -24}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexHeatingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.8, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {41, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
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
  inner Modelica.Fluid.System system(T_ambient(displayUnit = "K") = OutsideTemp.k, T_start = OutsideTemp.k)  annotation(
    Placement(visible = true, transformation(origin = {-80, -22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const_yBoiler(k = 1)  annotation(
    Placement(visible = true, transformation(origin = {16, 26}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexCoolingCoil(redeclare package Medium1 = air, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, m1_flow_nominal = 1, m2_flow_nominal = 1)  annotation(
    Placement(visible = true, transformation(origin = {69, 53}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  TestSys.CoolingLoop_v3 coolingLoop_v3 annotation(
    Placement(visible = true, transformation(origin = {69, 23}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
  Modelica.Blocks.Sources.BooleanPulse booleanPulse1(period = 600)  annotation(
    Placement(visible = true, transformation(origin = {23, -15}, extent = {{7, 7}, {-7, -7}}, rotation = -90)));
  TestSys.HeatingLoop_v2 heatingLoop_v2 annotation(
    Placement(visible = true, transformation(origin = {41, 23}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
  Modelica.Blocks.Sources.BooleanConstant booleanConstant1(k = true)  annotation(
    Placement(visible = true, transformation(origin = {53, -15}, extent = {{-7, -7}, {7, 7}}, rotation = 90)));
equation
  connect(booleanConstant1.y, coolingLoop_v3.yOnOff) annotation(
    Line(points = {{54, -8}, {52, -8}, {52, 22}, {56, 22}, {56, 22}}, color = {255, 0, 255}));
  connect(booleanPulse1.y, heatingLoop_v2.yOnOff) annotation(
    Line(points = {{24, -8}, {24, -8}, {24, 16}, {28, 16}, {28, 16}}, color = {255, 0, 255}));
  connect(senToutside.T, heatingLoop_v2.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 64}, {-54, 86}, {28, 86}, {28, 36}, {28, 36}}, color = {0, 0, 127}));
  connect(heatingLoop_v2.port_a, hexHeatingCoil.port_b2) annotation(
    Line(points = {{32, 36}, {32, 36}, {32, 48}, {32, 48}}, color = {0, 127, 255}));
  connect(hexHeatingCoil.port_a2, heatingLoop_v2.port_b) annotation(
    Line(points = {{50, 48}, {50, 48}, {50, 36}, {50, 36}}, color = {0, 127, 255}));
  connect(const_yBoiler.y, heatingLoop_v2.yBoilerPower) annotation(
    Line(points = {{22, 26}, {28, 26}, {28, 26}, {28, 26}}, color = {0, 0, 127}));
  connect(senToutside.T, coolingLoop_v3.T_ambient) annotation(
    Line(points = {{-54, 64}, {-54, 64}, {-54, 86}, {56, 86}, {56, 34}, {56, 34}}, color = {0, 0, 127}));
  connect(hexCoolingCoil.port_b2, coolingLoop_v3.port_a) annotation(
    Line(points = {{60, 48}, {60, 48}, {60, 36}, {60, 36}}, color = {0, 127, 255}));
  connect(hexCoolingCoil.port_a2, coolingLoop_v3.port_b) annotation(
    Line(points = {{78, 48}, {78, 48}, {78, 36}, {78, 36}}, color = {0, 127, 255}));
  connect(hexCoolingCoil.port_b1, Room.ports[1]) annotation(
    Line(points = {{78, 58}, {90, 58}, {90, -6}, {74, -6}, {74, -24}, {74, -24}}, color = {0, 127, 255}));
  connect(Room.ports[2], ahu1.port_RA) annotation(
    Line(points = {{74, -24}, {8, -24}, {8, 49}, {-7, 49}}, color = {0, 127, 255}));
  connect(hexHeatingCoil.port_b1, hexCoolingCoil.port_a1) annotation(
    Line(points = {{50, 58}, {60, 58}, {60, 58}, {60, 58}}, color = {0, 127, 255}));
  connect(OutsideTemp.y, Outside.T_in) annotation(
    Line(points = {{-85, 91}, {-74, 91}, {-74, 80}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, hexHeatingCoil.port_a1) annotation(
    Line(points = {{-7, 58.1}, {12, 58.1}, {12, 58.2}, {31, 58.2}}, color = {0, 127, 255}));
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
end HVACv1;
