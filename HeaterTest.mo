within TestSys;

model HeaterTest
  package water = Buildings.Media.Water;

  Buildings.Fluid.HeatExchangers.HeaterCooler_T heater(redeclare package Medium = water, dp_nominal = 1000, m_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {-20, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source(redeclare package Medium = water, m_flow = 1, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-72, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Fluid.System system annotation(
    Placement(visible = true, transformation(origin = {-76, -32}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 120, height = 100, offset = 273.15, startTime = 30)  annotation(
    Placement(visible = true, transformation(origin = {-48, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Pipes.StaticPipe pipe(redeclare package Medium = water, diameter = 0.2, length = 10) annotation(
    Placement(visible = true, transformation(origin = {22, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT sink(redeclare package Medium = water, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {78, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Sensors.TemperatureTwoPort senTem(redeclare package Medium = water, m_flow_nominal = 0.1) annotation(
    Placement(visible = true, transformation(origin = {51, 1}, extent = {{-7, -7}, {7, 7}}, rotation = 0)));
equation
  connect(senTem.port_b, sink.ports[1]) annotation(
    Line(points = {{58, 2}, {68, 2}, {68, 2}, {68, 2}}, color = {0, 127, 255}));
  connect(pipe.port_b, senTem.port_a) annotation(
    Line(points = {{32, 2}, {44, 2}, {44, 2}, {44, 2}}, color = {0, 127, 255}));
  connect(heater.port_b, pipe.port_a) annotation(
    Line(points = {{-10, 2}, {12, 2}, {12, 2}, {12, 2}, {12, 2}, {12, 2}}, color = {0, 127, 255}));
  connect(ramp1.y, heater.TSet) annotation(
    Line(points = {{-37, 34}, {-33, 34}, {-33, 8}, {-33, 8}, {-33, 8}, {-33, 8}}, color = {0, 0, 127}));
  connect(source.ports[1], heater.port_a) annotation(
    Line(points = {{-62, 2}, {-48, 2}, {-48, 2}, {-30, 2}, {-30, 2}, {-32, 2}, {-32, 2}, {-30, 2}}, color = {0, 127, 255}));
end HeaterTest;
