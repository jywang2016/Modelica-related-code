within TestSys;

model HeatExchangerTest2
  package water = Buildings.Media.Water;
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hex(redeclare package Medium1 = water, redeclare package Medium2 = water, dp1_nominal = 100, dp2_nominal = 100, eps = 0.6, m1_flow_nominal = 1, m2_flow_nominal = 3) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source2(redeclare package Medium = water, T = 273.15 + 80, m_flow = 3, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {40, -20}, extent = {{-6, -6}, {6, 6}}, rotation = 180)));
  Buildings.Fluid.Sources.FixedBoundary sink2(redeclare package Medium = water, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {-41, -21}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senTem1(redeclare package Medium = water, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {24, 20}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senTem2(redeclare package Medium = water, m_flow_nominal = 3) annotation(
    Placement(visible = true, transformation(origin = {20, -20}, extent = {{4, -4}, {-4, 4}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank tank(redeclare package Medium = water,crossArea = 2, height = 2,nPorts = 2, use_portsData = false)  annotation(
    Placement(visible = true, transformation(origin = {-4, 48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_m_flow pump(redeclare package Medium = water,dp(start = 100), m_flow(start = 1), m_flow_nominal = 1)  annotation(
    Placement(visible = true, transformation(origin = {-38, 6}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant flowrate(k = 1)  annotation(
    Placement(visible = true, transformation(origin = {-19, 17}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
equation
  connect(senTem1.port_b, tank.ports[2]) annotation(
    Line(points = {{28, 20}, {40, 20}, {40, 32}, {-3, 32}, {-3, 38}, {-4, 38}}, color = {0, 127, 255}));
  connect(tank.ports[1], pump.port_a) annotation(
    Line(points = {{-4, 38}, {-4, 26}, {-44, 26}, {-44, 6}}, color = {0, 127, 255}));
  connect(hex.port_b2, sink2.ports[1]) annotation(
    Line(points = {{-10, -6}, {-28, -6}, {-28, -20}, {-36, -20}, {-36, -20}}, color = {0, 127, 255}));
  connect(senTem2.port_b, hex.port_a2) annotation(
    Line(points = {{16, -20}, {16, -20}, {16, -6}, {10, -6}, {10, -6}}, color = {0, 127, 255}));
  connect(source2.ports[1], senTem2.port_a) annotation(
    Line(points = {{34, -20}, {24, -20}, {24, -20}, {24, -20}}, color = {0, 127, 255}));
  connect(flowrate.y, pump.m_flow_in) annotation(
    Line(points = {{-25, 17}, {-38, 17}, {-38, 14}}, color = {0, 0, 127}));
  connect(pump.port_b, hex.port_a1) annotation(
    Line(points = {{-32, 6}, {-10, 6}}, color = {0, 127, 255}));
  connect(hex.port_b1, senTem1.port_a) annotation(
    Line(points = {{10, 6}, {20, 6}, {20, 20}, {20, 20}}, color = {0, 127, 255}));
end HeatExchangerTest2;
