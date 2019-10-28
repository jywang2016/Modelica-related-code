within TestSys;


// As of version 1.11.0(64-bit), Boiler component in Buildings library cannot run. Use Jmodelica as an alternative.
// "Please redeclare it to any package compatible with Modelica.Media.Interfaces.PartialMedium" error while the medium is redeclared

model BoilerTest
  package water = Buildings.Media.Water;
  //package water = Modelica.Media.Water.StandardWater;

  Buildings.Fluid.Sources.Boundary_pT source(redeclare package Medium = water, T = 283.15, nPorts = 1, p = 101325 * 3) annotation(
    Placement(visible = true, transformation(origin = {-68, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT sink(redeclare package Medium = water, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {64, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Boilers.BoilerPolynomial boi(redeclare package Medium = water, Q_flow_nominal = 10000, dp_nominal = 100, energyDynamics = Modelica.Fluid.Types.Dynamics.SteadyState, fue = Buildings.Fluid.Data.Fuels.NaturalGasLowerHeatingValue(), m_flow_nominal = 0.1, massDynamics = Modelica.Fluid.Types.Dynamics.SteadyState) annotation(
    Placement(visible = true, transformation(origin = {-4, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.HeatTransfer.Sources.FixedTemperature fixedTemp1(T = 283.15)  annotation(
    Placement(visible = true, transformation(origin = {-24, 54}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 50, startTime = 25)  annotation(
    Placement(visible = true, transformation(origin = {-48, 28}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(ramp1.y, boi.y) annotation(
    Line(points = {{-36, 28}, {-27, 28}, {-27, 8}, {-16, 8}}, color = {0, 0, 127}));
  connect(fixedTemp1.port, boi.heatPort) annotation(
    Line(points = {{-14, 54}, {-4, 54}, {-4, 8}}, color = {191, 0, 0}));
// must add heatport input!
  connect(boi.port_b, sink.ports[1]) annotation(
    Line(points = {{6, 0}, {54, 0}}, color = {0, 127, 255}));
  connect(source.ports[1], boi.port_a) annotation(
    Line(points = {{-58, 0}, {-14, 0}, {-14, 0}, {-14, 0}}, color = {0, 127, 255}));
end BoilerTest;
