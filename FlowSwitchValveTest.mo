within TestSys;

model FlowSwitchValveTest
  package water = Buildings.Media.Water "Medium water";
  Buildings.Fluid.Sources.Boundary_pT bou(redeclare package Medium = water,nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-72, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT bou1(redeclare package Medium = water, nPorts = 2)  annotation(
    Placement(visible = true, transformation(origin = {76, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Movers.FlowControlled_m_flow fan(redeclare package Medium = water, dp_nominal = 300, m_flow_nominal = 2) annotation(
    Placement(visible = true, transformation(origin = {-30, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 4)  annotation(
    Placement(visible = true, transformation(origin = {-52, 66}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  TestSys.FlowSwitchValve flowSwitchValve1(redeclare package Medium = water)  annotation(
    Placement(visible = true, transformation(origin = {8, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const1(k = 0)  annotation(
    Placement(visible = true, transformation(origin = {-8, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Pulse pulse1(period = 200)  annotation(
    Placement(visible = true, transformation(origin = {34, 60}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
equation
  connect(pulse1.y, flowSwitchValve1.u) annotation(
    Line(points = {{22, 60}, {8, 60}, {8, 38}, {8, 38}}, color = {0, 0, 127}));
  connect(flowSwitchValve1.port_b2, bou1.ports[2]) annotation(
    Line(points = {{14, 26}, {66, 26}, {66, 30}}, color = {0, 127, 255}));
  connect(flowSwitchValve1.port_b1, bou1.ports[1]) annotation(
    Line(points = {{14, 36}, {66, 36}, {66, 30}}, color = {0, 127, 255}));
  connect(fan.port_b, flowSwitchValve1.port_a) annotation(
    Line(points = {{-20, 30}, {0, 30}, {0, 30}, {0, 30}}, color = {0, 127, 255}));
  connect(const.y, fan.m_flow_in) annotation(
    Line(points = {{-40, 66}, {-30, 66}, {-30, 42}, {-30, 42}}, color = {0, 0, 127}));
  connect(bou.ports[1], fan.port_a) annotation(
    Line(points = {{-62, 30}, {-40, 30}, {-40, 30}, {-40, 30}}, color = {0, 127, 255}));
  annotation(
    uses(Buildings(version = "4.0.0"), Modelica(version = "3.2.2")));
end FlowSwitchValveTest;
