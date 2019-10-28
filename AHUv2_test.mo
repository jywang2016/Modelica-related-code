within TestSys;

model AHUv2_test
  // Note the input for the fans are "pressure rise", choose the fan/pump type carefully!
  package Air = Buildings.Media.Air "Medium air";
  package water = Buildings.Media.Water "Medium water";
  AHUv2 ahu1(redeclare package Medium1 = Air, redeclare package Medium2 = water) annotation(
    Placement(visible = true, transformation(origin = {0, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.FixedBoundary EA(redeclare package Medium = Air, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {-56, -14}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant constOA(k = 0.8) annotation(
    Placement(visible = true, transformation(origin = {-32, 48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.MixingVolumes.MixingVolume vol(redeclare package Medium = Air, V = 5, m_flow_nominal = 1, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {54, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Ramp pressure_rise(duration = 1, height = 1000) annotation(
    Placement(visible = true, transformation(origin = {-22, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT OA(redeclare package Medium = Air, T = 273.15 + 18, nPorts = 1, p = 101325) annotation(
    Placement(visible = true, transformation(origin = {-56, 12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Sine sine1(amplitude = 0.2, freqHz = 1 / 500, offset = 0.8) annotation(
    Placement(visible = true, transformation(origin = {-74, -78}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Cosine cosine1(amplitude = 0.4, freqHz = 1 / 300, offset = 0.5) annotation(
    Placement(visible = true, transformation(origin = {48, -78}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT CSource(redeclare package Medium = water, T = 273.15 + 8, nPorts = 1, p = 101315 * 1.2) annotation(
    Placement(visible = true, transformation(origin = {86, -22}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.FixedBoundary water_sink(redeclare package Medium = water, nPorts = 2) annotation(
    Placement(visible = true, transformation(origin = {4, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Buildings.Fluid.Sources.Boundary_pT HSource(redeclare package Medium = water, T = 273.15 + 90, nPorts = 1, p = 101315 * 1.5) annotation(
    Placement(visible = true, transformation(origin = {-86, -28}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(cosine1.y, ahu1.uCoolWater) annotation(
    Line(points = {{38, -78}, {24, -78}, {24, -6}, {10, -6}, {10, -6}}, color = {0, 0, 127}));
  connect(HSource.ports[1], ahu1.port_HW_in) annotation(
    Line(points = {{-76, -28}, {-14, -28}, {-14, -8}, {-8, -8}, {-8, -8}}, color = {0, 127, 255}));
  connect(ahu1.port_HW_out, water_sink.ports[1]) annotation(
    Line(points = {{-8, -10}, {-8, -10}, {-8, -58}, {4, -58}, {4, -58}}, color = {0, 127, 255}));
  connect(ahu1.port_CW_out, water_sink.ports[2]) annotation(
    Line(points = {{10, -10}, {10, -10}, {10, -58}, {4, -58}, {4, -58}}, color = {0, 127, 255}));
  connect(CSource.ports[1], ahu1.port_CW_in) annotation(
    Line(points = {{76, -22}, {20, -22}, {20, -8}, {10, -8}, {10, -8}}, color = {0, 127, 255}));
  connect(sine1.y, ahu1.uHotWater) annotation(
    Line(points = {{-62, -78}, {-36, -78}, {-36, -6}, {-10, -6}, {-10, -6}}, color = {0, 0, 127}));
  connect(constOA.y, ahu1.y_RA) annotation(
    Line(points = {{-20, 48}, {14, 48}, {14, -20}, {4, -20}, {4, -4}, {2, -4}}, color = {0, 0, 127}));
  connect(pressure_rise.y, ahu1.y_fanRA) annotation(
    Line(points = {{-10, -44}, {6, -44}, {6, -12}, {2, -12}, {2, -10}}, color = {0, 0, 127}));
  connect(ahu1.port_EA, EA.ports[1]) annotation(
    Line(points = {{-8, -4}, {-26, -4}, {-26, -14}, {-46, -14}}, color = {0, 127, 255}));
  connect(OA.ports[1], ahu1.port_OA) annotation(
    Line(points = {{-46, 12}, {-26, 12}, {-26, 2}, {-8, 2}, {-8, 2}}, color = {0, 127, 255}));
  connect(vol.ports[2], ahu1.port_RA) annotation(
    Line(points = {{44, 0}, {28, 0}, {28, -4}, {8, -4}, {8, -4}}, color = {0, 127, 255}));
  connect(pressure_rise.y, ahu1.y_fanOA) annotation(
    Line(points = {{-10, -44}, {-12, -44}, {-12, 6}, {-8, 6}, {-8, 6}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, vol.ports[1]) annotation(
    Line(points = {{8, 2}, {44, 2}, {44, 0}, {44, 0}}, color = {0, 127, 255}));
  connect(constOA.y, ahu1.y_EA) annotation(
    Line(points = {{-20, 48}, {-18, 48}, {-18, -12}, {-4, -12}, {-4, -10}}, color = {0, 0, 127}));
  connect(constOA.y, ahu1.y_SA) annotation(
    Line(points = {{-20, 48}, {4, 48}, {4, 6}, {4, 6}}, color = {0, 0, 127}));
  connect(constOA.y, ahu1.y_OA) annotation(
    Line(points = {{-20, 48}, {-4, 48}, {-4, 6}, {-4, 6}}, color = {0, 0, 127}));
end AHUv2_test;
