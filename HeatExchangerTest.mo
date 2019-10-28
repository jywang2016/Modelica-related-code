within TestSys;

model HeatExchangerTest
  package water = Buildings.Media.Water;
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hex(redeclare package Medium1 = water, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.2, m1_flow_nominal = 5, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source1(redeclare package Medium = water, m_flow = 1, nPorts = 1, use_T_in = true) annotation(
    Placement(visible = true, transformation(origin = {-40, 20}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source2(redeclare package Medium = water, m_flow = 1, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {40, -20}, extent = {{-6, -6}, {6, 6}}, rotation = 180)));
  Buildings.Fluid.Sources.FixedBoundary sink1(redeclare package Medium = water, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {41, 21}, extent = {{-5, -5}, {5, 5}}, rotation = 180)));
  Buildings.Fluid.Sources.FixedBoundary sink2(redeclare package Medium = water, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {-41, -21}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senTem1(redeclare package Medium = water, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {24, 20}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senTem2(redeclare package Medium = water, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {-22, -12}, extent = {{4, -4}, {-4, 4}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp temperature(duration = 300, height = 80, offset = 273.15 + 10) annotation(
    Placement(visible = true, transformation(origin = {-41, 3}, extent = {{-5, -5}, {5, 5}}, rotation = 180)));
equation
  connect(temperature.y, source1.T_in) annotation(
    Line(points = {{-46, 4}, {-52, 4}, {-52, 22}, {-48, 22}, {-48, 22}}, color = {0, 0, 127}));
  connect(senTem2.port_b, sink2.ports[1]) annotation(
    Line(points = {{-26, -12}, {-36, -12}, {-36, -20}, {-36, -20}}, color = {0, 127, 255}));
  connect(hex.port_b2, senTem2.port_a) annotation(
    Line(points = {{-10, -6}, {-18, -6}, {-18, -12}, {-18, -12}}, color = {0, 127, 255}));
  connect(senTem1.port_b, sink1.ports[1]) annotation(
    Line(points = {{28, 20}, {36, 20}, {36, 22}, {36, 22}}, color = {0, 127, 255}));
  connect(hex.port_b1, senTem1.port_a) annotation(
    Line(points = {{10, 6}, {20, 6}, {20, 20}, {20, 20}}, color = {0, 127, 255}));
  connect(source2.ports[1], hex.port_a2) annotation(
    Line(points = {{34, -20}, {10, -20}, {10, -6}, {10, -6}}, color = {0, 127, 255}));
  connect(source1.ports[1], hex.port_a1) annotation(
    Line(points = {{-34, 20}, {-10, 20}, {-10, 6}, {-10, 6}}, color = {0, 127, 255}));
end HeatExchangerTest;
