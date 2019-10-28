within TestSys;

model HeatingLoopTest
  package water = Buildings.Media.Water;
  Buildings.Fluid.Movers.FlowControlled_m_flow pump(redeclare package Medium = water,VMachine_flow(start = 2e-4), m_flow(start = 0.2), m_flow_nominal = 0.2)  annotation(
    Placement(visible = true, transformation(origin = {-60, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe1(redeclare package Medium = water,lambdaIns = 1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.2)  annotation(
    Placement(visible = true, transformation(origin = {0, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Boilers.BoilerPolynomial boiler(redeclare package Medium = water,Q_flow_nominal = 1e5, dp_nominal = 1e5, m_flow_nominal = 0.2)  annotation(
    Placement(visible = true, transformation(origin = {52, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank tank(redeclare package Medium = water,crossArea = 25, height = 3, nPorts = 2, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1)})  annotation(
    Placement(visible = true, transformation(origin = {70, 48}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe2(redeclare package Medium = water,lambdaIns = 1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.2)  annotation(
    Placement(visible = true, transformation(origin = {0, 36}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.HeatTransfer.Sources.FixedTemperature fixedTemperature(T = 293.15)  annotation(
    Placement(visible = true, transformation(origin = {-24, 6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 1)  annotation(
    Placement(visible = true, transformation(origin = {-58, -6}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
equation
  connect(ramp1.y, boiler.y) annotation(
    Line(points = {{-58, -18}, {28, -18}, {28, -38}, {40, -38}, {40, -38}}, color = {0, 0, 127}));
  connect(fixedTemperature.port, pipe1.heatPort) annotation(
    Line(points = {{-14, 6}, {0, 6}, {0, -40}, {0, -40}}, color = {191, 0, 0}));
  connect(fixedTemperature.port, pipe2.heatPort) annotation(
    Line(points = {{-14, 6}, {0, 6}, {0, 32}, {0, 32}}, color = {191, 0, 0}));
  connect(ramp1.y, pump.m_flow_in) annotation(
    Line(points = {{-58, -18}, {-60, -18}, {-60, -34}, {-60, -34}}, color = {0, 0, 127}));
  connect(pipe2.port_b, pump.port_a) annotation(
    Line(points = {{-10, 36}, {-70, 36}, {-70, -46}, {-70, -46}}, color = {0, 127, 255}));
  connect(tank.ports[2], pipe2.port_a) annotation(
    Line(points = {{70, 28}, {22, 28}, {22, 36}, {10, 36}, {10, 36}}, color = {0, 127, 255}));
  connect(boiler.port_b, tank.ports[1]) annotation(
    Line(points = {{62, -46}, {76, -46}, {76, 28}, {70, 28}}, color = {0, 127, 255}));
  connect(pipe1.port_b, boiler.port_a) annotation(
    Line(points = {{10, -46}, {42, -46}, {42, -46}, {42, -46}}, color = {0, 127, 255}));
  connect(pump.port_b, pipe1.port_a) annotation(
    Line(points = {{-50, -46}, {-10, -46}, {-10, -46}, {-10, -46}}, color = {0, 127, 255}));

end HeatingLoopTest;
