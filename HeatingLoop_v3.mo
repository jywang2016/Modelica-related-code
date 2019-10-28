within TestSys;

model HeatingLoop_v3
  // In * v3 *
  // Simplified v2 by removing power on/off, using yBoilerPower alone
  // http://www.engineeringtoolbox.com/boiler-efficiency-d_438.html
  // http://www.engineeringtoolbox.com/air-properties-d_156.html
  // WaterTinit is just setting the initial temperature to a different value
  //package water = WaterTinit15dC;
  // Or use the "system" component in standard lib under Fluids
  // This is due to T_start in PartialLumpedVolume is written this way....
  package water = Buildings.Media.Water "Medium water";
  Buildings.Fluid.Movers.FlowControlled_m_flow pump(redeclare package Medium = water, VMachine_flow(start = 2e-4), dp(start = 100), m_flow(start = 0.01), m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-60, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe1(redeclare package Medium = water,lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05)  annotation(
    Placement(visible = true, transformation(origin = {0, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Boilers.BoilerPolynomial boiler(redeclare package Medium = water,Q_flow_nominal = 5e5, dp_nominal = 500, m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {52, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank tank(redeclare package Medium = water,crossArea = 1, height = 2, nPorts = 2, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1)})  annotation(
    Placement(visible = true, transformation(origin = {70, 70}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe2(redeclare package Medium = water,lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05)  annotation(
    Placement(visible = true, transformation(origin = {0, 58}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Interfaces.RealOutput T_ambient annotation(
    Placement(visible = true, transformation(origin = {-32, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-88, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Buildings.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature annotation(
    Placement(visible = true, transformation(origin = {-22, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yBoilerPower "Boiler power index (0-1)" annotation(
    Placement(visible = true, transformation(origin = {0, -86}, extent = {{-10, -10}, {10, 10}}, rotation = 90), iconTransformation(origin = {-26, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Fluid.Interfaces.FluidPort_a port_a(redeclare package Medium = water) "Cool water in" annotation(
    Placement(visible = true, transformation(origin = {-84, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_b(redeclare package Medium = water) "Hot water out" annotation(
    Placement(visible = true, transformation(origin = {-84, 58}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-82, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient = T_ambient)  annotation(
    Placement(visible = true, transformation(origin = {-82, -86}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant constBoilerOffPower(k = 0.001)  annotation(
    Placement(visible = true, transformation(origin = {65, -89}, extent = {{5, -5}, {-5, 5}}, rotation = -90)));
  Modelica.Blocks.Sources.Constant constBoilerTempHighLimit(k = 273.15 + 70)  annotation(
    Placement(visible = true, transformation(origin = {87, -33}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
  TestSys.SafetyBox_v2 safetyBox_v2 annotation(
    Placement(visible = true, transformation(origin = {62, -52}, extent = {{12, -12}, {-12, 12}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant constBoilerTempLowLimit(k = 273.15 + 50)  annotation(
    Placement(visible = true, transformation(origin = {91, -53}, extent = {{5, -5}, {-5, 5}}, rotation = 0)));
equation
  connect(yBoilerPower, pump.m_flow_in) annotation(
    Line(points = {{0, -86}, {0, -68}, {-94, -68}, {-94, 0}, {-60, 0}, {-60, -12}}, color = {0, 0, 127}));
  connect(yBoilerPower, safetyBox_v2.u) annotation(
    Line(points = {{0, -86}, {0, -68}, {76, -68}, {76, -58}, {66, -58}, {66, -56}}, color = {0, 0, 127}));
  connect(boiler.T, safetyBox_v2.uSensor) annotation(
    Line(points = {{64, -16}, {72, -16}, {72, -42}, {66, -42}}, color = {0, 0, 127}));
  connect(constBoilerTempHighLimit.y, safetyBox_v2.uHighLimit) annotation(
    Line(points = {{81.5, -33}, {76, -33}, {76, -47}, {66, -47}}, color = {0, 0, 127}));
  connect(constBoilerOffPower.y, safetyBox_v2.uNew) annotation(
    Line(points = {{66, -84}, {64, -84}, {64, -76}, {72, -76}, {72, -62}, {66, -62}}, color = {0, 0, 127}));
  connect(constBoilerTempLowLimit.y, safetyBox_v2.uLowLimit) annotation(
    Line(points = {{86, -52}, {66, -52}}, color = {0, 0, 127}));
  connect(safetyBox_v2.y, boiler.y) annotation(
    Line(points = {{54, -52}, {32, -52}, {32, -16}, {40, -16}}, color = {0, 0, 127}));
  connect(pipe1.port_b, boiler.port_a) annotation(
    Line(points = {{10, -24}, {42, -24}, {42, -24}, {42, -24}}, color = {0, 127, 255}));
  connect(boiler.port_b, tank.ports[1]) annotation(
    Line(points = {{62, -24}, {76, -24}, {76, 50}, {70, 50}}, color = {0, 127, 255}));
  connect(prescribedTemperature.port, boiler.heatPort) annotation(
    Line(points = {{-12, 26}, {52, 26}, {52, -16}, {52, -16}}, color = {191, 0, 0}));
  connect(tank.ports[2], pipe2.port_a) annotation(
    Line(points = {{70, 50}, {22, 50}, {22, 58}, {10, 58}, {10, 58}}, color = {0, 127, 255}));
  connect(T_ambient, prescribedTemperature.T) annotation(
    Line(points = {{-32, -50}, {-36, -50}, {-36, 26}, {-34, 26}}, color = {0, 0, 127}));
  connect(port_a, pump.port_a) annotation(
    Line(points = {{-84, -24}, {-70, -24}, {-70, -24}, {-70, -24}}));
  connect(pump.port_b, pipe1.port_a) annotation(
    Line(points = {{-50, -24}, {-10, -24}, {-10, -24}, {-10, -24}}, color = {0, 127, 255}));
  connect(prescribedTemperature.port, pipe1.heatPort) annotation(
    Line(points = {{-12, 26}, {0, 26}, {0, -18}, {0, -18}}, color = {191, 0, 0}));
  connect(prescribedTemperature.port, pipe2.heatPort) annotation(
    Line(points = {{-12, 26}, {0, 26}, {0, 54}, {0, 54}}, color = {191, 0, 0}));
  connect(port_b, pipe2.port_b) annotation(
    Line(points = {{-84, 58}, {-10, 58}, {-10, 58}, {-10, 58}}));
  annotation(
    Icon(graphics = {Rectangle(origin = {-3, -61}, lineColor = {0, 0, 255}, fillColor = {0, 255, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-71, 7}, {69, -5}}), Rectangle(origin = {-3, 59}, lineColor = {255, 0, 0}, fillColor = {255, 170, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-71, 7}, {69, -5}}), Rectangle(origin = {58, -11}, lineColor = {255, 170, 0}, fillColor = {255, 255, 127}, fillPattern = FillPattern.VerticalCylinder, extent = {{-4, 77}, {8, -55}}), Polygon(origin = {-53.12, -38.05}, fillColor = {0, 85, 255}, fillPattern = FillPattern.Solid, points = {{-16.8763, 2.05038}, {3.12371, 2.05038}, {3.12371, 10.0504}, {17.1237, -1.94962}, {3.12371, -11.9496}, {3.12371, -5.94962}, {-16.8763, -5.94962}, {-16.8763, 2.05038}, {-16.8763, 2.05038}}), Polygon(origin = {-55.12, 37.95}, rotation = 180, fillColor = {255, 0, 0}, fillPattern = FillPattern.Solid, points = {{-16.8763, 2.05038}, {3.12371, 2.05038}, {3.12371, 10.0504}, {17.1237, -1.94962}, {3.12371, -11.9496}, {3.12371, -5.94962}, {-16.8763, -5.94962}, {-16.8763, 2.05038}, {-16.8763, 2.05038}}), Text(origin = {-31, -11}, extent = {{-45, 9}, {81, -21}}, textString = "Cool Water In"), Text(origin = {-31, 27}, extent = {{-45, 9}, {81, -21}}, textString = "Hot Water Out"), Text(origin = {-55, -85}, extent = {{-27, 13}, {17, -7}}, textString = "Tamb"), Text(origin = {3, -78}, extent = {{-23, 6}, {31, -14}}, textString = "yBoiler")}, coordinateSystem(initialScale = 0.1)));

end HeatingLoop_v3;
