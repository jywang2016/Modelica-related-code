within TestSys;

// Note the input for the fans are "pressure rise", choose the fan/pump type carefully!

model AHUTest
  package Air = Buildings.Media.Air;
  AHU ahu1(redeclare package Medium=Air) annotation(
    Placement(visible = true, transformation(origin = {0, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.FixedBoundary EA(redeclare package Medium=Air, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-52, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant constOA(k = 0.8)  annotation(
    Placement(visible = true, transformation(origin = {-32, 48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.MixingVolumes.MixingVolume vol(redeclare package Medium=Air, V = 5, m_flow_nominal = 1, nPorts = 2)  annotation(
    Placement(visible = true, transformation(origin = {54, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Ramp pressure_rise(duration = 1, height = 1000)  annotation(
    Placement(visible = true, transformation(origin = {-22, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.Boundary_pT OA(redeclare package Medium=Air, T = 273.15 + 18, nPorts = 1, p = 101325)  annotation(
    Placement(visible = true, transformation(origin = {-56, 12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(OA.ports[1], ahu1.port_OA) annotation(
    Line(points = {{-46, 12}, {-26, 12}, {-26, 2}, {-8, 2}, {-8, 2}}, color = {0, 127, 255}));
  connect(ahu1.port_EA, EA.ports[1]) annotation(
    Line(points = {{-8, -4}, {-26, -4}, {-26, -24}, {-42, -24}, {-42, -24}}, color = {0, 127, 255}));
  connect(vol.ports[2], ahu1.port_RA) annotation(
    Line(points = {{44, 0}, {28, 0}, {28, -4}, {8, -4}, {8, -4}}, color = {0, 127, 255}));
  connect(pressure_rise.y, ahu1.y_fanOA) annotation(
    Line(points = {{-10, -44}, {-12, -44}, {-12, 6}, {-8, 6}, {-8, 6}}, color = {0, 0, 127}));
  connect(pressure_rise.y, ahu1.y_fanRA) annotation(
    Line(points = {{-10, -44}, {6, -44}, {6, -10}, {6, -10}}, color = {0, 0, 127}));
  connect(ahu1.port_SA, vol.ports[1]) annotation(
    Line(points = {{8, 2}, {44, 2}, {44, 0}, {44, 0}}, color = {0, 127, 255}));
  connect(constOA.y, ahu1.y_RA) annotation(
    Line(points = {{-20, 48}, {12, 48}, {12, -12}, {2, -12}, {2, -4}, {2, -4}}, color = {0, 0, 127}));
  connect(constOA.y, ahu1.y_EA) annotation(
    Line(points = {{-20, 48}, {-18, 48}, {-18, -12}, {-4, -12}, {-4, -10}}, color = {0, 0, 127}));
  connect(constOA.y, ahu1.y_SA) annotation(
    Line(points = {{-20, 48}, {4, 48}, {4, 6}, {4, 6}}, color = {0, 0, 127}));
  connect(constOA.y, ahu1.y_OA) annotation(
    Line(points = {{-20, 48}, {-4, 48}, {-4, 6}, {-4, 6}}, color = {0, 0, 127}));
end AHUTest;
