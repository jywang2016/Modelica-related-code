within TestSys;

model AHU
  // Note that junction properties are given in an array(multiple ports)
  // e.g.
  // m_flow_nominal={ 0.1, 0.1,  -0.2},
  // dp_nominal =   {500,    0, -6000}
  // See: https://simulationresearch.lbl.gov/modelica/releases/latest/help/Buildings_Fluid_Movers_UsersGuide.html#Buildings.Fluid.Movers.UsersGuide
  // for Fan curves
  //extends Buildings.Fluid.Actuators.BaseClasses.ActuatorSignal;
  replaceable package Medium = Modelica.Media.Interfaces.PartialMedium "Medium in the component";
  import Modelica.Constants;
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential OA_damper(redeclare package Medium = Medium, dp(start = 100), dp_nominal = 50, m_flow(start = 0.1), m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-30, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential EA_damper(redeclare package Medium = Medium, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-30, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential SA_damper(redeclare package Medium = Medium, dp_nominal = 120, m_flow_nominal = 0.7) annotation(
    Placement(visible = true, transformation(origin = {30, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential RA_damper(redeclare package Medium = Medium, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {0, 8}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Fluid.Interfaces.FluidPort_a port_OA(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(origin = {-80, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_a port_RA(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(origin = {80, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {80, -26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_SA(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(origin = {80, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {80, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_EA(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(origin = {-80, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, -26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput y_OA "Damper postion for OA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {-30, 80}, extent = {{-20, -20}, {20, 20}}, rotation = -90), iconTransformation(origin = {-46, 86}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput y_SA "Damper postion for SA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, 80}, extent = {{-20, -20}, {20, 20}}, rotation = -90), iconTransformation(origin = {34, 86}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput y_EA "Damper postion for EA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {-30, -60}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-44, -86}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Modelica.Blocks.Interfaces.RealInput y_RA "Damper postion for RA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, -60}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {26, -30}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Buildings.Fluid.Movers.FlowControlled_dp fanOA(redeclare package Medium = Medium, dp(start = 2000), dp_nominal = 1000, m_flow(start = 0.1), m_flow_nominal = 1, per.pressure(V_flow = {0.0003, 1, 2}, dp = {3500, 3000, 10})) annotation(
    Placement(visible = true, transformation(origin = {-58, 40}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_dp fanRA(redeclare package Medium = Medium, dp(start = 2000), dp_nominal = 1000, m_flow(start = 0.1), m_flow_nominal = 1, per.pressure(V_flow = {0.0003, 1, 2}, dp = {3500, 3000, 10})) annotation(
    Placement(visible = true, transformation(origin = {46, -20}, extent = {{-8, -8}, {8, 8}}, rotation = 180)));
  Buildings.Fluid.FixedResistances.Junction jun(redeclare package Medium = Medium, dp_nominal = {30, -30, -30}, m_flow_nominal = {1, -0.5, -0.5}) annotation(
    Placement(visible = true, transformation(origin = {-8.88178e-16, -20}, extent = {{-8, -8}, {8, 8}}, rotation = 180)));
  Modelica.Blocks.Interfaces.RealInput y_fanOA "Pressure rise for fanOA" annotation(
    Placement(visible = true, transformation(origin = {-59, 77}, extent = {{-11, -11}, {11, 11}}, rotation = -90), iconTransformation(origin = {-76, 80}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput y_fanRA "Pressure rise for fanRA" annotation(
    Placement(visible = true, transformation(origin = {68, -56}, extent = {{-12, -12}, {12, 12}}, rotation = 90), iconTransformation(origin = {80, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
equation
  connect(y_fanRA, fanRA.dp_in) annotation(
    Line(points = {{68, -56}, {46, -56}, {46, -30}, {46, -30}}, color = {0, 0, 127}));
  connect(y_fanOA, fanOA.dp_in) annotation(
    Line(points = {{-58, 78}, {-58, 78}, {-58, 50}, {-58, 50}}, color = {0, 0, 127}));
  connect(jun.port_2, EA_damper.port_a) annotation(
    Line(points = {{-8, -20}, {-20, -20}, {-20, -20}, {-20, -20}}, color = {0, 127, 255}));
  connect(jun.port_3, RA_damper.port_a) annotation(
    Line(points = {{0, -12}, {0, -12}, {0, -2}, {0, -2}}, color = {0, 127, 255}));
  connect(jun.port_1, fanRA.port_b) annotation(
    Line(points = {{8, -20}, {38, -20}, {38, -20}, {38, -20}}, color = {0, 127, 255}));
  connect(fanRA.port_a, port_RA) annotation(
    Line(points = {{54, -20}, {78, -20}, {78, -20}, {80, -20}}, color = {0, 127, 255}));
  connect(fanOA.port_b, OA_damper.port_a) annotation(
    Line(points = {{-50, 40}, {-40, 40}, {-40, 40}, {-40, 40}}, color = {0, 127, 255}));
  connect(port_OA, fanOA.port_a) annotation(
    Line(points = {{-80, 40}, {-66, 40}, {-66, 40}, {-66, 40}}));
  connect(RA_damper.port_b, SA_damper.port_a) annotation(
    Line(points = {{0, 18}, {0, 18}, {0, 40}, {20, 40}, {20, 40}}, color = {0, 127, 255}));
  connect(y_RA, RA_damper.y) annotation(
    Line(points = {{30, -60}, {30, -46}, {-12, -46}, {-12, 8}}, color = {0, 0, 127}));
  connect(y_EA, EA_damper.y) annotation(
    Line(points = {{-30, -60}, {-30, -60}, {-30, -32}, {-30, -32}}, color = {0, 0, 127}));
  connect(y_SA, SA_damper.y) annotation(
    Line(points = {{30, 80}, {30, 80}, {30, 52}, {30, 52}}, color = {0, 0, 127}));
  connect(y_OA, OA_damper.y) annotation(
    Line(points = {{-30, 80}, {-30, 80}, {-30, 52}, {-30, 52}}, color = {0, 0, 127}));
  connect(EA_damper.port_b, port_EA) annotation(
    Line(points = {{-40, -20}, {-78, -20}, {-78, -20}, {-80, -20}}, color = {0, 127, 255}));
  connect(SA_damper.port_b, port_SA) annotation(
    Line(points = {{40, 40}, {80, 40}, {80, 40}, {80, 40}}, color = {0, 127, 255}));
  connect(OA_damper.port_b, SA_damper.port_a) annotation(
    Line(points = {{-20, 40}, {20, 40}, {20, 40}, {20, 40}}, color = {0, 127, 255}));
  annotation(
    Icon(graphics = {Line(origin = {0, 4}, points = {{-80, 40}, {80, 40}, {80, 20}, {10, 20}, {10, -20}, {80, -20}, {80, -40}, {-80, -40}, {-80, -20}, {-6, -20}, {-6, 20}, {-80, 20}, {-80, 40}}, thickness = 1.5), Rectangle(origin = {-30, 41}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {48, 41}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {-26, -21}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {14, 7}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {34, 59}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Rectangle(origin = {-44, -51}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Rectangle(origin = {-48, 59}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Text(origin = {-43, -51}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Text(origin = {-47, 59}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Text(origin = {35, 59}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Rectangle(origin = {24, 3}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Text(origin = {25, 3}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Text(origin = {-75, 51}, extent = {{-25, 29}, {11, -11}}, textString = "OA"), Text(origin = {82, 55}, extent = {{-22, 21}, {14, -11}}, textString = "SA"), Text(origin = {80, -6}, extent = {{-20, 30}, {14, -18}}, textString = "RA"), Text(origin = {-80, -1}, extent = {{-18, 21}, {18, -21}}, textString = "EA"), Text(origin = {-84, 94}, extent = {{-12, 6}, {12, -6}}, textString = "fanOA"), Text(origin = {64, -92}, extent = {{-12, 6}, {12, -6}}, textString = "fanRA")}, coordinateSystem(initialScale = 0.1)));
end AHU;
