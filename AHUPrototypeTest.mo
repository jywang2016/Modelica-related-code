within TestSys;




model AHUPrototypeTest

  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential dampOA(redeclare package Medium = Air, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-22, 36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential dampSA(redeclare package Medium = Air, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {20, 36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential dampRA(redeclare package Medium = Air, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {0, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential dampEA(redeclare package Medium = Air, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-22, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Constant const(k = 0.8)  annotation(
    Placement(visible = true, transformation(origin = {-50, 74}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT OA(redeclare package Medium=Air,T = 273.15 + 18, nPorts = 1, p = 101325)  annotation(
    Placement(visible = true, transformation(origin = {-76, 36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.FixedBoundary EA(redeclare package Medium=Air,nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-76, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.MixingVolumes.MixingVolume vol(redeclare package Medium = Air,V = 5, m_flow_nominal = 0.5, nPorts = 2)  annotation(
    Placement(visible = true, transformation(origin = {72, 16}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Buildings.Fluid.FixedResistances.Junction jun(redeclare package Medium = Air, dp_nominal = {50, -50, -50}, m_flow_nominal = {0.8, -0.4, -0.4})  annotation(
    Placement(visible = true, transformation(origin = {14, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Movers.FlowControlled_dp fanRA(redeclare package Medium = Air, dp_nominal = 1000, m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {50, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Ramp pressure_rise(duration = 1, height = 1000)  annotation(
    Placement(visible = true, transformation(origin = {-76, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_dp fanOA(redeclare package Medium = Air, dp_nominal = 1000, m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {-52, 36}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
equation
  connect(pressure_rise.y, fanOA.dp_in) annotation(
    Line(points = {{-64, -68}, {-60, -68}, {-60, 44}, {-52, 44}, {-52, 44}}, color = {0, 0, 127}));
  connect(fanOA.port_b, dampOA.port_a) annotation(
    Line(points = {{-46, 36}, {-32, 36}, {-32, 36}, {-32, 36}}, color = {0, 127, 255}));
  connect(OA.ports[1], fanOA.port_a) annotation(
    Line(points = {{-66, 36}, {-58, 36}, {-58, 36}, {-58, 36}}, color = {0, 127, 255}));
  connect(pressure_rise.y, fanRA.dp_in) annotation(
    Line(points = {{-65, -68}, {50, -68}, {50, -42}}, color = {0, 0, 127}));
  connect(fanRA.port_b, jun.port_1) annotation(
    Line(points = {{40, -30}, {24, -30}, {24, -30}, {24, -30}}, color = {0, 127, 255}));
  connect(vol.ports[2], fanRA.port_a) annotation(
    Line(points = {{62, 16}, {60, 16}, {60, -30}, {60, -30}}, color = {0, 127, 255}));
  connect(jun.port_3, dampRA.port_a) annotation(
    Line(points = {{14, -20}, {0, -20}, {0, -8}, {0, -8}}, color = {0, 127, 255}));
  connect(jun.port_2, dampEA.port_a) annotation(
    Line(points = {{4, -30}, {-12, -30}, {-12, -30}, {-12, -30}}, color = {0, 127, 255}));
  connect(const.y, dampRA.y) annotation(
    Line(points = {{-38, 74}, {-34, 74}, {-34, 2}, {-12, 2}}, color = {0, 0, 127}));
  connect(dampRA.port_b, dampSA.port_a) annotation(
    Line(points = {{0, 12}, {0, 23}, {10, 23}, {10, 36}}, color = {0, 127, 255}));
  connect(dampSA.port_b, vol.ports[1]) annotation(
    Line(points = {{30, 36}, {62, 36}, {62, 16}, {62, 16}}, color = {0, 127, 255}));
  connect(dampEA.port_b, EA.ports[1]) annotation(
    Line(points = {{-32, -30}, {-66, -30}, {-66, -30}, {-66, -30}}, color = {0, 127, 255}));
  connect(const.y, dampEA.y) annotation(
    Line(points = {{-38, 74}, {-38, 74}, {-38, -44}, {-22, -44}, {-22, -42}}, color = {0, 0, 127}));
  connect(const.y, dampSA.y) annotation(
    Line(points = {{-38, 74}, {20, 74}, {20, 48}, {20, 48}}, color = {0, 0, 127}));
  connect(const.y, dampOA.y) annotation(
    Line(points = {{-38, 74}, {-22, 74}, {-22, 48}, {-22, 48}}, color = {0, 0, 127}));
  connect(dampOA.port_b, dampSA.port_a) annotation(
    Line(points = {{-12, 36}, {10, 36}, {10, 36}, {10, 36}}, color = {0, 127, 255}));
end AHUPrototypeTest;
