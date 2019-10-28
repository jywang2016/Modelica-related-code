within TestSys;

model AirTest_b
  package Air = Buildings.Media.Air;
  Buildings.Fluid.MixingVolumes.MixingVolume volRoom(redeclare package Medium = Air, T_start = 300, V = 3 * 3 * 3, m_flow_nominal = 1, nPorts = 3, p_start = 101300) annotation(
    Placement(visible = true, transformation(origin = {55, 62}, extent = {{-12, -13}, {12, 13}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT outsideAir(redeclare package Medium = Air, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {-84, 40}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient = 283.15, m_flow_start = 0.1) annotation(
    Placement(visible = true, transformation(origin = {-18, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Airflow.Multizone.Orifice orifice(redeclare package Medium = Air, A = 0.001) annotation(
    Placement(visible = true, transformation(origin = {92, 64}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Fluid.MixingVolumes.MixingVolume volOutside(redeclare package Medium = Air, V = 1e10, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {85, 33}, extent = {{-9, -9}, {9, 9}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.Exponential damper1(redeclare package Medium = Air, m_flow_nominal = 0.1, riseTime = 20) annotation(
    Placement(visible = true, transformation(origin = {56, 90}, extent = {{-6, -6}, {6, 6}}, rotation = 270)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 10, height = 0.9, offset = 0.1, startTime = 100) annotation(
    Placement(visible = true, transformation(origin = {74, 84}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_dp fan1(redeclare package Medium = Air, inputType = Buildings.Fluid.Types.InputType.Continuous, m_flow_nominal = 0.1, nominalValuesDefineDefaultPressureCurve = true) annotation(
    Placement(visible = true, transformation(origin = {-4, 76}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Sources.Step step1(startTime = 20) annotation(
    Placement(visible = true, transformation(origin = {-20, 94}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Pipes.StaticPipe pipe1(redeclare package Medium = Air, diameter = 0.2, length = 10) annotation(
    Placement(visible = true, transformation(origin = {22, 86}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Math.Gain gain1(k = 1000) annotation(
    Placement(visible = true, transformation(origin = {-8, 94}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_dp fan2(redeclare package Medium = Air, m_flow_nominal = 0.1, nominalValuesDefineDefaultPressureCurve = true)  annotation(
    Placement(visible = true, transformation(origin = {48, -12}, extent = {{-6, -6}, {6, 6}}, rotation = 180)));
  Modelica.Blocks.Sources.Step step2(startTime = 40)  annotation(
    Placement(visible = true, transformation(origin = {18, -32}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Math.Gain gain2(k = 1000)  annotation(
    Placement(visible = true, transformation(origin = {34, -32}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Pipes.StaticPipe pipe2(redeclare package Medium = Air, diameter = 0.2, length = 5)  annotation(
    Placement(visible = true, transformation(origin = {14, -12}, extent = {{-4, -4}, {4, 4}}, rotation = 180)));
  Buildings.Fluid.Actuators.Dampers.MixingBox mixingBox(redeclare package Medium = Air, dpExh_nominal = 100, dpOut_nominal = 100, dpRec_nominal = 100, dp_nominalIncludesDamper = false, mExh_flow_nominal = 0.1, mOut_flow_nominal = 0.1, mRec_flow_nominal = 0.1) annotation(
    Placement(visible = true, transformation(origin = {-46, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp2(duration = 10, height = 0.4, offset = 0.1)  annotation(
    Placement(visible = true, transformation(origin = {-58, 54}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
equation
  connect(ramp2.y, mixingBox.y) annotation(
    Line(points = {{-54, 54}, {-46, 54}, {-46, 46}, {-46, 46}}, color = {0, 0, 127}));
  connect(mixingBox.port_Sup, fan1.port_a) annotation(
    Line(points = {{-36, 40}, {-36, 40}, {-36, 76}, {-10, 76}, {-10, 76}}, color = {0, 127, 255}));
  connect(outsideAir.ports[2], mixingBox.port_Exh) annotation(
    Line(points = {{-76, 40}, {-76, 40}, {-76, 28}, {-56, 28}, {-56, 28}}, color = {0, 127, 255}));
  connect(outsideAir.ports[1], mixingBox.port_Out) annotation(
    Line(points = {{-76, 40}, {-56, 40}}, color = {0, 127, 255}));
  connect(pipe2.port_b, mixingBox.port_Ret) annotation(
    Line(points = {{10, -12}, {-21, -12}, {-21, 28}, {-36, 28}}, color = {0, 127, 255}));
  connect(fan2.port_b, pipe2.port_a) annotation(
    Line(points = {{42, -12}, {18, -12}}, color = {0, 127, 255}));
  connect(volRoom.ports[3], fan2.port_a) annotation(
    Line(points = {{68, 62}, {68, 25.5}, {54, 25.5}, {54, -12}}, color = {0, 127, 255}));
  connect(gain2.y, fan2.dp_in) annotation(
    Line(points = {{38, -32}, {48, -32}, {48, -19}}, color = {0, 0, 127}));
  connect(step2.y, gain2.u) annotation(
    Line(points = {{22, -32}, {28, -32}, {28, -32}, {30, -32}}, color = {0, 0, 127}));
  connect(fan1.port_b, pipe1.port_a) annotation(
    Line(points = {{2, 76}, {12, 76}, {12, 86}, {18, 86}}, color = {0, 127, 255}));
  connect(damper1.port_b, volRoom.ports[1]) annotation(
    Line(points = {{56, 84}, {68, 84}, {68, 62}, {68, 62}}, color = {0, 127, 255}));
  connect(pipe1.port_b, damper1.port_a) annotation(
    Line(points = {{26, 86}, {40, 86}, {40, 96}, {56, 96}}, color = {0, 127, 255}));
  connect(ramp1.y, damper1.y) annotation(
    Line(points = {{78, 84}, {70.5, 84}, {70.5, 90}, {63, 90}}, color = {0, 0, 127}));
  connect(gain1.y, fan1.dp_in) annotation(
    Line(points = {{-3.6, 94}, {-3.6, 94}, {-3.6, 84}, {-3.6, 84}}, color = {0, 0, 127}));
  connect(step1.y, gain1.u) annotation(
    Line(points = {{-15.6, 94}, {-13.6, 94}, {-13.6, 94}, {-11.6, 94}}, color = {0, 0, 127}));
  connect(orifice.port_b, volOutside.ports[1]) annotation(
    Line(points = {{96, 64}, {96, 12.5}, {85, 12.5}, {85, 24}}, color = {0, 127, 255}));
  connect(volRoom.ports[2], orifice.port_a) annotation(
    Line(points = {{68, 62}, {68, 63}, {74, 63}, {74, 63.75}, {88, 63.75}, {88, 64}}, color = {0, 127, 255}));
end AirTest_b;
