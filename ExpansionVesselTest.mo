within TestSys;

model ExpansionVesselTest
  package water = Buildings.Media.Water "Medium model";

  Buildings.Fluid.Storage.ExpansionVessel expVess(redeclare package Medium = water, V_start = 1, p(displayUnit = "Pa")) annotation(
    Placement(visible = true, transformation(origin = {38, 16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T boundary(redeclare package Medium = water,m_flow = 0.01, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-32, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(boundary.ports[1], expVess.port_a) annotation(
    Line(points = {{-22, 0}, {38, 0}, {38, 6}, {38, 6}}, color = {0, 127, 255}));
end ExpansionVesselTest;
