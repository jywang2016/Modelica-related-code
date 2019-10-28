within TestSys;

model ControlUnitType2Test
  Modelica.Blocks.Sources.Sine sine1(amplitude = 10, freqHz = 0.01, offset = 273.15 + 20)  annotation(
    Placement(visible = true, transformation(origin = {-58, 56}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 100, height = 10, offset = 273.15 + 15)  annotation(
    Placement(visible = true, transformation(origin = {-64, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const1(k = 273.15 + 22)  annotation(
    Placement(visible = true, transformation(origin = {-62, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 273.15 + 20)  annotation(
    Placement(visible = true, transformation(origin = {-56, -42}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  ControlUnitType2 controlUnitType2 annotation(
    Placement(visible = true, transformation(origin = {11, 5}, extent = {{-25, -25}, {25, 25}}, rotation = 0)));
equation
  connect(sine1.y, controlUnitType2.uSAT) annotation(
    Line(points = {{-46, 56}, {-40, 56}, {-40, -2}, {-4, -2}, {-4, -2}}, color = {0, 0, 127}));
  connect(sine1.y, controlUnitType2.uOAT) annotation(
    Line(points = {{-46, 56}, {-26, 56}, {-26, 24}, {-4, 24}, {-4, 24}}, color = {0, 0, 127}));
  connect(ramp1.y, controlUnitType2.uRAT) annotation(
    Line(points = {{-52, 26}, {-36, 26}, {-36, 12}, {-4, 12}, {-4, 12}}, color = {0, 0, 127}));
  connect(const.y, controlUnitType2.uSP) annotation(
    Line(points = {{-44, -42}, {-26, -42}, {-26, -16}, {-4, -16}, {-4, -14}}, color = {0, 0, 127}));
end ControlUnitType2Test;
