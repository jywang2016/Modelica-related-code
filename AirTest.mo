within TestSys;

model AirTest

  package Air = Buildings.Media.Air;

  Buildings.Fluid.MixingVolumes.MixingVolume volRoom(redeclare package Medium = Air, T_start = 300, V = 3 * 3 * 3, m_flow_nominal = 1, nPorts = 2, p_start = 101300)  annotation(
    Placement(visible = true, transformation(origin = {55, 62}, extent = {{-12, -13}, {12, 13}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT airSource(redeclare package Medium = Air, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-74, 80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient = 283.15, m_flow_start = 0.1)  annotation(
      Placement(visible = true, transformation(origin = {-74, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe1(redeclare package Medium = Air, lambdaIns = 0.01, length = 10, m_flow_nominal = 0.01, thicknessIns = 0.01)  annotation(
      Placement(visible = true, transformation(origin = {28, 80}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Airflow.Multizone.Orifice orifice(redeclare package Medium = Air, A = 0.001)  annotation(
      Placement(visible = true, transformation(origin = {92, 64}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Fluid.MixingVolumes.MixingVolume volOutside(redeclare package Medium = Air, V = 1e10, nPorts = 1)  annotation(
      Placement(visible = true, transformation(origin = {85, 33}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.Exponential damper1(redeclare package Medium = Air, m_flow_nominal = 0.1, riseTime = 20) annotation(
    Placement(visible = true, transformation(origin = {-10, 80}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
Modelica.Blocks.Sources.Ramp ramp1(duration = 10, height = -1, offset = 1, startTime = 100)  annotation(
    Placement(visible = true, transformation(origin = {-30, 90}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
equation
  connect(airSource.ports[1], damper1.port_a) annotation(
    Line(points = {{-64, 80}, {-16, 80}, {-16, 80}, {-16, 80}}, color = {0, 127, 255}));
  connect(ramp1.y, damper1.y) annotation(
    Line(points = {{-25.6, 90}, {-17.6, 90}, {-17.6, 90}, {-9.6, 90}, {-9.6, 88}, {-9.6, 88}, {-9.6, 88}, {-9.6, 88}}, color = {0, 0, 127}));
  connect(damper1.port_b, pipe1.port_a) annotation(
    Line(points = {{-4, 80}, {24, 80}}, color = {0, 127, 255}));
  connect(orifice.port_b, volOutside.ports[1]) annotation(
    Line(points = {{96, 64}, {96, 12.5}, {85, 12.5}, {85, 24}}, color = {0, 127, 255}));
  connect(volRoom.ports[2], orifice.port_a) annotation(
    Line(points = {{68, 62}, {68, 63}, {74, 63}, {74, 63.75}, {88, 63.75}, {88, 64}}, color = {0, 127, 255}));
  connect(pipe1.port_b, volRoom.ports[1]) annotation(
    Line(points = {{32, 80}, {50, 80}, {50, 80}, {68, 80}, {68, 62}}, color = {0, 127, 255}));
end AirTest;
