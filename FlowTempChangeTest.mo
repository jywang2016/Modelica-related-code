within TestSys;

model FlowTempChangeTest
  package air = Buildings.Media.Air "Medium air";
  Buildings.Fluid.Sources.Boundary_pT source(redeclare package Medium = air, T = 273.15 + 22,nPorts = 1, use_T_in = true)  annotation(
    Placement(visible = true, transformation(origin = {-12, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 273.15 + 22)  annotation(
    Placement(visible = true, transformation(origin = {-60, 64}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.PressureDrop res(redeclare package Medium = air,dp_nominal = 100, m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {22, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Sine sine1(amplitude = 3, freqHz = 0.05, offset = 273.15 + 22)  annotation(
    Placement(visible = true, transformation(origin = {-60, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable timeTable1(offset = 273.15, table = [0, 10; 100, 15; 200, 20; 300, 25; 400, 20])  annotation(
    Placement(visible = true, transformation(origin = {-60, 4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient = 295.15)  annotation(
    Placement(visible = true, transformation(origin = {-12, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(sine1.y, source.T_in) annotation(
    Line(points = {{-48, 34}, {-32, 34}, {-32, 64}, {-24, 64}, {-24, 64}}, color = {0, 0, 127}));
  connect(source.ports[1], res.port_a) annotation(
    Line(points = {{-2, 60}, {12, 60}, {12, 60}, {12, 60}}, color = {0, 127, 255}));
end FlowTempChangeTest;
