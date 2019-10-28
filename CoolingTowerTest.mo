within TestSys;
// http://www.engineeringtoolbox.com/cooling-tower-efficiency-d_699.html
model CoolingTowerTest
  package water = Buildings.Media.Water;

  Buildings.Fluid.HeatExchangers.CoolingTowers.FixedApproach fixedApproach1(redeclare package Medium = water, TApp = 12, dp(start = 101325), dp_nominal = 101325, m_flow(start = 0.1), m_flow_nominal = 0.3) annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT source(redeclare package Medium = water,T = 273.15 + 40, nPorts = 1, p = 101325 * 3)  annotation(
    Placement(visible = true, transformation(origin = {-52, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT sink(redeclare package Medium = water,nPorts = 1, use_T_in = true)  annotation(
    Placement(visible = true, transformation(origin = {52, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Sine sine1(amplitude = 5, freqHz = 0.01, offset = 273.15 +20)  annotation(
    Placement(visible = true, transformation(origin = {-38, 46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(fixedApproach1.TLvg, sink.T_in) annotation(
    Line(points = {{12, -6}, {28, -6}, {28, -24}, {74, -24}, {74, -4}, {64, -4}, {64, -4}}, color = {0, 0, 127}));
  connect(fixedApproach1.port_b, sink.ports[1]) annotation(
    Line(points = {{10, 0}, {42, 0}, {42, 0}, {42, 0}}, color = {0, 127, 255}));
  connect(source.ports[1], fixedApproach1.port_a) annotation(
    Line(points = {{-42, 0}, {-10, 0}, {-10, 0}, {-10, 0}}, color = {0, 127, 255}));
  connect(sine1.y, fixedApproach1.TAir) annotation(
    Line(points = {{-26, 46}, {-12, 46}, {-12, 4}, {-12, 4}}, color = {0, 0, 127}));

end CoolingTowerTest;
