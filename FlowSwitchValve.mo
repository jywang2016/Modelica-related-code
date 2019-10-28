within TestSys;

model FlowSwitchValve "Switching valve that determines which outlet(s) the flow goes"
  replaceable package Medium = Modelica.Media.Interfaces.PartialMedium "Medium in the component";
  parameter Real m_flow_nominal_val1 = 0.05 "Nomial flow rate N.C. valve";
  parameter Real m_flow_nominal_val2 = 0.95 "Nomial flow rate N.O. valve";
  parameter Modelica.SIunits.MassFlowRate m_flow_nominal_jun[3] ={1,-0.5,-0.5} "Nomial flow rate for junction e.g. {1,0.5,0.5}";
  parameter Modelica.SIunits.Pressure dp_nominal_jun[3] ={30,-30,-30} "Nomial dp for junction e.g. {1,0.5,0.5}";
  Buildings.Fluid.Actuators.Valves.TwoWayLinear val1(redeclare package Medium = Medium, dpValve_nominal = 100, m_flow_nominal = 1) "Normally Closed Valve(closed when input is 0)" annotation(
    Placement(visible = true, transformation(origin = {0, 20}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Valves.TwoWayLinear val2(redeclare package Medium = Medium, dpValve_nominal = 100, m_flow_nominal = 1) "Normally Openned Valve(openned when signal is 0)" annotation(
    Placement(visible = true, transformation(origin = {0, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput u "Valve input signal(0-1)" annotation(
    Placement(visible = true, transformation(origin = {0, 74}, extent = {{-14, -14}, {14, 14}}, rotation = -90), iconTransformation(origin = {-6.66134e-16, 80}, extent = {{-14, -14}, {14, 14}}, rotation = -90)));
  Modelica.Fluid.Interfaces.FluidPort_a port_a(redeclare package Medium = Medium) "Always Open port" annotation(
    Placement(visible = true, transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_b1(redeclare package Medium = Medium) "Normally Closed port" annotation(
    Placement(visible = true, transformation(origin = {60, 20}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {60, 50}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_b2(redeclare package Medium = Medium) "Normally Openned port" annotation(
    Placement(visible = true, transformation(origin = {60, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {60, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction jun(redeclare package Medium = Medium, dp_nominal = {30, -30, -30}, m_flow_nominal = {1, -0.5, -0.5}) annotation(
    Placement(visible = true, transformation(origin = {-54, 0}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Modelica.Blocks.Math.Add add1(k2 = -1) annotation(
    Placement(visible = true, transformation(origin = {34, 44}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Constant const(k = 1) annotation(
    Placement(visible = true, transformation(origin = {58, 66}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
equation
  connect(add1.y, val2.y) annotation(
    Line(points = {{34, 32}, {34, 32}, {34, 0}, {0, 0}, {0, -8}, {0, -8}}, color = {0, 0, 127}));
  connect(const.y, add1.u1) annotation(
    Line(points = {{46, 66}, {40, 66}, {40, 56}, {40, 56}}, color = {0, 0, 127}));
  connect(u, add1.u2) annotation(
    Line(points = {{0, 74}, {28, 74}, {28, 56}, {28, 56}}, color = {0, 0, 127}));
  connect(port_a, jun.port_1) annotation(
    Line(points = {{-80, 0}, {-64, 0}, {-64, 0}, {-64, 0}}));
  connect(val1.port_b, port_b1) annotation(
    Line(points = {{10, 20}, {60, 20}, {60, 20}, {60, 20}}, color = {0, 127, 255}));
  connect(jun.port_3, val1.port_a) annotation(
    Line(points = {{-54, 10}, {-54, 10}, {-54, 20}, {-10, 20}, {-10, 20}}, color = {0, 127, 255}));
  connect(val2.port_b, port_b2) annotation(
    Line(points = {{10, -20}, {60, -20}, {60, -20}, {60, -20}}, color = {0, 127, 255}));
  connect(jun.port_2, val2.port_a) annotation(
    Line(points = {{-44, 0}, {-36, 0}, {-36, -20}, {-10, -20}, {-10, -20}}, color = {0, 127, 255}));
  connect(u, val1.y) annotation(
    Line(points = {{0, 74}, {0, 74}, {0, 32}, {0, 32}}, color = {0, 0, 127}));
// Name for component: annotation>Icon>graphics{}
  annotation(
    defaultComponentName = "swVal",
    Icon(graphics = {Rectangle(origin = {-40, 0}, fillColor = {85, 170, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-34, 8}, {34, -8}}), Rectangle(origin = {24, 50}, fillColor = {85, 170, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-30, 8}, {30, -8}}), Rectangle(origin = {26, -50}, fillColor = {85, 170, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-32, 8}, {32, -8}}), Rectangle(origin = {1, -1}, fillColor = {85, 170, 255}, pattern = LinePattern.None, fillPattern = FillPattern.VerticalCylinder, extent = {{-13, 61}, {13, -59}}), Polygon(origin = {6, 0}, fillColor = {120, 120, 120}, fillPattern = FillPattern.Solid, lineThickness = 1, points = {{-18, 14}, {8, -14}, {8, 14}, {-18, -14}, {-18, -14}, {-18, 14}}), Text(origin = {40, 29}, extent = {{-26, 15}, {26, -15}}, textString = "N.C."), Text(origin = {42, -27}, extent = {{-26, 15}, {26, -15}}, textString = "N.O."), Text(extent = {{-150, 150}, {150, 110}}, textString = "%name", lineColor = {0, 0, 255})}, coordinateSystem(initialScale = 0.1)));
end FlowSwitchValve;
