within TestSys;

model ControlUnitTest
  TestSys.ControlUnit controlUnit1 annotation(
    Placement(visible = true, transformation(origin = {1, -1}, extent = {{-25, -25}, {25, 25}}, rotation = 0)));
  Modelica.Blocks.Sources.Sine sine1(amplitude = 10, freqHz = 0.01, offset = 273.15 + 20)  annotation(
    Placement(visible = true, transformation(origin = {-58, 56}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 100, height = 10, offset = 273.15 + 15)  annotation(
    Placement(visible = true, transformation(origin = {-64, 12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp2(duration = 1, offset = 273.15 + 20)  annotation(
    Placement(visible = true, transformation(origin = {-64, -26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(ramp2.y, controlUnit1.uSAT) annotation(
    Line(points = {{-52, -26}, {-30, -26}, {-30, -8}, {-14, -8}, {-14, -8}}, color = {0, 0, 127}));
  connect(sine1.y, controlUnit1.uOAT) annotation(
    Line(points = {{-46, 56}, {-26, 56}, {-26, 18}, {-14, 18}, {-14, 18}}, color = {0, 0, 127}));
  connect(ramp1.y, controlUnit1.uRAT) annotation(
    Line(points = {{-52, 12}, {-30, 12}, {-30, 6}, {-14, 6}, {-14, 6}}, color = {0, 0, 127}));
end ControlUnitTest;
