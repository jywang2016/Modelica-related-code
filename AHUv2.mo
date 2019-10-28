within TestSys;

model AHUv2
  // AHUv2:
  // add in heat exchangers(with efficiency options) and hot/cool water ports 
  // 
  
  // Note that junction properties are given in an array(multiple ports)
  // e.g.
  // m_flow_nominal={ 0.1, 0.1,  -0.2},
  // dp_nominal =   {500,    0, -6000}
  // See: https://simulationresearch.lbl.gov/modelica/releases/latest/help/Buildings_Fluid_Movers_UsersGuide.html#Buildings.Fluid.Movers.UsersGuide
  // for Fan curves
  //extends Buildings.Fluid.Actuators.BaseClasses.ActuatorSignal;
  
  parameter Real hex_H_eps = 0.8 "hot water heat exchanger efficiency(0-1)";
  parameter Real hex_C_eps = 0.8 "cold water heat exchanger efficiency(0-1)";
  
  replaceable package Medium1 = Modelica.Media.Interfaces.PartialMedium "Medium in the component";
  // air
  replaceable package Medium2 = Modelica.Media.Interfaces.PartialMedium "Medium in the component";
  // water
  import Modelica.Constants;
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential OA_damper(redeclare package Medium = Medium1, dp(start = 100), dp_nominal = 50, m_flow(start = 0.1), m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-28, -12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential EA_damper(redeclare package Medium = Medium1, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-28, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential SA_damper(redeclare package Medium = Medium1, dp_nominal = 120, m_flow_nominal = 0.7) annotation(
    Placement(visible = true, transformation(origin = {32, -12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Actuators.Dampers.VAVBoxExponential RA_damper(redeclare package Medium = Medium1, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {2, -26}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Fluid.Interfaces.FluidPort_a port_OA(redeclare package Medium = Medium1) annotation(
    Placement(visible = true, transformation(origin = {-78, -12}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_a port_RA(redeclare package Medium = Medium1) annotation(
    Placement(visible = true, transformation(origin = {82, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {80, -26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_SA(redeclare package Medium = Medium1) annotation(
    Placement(visible = true, transformation(origin = {82, -12}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {80, 34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_EA(redeclare package Medium = Medium1) annotation(
    Placement(visible = true, transformation(origin = {-78, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, -26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput y_SA "Damper postion for SA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {32, 28}, extent = {{-20, -20}, {20, 20}}, rotation = -90), iconTransformation(origin = {34, 86}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput y_EA "Damper postion for EA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {-28, -90}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {-44, -86}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Modelica.Blocks.Interfaces.RealInput y_RA "Damper postion for RA_damper(0-1)" annotation(
    Placement(visible = true, transformation(origin = {32, -90}, extent = {{-20, -20}, {20, 20}}, rotation = 90), iconTransformation(origin = {26, -30}, extent = {{-20, -20}, {20, 20}}, rotation = 90)));
  Buildings.Fluid.Movers.FlowControlled_dp fanOA(redeclare package Medium = Medium1, dp(start = 2000), dp_nominal = 1000, m_flow(start = 0.1), m_flow_nominal = 1, per.pressure(V_flow = {0.0003, 1, 2}, dp = {3500, 3000, 10})) annotation(
    Placement(visible = true, transformation(origin = {-56, -12}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_dp fanRA(redeclare package Medium = Medium1, dp(start = 2000), dp_nominal = 1000, m_flow(start = 0.1), m_flow_nominal = 1, per.pressure(V_flow = {0.0003, 1, 2}, dp = {3500, 3000, 10})) annotation(
    Placement(visible = true, transformation(origin = {48, -50}, extent = {{-8, -8}, {8, 8}}, rotation = 180)));
  Buildings.Fluid.FixedResistances.Junction jun(redeclare package Medium = Medium1, dp_nominal = {30, -30, -30}, m_flow_nominal = {1, -0.5, -0.5}) annotation(
    Placement(visible = true, transformation(origin = {2, -50}, extent = {{-8, -8}, {8, 8}}, rotation = 180)));
  Modelica.Blocks.Interfaces.RealInput y_fanOA "Pressure rise for fanOA" annotation(
    Placement(visible = true, transformation(origin = {-57, 25}, extent = {{-11, -11}, {11, 11}}, rotation = -90), iconTransformation(origin = {-76, 80}, extent = {{-8, -8}, {8, 8}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput y_fanRA "Pressure rise for fanRA" annotation(
    Placement(visible = true, transformation(origin = {70, -86}, extent = {{-12, -12}, {12, 12}}, rotation = 90), iconTransformation(origin = {10, -88}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexHot(redeclare package Medium1 = Medium1, redeclare package Medium2 = Medium2, dp1_nominal = 100, dp2_nominal = 100, eps = hex_H_eps, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {-30, 74}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.ConstantEffectiveness hexCool(redeclare package Medium1 = Medium1, redeclare package Medium2 = Medium2, dp1_nominal = 100, dp2_nominal = 100, eps = hex_C_eps, m1_flow_nominal = 1, m2_flow_nominal = 1) annotation(
    Placement(visible = true, transformation(origin = {60, 74}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  TestSys.FlowSwitchValve swValHotWater(redeclare package Medium = Medium1, m_flow_nominal_val1 = 0.1, m_flow_nominal_val2 = 0.9) annotation(
    Placement(visible = true, transformation(origin = {-66, 84}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  TestSys.FlowSwitchValve swValCoolWater(redeclare package Medium = Medium1, m_flow_nominal_val1 = 0.1, m_flow_nominal_val2 = 0.9) annotation(
    Placement(visible = true, transformation(origin = {32, 86}, extent = {{-10, 10}, {10, -10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_a port_HW_in(redeclare package Medium = Medium2) "Port for hot water inflow" annotation(
    Placement(visible = true, transformation(origin = {-8, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-90, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_HW_out(redeclare package Medium = Medium2) "Port for hot water outflow" annotation(
    Placement(visible = true, transformation(origin = {-50, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-90, -90}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_a port_CW_in(redeclare package Medium = Medium2) "Port for cool water inflow" annotation(
    Placement(visible = true, transformation(origin = {80, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {90, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_CW_out(redeclare package Medium = Medium2) "Port for cool water outflow" annotation(
    Placement(visible = true, transformation(origin = {40, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {90, -90}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction jun_HA(redeclare package Medium = Medium1, dp_nominal = {30, -30, 30}, m_flow_nominal = {0.5, -1, 0.5}) "junction for hot air" annotation(
    Placement(visible = true, transformation(origin = {-12, 92}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Junction jun_CA(redeclare package Medium = Medium1, dp_nominal = {30, -30, 30}, m_flow_nominal = {0.5, -1, 0.5}) "junction for cool air" annotation(
    Placement(visible = true, transformation(origin = {80, 92}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput uHotWater "HeatingControl(0-1)" annotation(
    Placement(visible = true, transformation(origin = {-92, 76}, extent = {{-8, -8}, {8, 8}}, rotation = 0), iconTransformation(origin = {-91, -49}, extent = {{-7, -7}, {7, 7}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput uCoolWater "CoolingControl(0-1)" annotation(
    Placement(visible = true, transformation(origin = {18, 66}, extent = {{-8, -8}, {8, 8}}, rotation = 0), iconTransformation(origin = {91, -49}, extent = {{7, -7}, {-7, 7}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput y_OA annotation(
    Placement(visible = true, transformation(origin = {-28, 28}, extent = {{-20, -20}, {20, 20}}, rotation = -90), iconTransformation(origin = {-46, 86}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
equation
  connect(hexCool.port_b2, port_CW_out) annotation(
    Line(points = {{50, 68}, {40, 68}, {40, 52}, {40, 52}}, color = {0, 127, 255}));
  connect(port_CW_in, hexCool.port_a2) annotation(
    Line(points = {{80, 52}, {80, 52}, {80, 68}, {70, 68}, {70, 68}}));
  connect(hexHot.port_b2, port_HW_out) annotation(
    Line(points = {{-40, 68}, {-50, 68}, {-50, 52}, {-50, 52}}, color = {0, 127, 255}));
  connect(port_HW_in, hexHot.port_a2) annotation(
    Line(points = {{-8, 52}, {-8, 52}, {-8, 68}, {-20, 68}, {-20, 68}}));
  connect(hexCool.port_b1, jun_CA.port_3) annotation(
    Line(points = {{70, 80}, {80, 80}, {80, 86}}, color = {0, 127, 255}));
  connect(swValCoolWater.port_b1, hexCool.port_a1) annotation(
    Line(points = {{38, 81}, {44, 81}, {44, 80}, {50, 80}}, color = {0, 127, 255}));
  connect(swValCoolWater.port_b2, jun_CA.port_1) annotation(
    Line(points = {{38, 91}, {74, 91}, {74, 92}}, color = {0, 127, 255}));
  connect(jun_HA.port_2, swValCoolWater.port_a) annotation(
    Line(points = {{-6, 92}, {16, 92}, {16, 86}, {24, 86}}, color = {0, 127, 255}));
  connect(uCoolWater, swValCoolWater.u) annotation(
    Line(points = {{18, 66}, {32, 66}, {32, 78}}, color = {0, 0, 127}));
  connect(hexHot.port_b1, jun_HA.port_3) annotation(
    Line(points = {{-20, 80}, {-12, 80}, {-12, 86}}, color = {0, 127, 255}));
  connect(swValHotWater.port_b1, hexHot.port_a1) annotation(
    Line(points = {{-60, 80}, {-40, 80}}, color = {0, 127, 255}));
  connect(jun_CA.port_2, port_SA) annotation(
    Line(points = {{86, 92}, {96, 92}, {96, 6}, {82, 6}, {82, -12}}, color = {0, 127, 255}));
  connect(swValHotWater.port_b2, jun_HA.port_1) annotation(
    Line(points = {{-60, 90}, {-18, 90}, {-18, 92}, {-18, 92}}, color = {0, 127, 255}));
  connect(SA_damper.port_b, swValHotWater.port_a) annotation(
    Line(points = {{42, -12}, {56, -12}, {56, 40}, {-80, 40}, {-80, 84}, {-74, 84}, {-74, 84}}, color = {0, 127, 255}));
  connect(uHotWater, swValHotWater.u) annotation(
    Line(points = {{-92, 76}, {-66, 76}}, color = {0, 0, 127}));
  connect(y_OA, OA_damper.y) annotation(
    Line(points = {{-28, 28}, {-28, 28}, {-28, 0}, {-28, 0}}, color = {0, 0, 127}));
  connect(port_OA, fanOA.port_a) annotation(
    Line(points = {{-78, -12}, {-64, -12}, {-64, -12}, {-64, -12}}));
  connect(EA_damper.port_b, port_EA) annotation(
    Line(points = {{-38, -50}, {-76, -50}, {-76, -50}, {-78, -50}}, color = {0, 127, 255}));
  connect(y_fanOA, fanOA.dp_in) annotation(
    Line(points = {{-57, 25}, {-57, 25}, {-57, -3}, {-57, -3}}, color = {0, 0, 127}));
  connect(fanOA.port_b, OA_damper.port_a) annotation(
    Line(points = {{-48, -12}, {-38, -12}, {-38, -12}, {-38, -12}}, color = {0, 127, 255}));
  connect(OA_damper.port_b, SA_damper.port_a) annotation(
    Line(points = {{-18, -12}, {22, -12}, {22, -12}, {22, -12}}, color = {0, 127, 255}));
  connect(jun.port_2, EA_damper.port_a) annotation(
    Line(points = {{-6, -50}, {-18, -50}, {-18, -50}, {-18, -50}}, color = {0, 127, 255}));
  connect(y_EA, EA_damper.y) annotation(
    Line(points = {{-28, -90}, {-28, -90}, {-28, -62}, {-28, -62}}, color = {0, 0, 127}));
  connect(y_SA, SA_damper.y) annotation(
    Line(points = {{32, 28}, {32, 28}, {32, 0}, {32, 0}}, color = {0, 0, 127}));
  connect(jun.port_3, RA_damper.port_a) annotation(
    Line(points = {{2, -42}, {2, -41}, {2, -41}, {2, -36}}, color = {0, 127, 255}));
  connect(y_RA, RA_damper.y) annotation(
    Line(points = {{32, -90}, {32, -80}, {-10, -80}, {-10, -26}}, color = {0, 0, 127}));
  connect(RA_damper.port_b, SA_damper.port_a) annotation(
    Line(points = {{2, -16}, {2, -12}, {22, -12}}, color = {0, 127, 255}));
  connect(jun.port_1, fanRA.port_b) annotation(
    Line(points = {{10, -50}, {40, -50}, {40, -50}, {40, -50}}, color = {0, 127, 255}));
  connect(fanRA.port_a, port_RA) annotation(
    Line(points = {{56, -50}, {80, -50}, {80, -50}, {82, -50}}, color = {0, 127, 255}));
  connect(y_fanRA, fanRA.dp_in) annotation(
    Line(points = {{70, -86}, {48, -86}, {48, -60}, {48, -60}}, color = {0, 0, 127}));
  annotation(
    Icon(graphics = {Line(origin = {0, 4}, points = {{-80, 40}, {80, 40}, {80, 20}, {10, 20}, {10, -20}, {80, -20}, {80, -40}, {-80, -40}, {-80, -20}, {-6, -20}, {-6, 20}, {-80, 20}, {-80, 40}}, thickness = 1.5), Rectangle(origin = {-30, 41}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {48, 41}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {-26, -21}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {14, 7}, rotation = 30, fillPattern = FillPattern.Solid, extent = {{-16, 17}, {-12, -15}}), Rectangle(origin = {34, 59}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Rectangle(origin = {-44, -51}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Rectangle(origin = {-48, 59}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Text(origin = {-43, -51}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Text(origin = {-47, 59}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Text(origin = {35, 59}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Rectangle(origin = {24, 3}, fillColor = {170, 170, 127}, fillPattern = FillPattern.Solid, extent = {{-14, 15}, {16, -15}}), Text(origin = {25, 3}, extent = {{15, 11}, {-15, -11}}, textString = "M"), Text(origin = {-75, 51}, extent = {{-25, 29}, {11, -11}}, textString = "OA"), Text(origin = {82, 55}, extent = {{-22, 21}, {14, -11}}, textString = "SA"), Text(origin = {80, -6}, extent = {{-20, 30}, {14, -18}}, textString = "RA"), Text(origin = {-80, -1}, extent = {{-18, 21}, {18, -21}}, textString = "EA"), Text(origin = {-84, 94}, extent = {{-12, 6}, {12, -6}}, textString = "fanOA"), Text(origin = {-6, -96}, extent = {{-12, 6}, {12, -6}}, textString = "fanRA"), Text(origin = {-74, -49}, lineColor = {255, 0, 0}, extent = {{-8, 11}, {8, -11}}, textString = "Hot"), Text(origin = {74, -49}, lineColor = {0, 85, 255}, fillColor = {0, 85, 255}, extent = {{-8, 11}, {8, -11}}, textString = "Cool")}, coordinateSystem(initialScale = 0.1)));
end AHUv2;
