within TestSys;

model HeatingLoop
  // http://www.engineeringtoolbox.com/boiler-efficiency-d_438.html
  // http://www.engineeringtoolbox.com/air-properties-d_156.html
  
  // WaterTinit is just setting the initial temperature to a different value
  //package water = WaterTinit15dC;
  
  // Or use the "system" component in standard lib under Fluids
  // This is due to T_start in PartialLumpedVolume is written this way....
  package water = Buildings.Media.Water "Medium water";  
  
  Buildings.Fluid.Movers.FlowControlled_m_flow pump(redeclare package Medium = water,VMachine_flow(start = 2e-4), dp(start = 100), m_flow(start = 0.01), m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {-60, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe1(redeclare package Medium = water,lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05)  annotation(
    Placement(visible = true, transformation(origin = {0, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Boilers.BoilerPolynomial boiler(redeclare package Medium = water,Q_flow_nominal = 5e4, dp_nominal = 500, m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {52, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank tank(redeclare package Medium = water,crossArea = 1, height = 2, nPorts = 2, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1)})  annotation(
    Placement(visible = true, transformation(origin = {70, 48}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe2(redeclare package Medium = water,lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05)  annotation(
    Placement(visible = true, transformation(origin = {0, 36}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 5, height = 2)  annotation(
    Placement(visible = true, transformation(origin = {-58, -6}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealOutput T_ambient annotation(
    Placement(visible = true, transformation(origin = {-32, -72}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-76, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature annotation(
    Placement(visible = true, transformation(origin = {-22, 4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yBoilerPower "Boiler power index (0-1)" annotation(
    Placement(visible = true, transformation(origin = {28, -66}, extent = {{-10, -10}, {10, 10}}, rotation = 90), iconTransformation(origin = {12, -82}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_a port_a "Cool water in" annotation(
    Placement(visible = true, transformation(origin = {-84, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_b "Hot water out" annotation(
    Placement(visible = true, transformation(origin = {-84, 36}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-82, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient = T_ambient)  annotation(
    Placement(visible = true, transformation(origin = {-80, -82}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(port_b, pipe2.port_b) annotation(
    Line(points = {{-84, 36}, {-10, 36}, {-10, 36}, {-10, 36}}));
  connect(port_a, pump.port_a) annotation(
    Line(points = {{-84, -46}, {-70, -46}, {-70, -46}, {-70, -46}}));
  connect(yBoilerPower, boiler.y) annotation(
    Line(points = {{28, -66}, {28, -66}, {28, -38}, {40, -38}, {40, -38}}, color = {0, 0, 127}));
  connect(T_ambient, prescribedTemperature.T) annotation(
    Line(points = {{-32, -72}, {-36, -72}, {-36, 4}, {-34, 4}}, color = {0, 0, 127}));
  connect(prescribedTemperature.port, boiler.heatPort) annotation(
    Line(points = {{-12, 4}, {52, 4}, {52, -38}, {52, -38}}, color = {191, 0, 0}));
  connect(prescribedTemperature.port, pipe1.heatPort) annotation(
    Line(points = {{-12, 4}, {0, 4}, {0, -40}, {0, -40}}, color = {191, 0, 0}));
  connect(prescribedTemperature.port, pipe2.heatPort) annotation(
    Line(points = {{-12, 4}, {0, 4}, {0, 32}, {0, 32}}, color = {191, 0, 0}));
  connect(ramp1.y, pump.m_flow_in) annotation(
    Line(points = {{-58, -18}, {-60, -18}, {-60, -34}, {-60, -34}}, color = {0, 0, 127}));
  connect(tank.ports[2], pipe2.port_a) annotation(
    Line(points = {{70, 28}, {22, 28}, {22, 36}, {10, 36}, {10, 36}}, color = {0, 127, 255}));
  connect(boiler.port_b, tank.ports[1]) annotation(
    Line(points = {{62, -46}, {76, -46}, {76, 28}, {70, 28}}, color = {0, 127, 255}));
  connect(pipe1.port_b, boiler.port_a) annotation(
    Line(points = {{10, -46}, {42, -46}, {42, -46}, {42, -46}}, color = {0, 127, 255}));
  connect(pump.port_b, pipe1.port_a) annotation(
    Line(points = {{-50, -46}, {-10, -46}, {-10, -46}, {-10, -46}}, color = {0, 127, 255}));
  annotation(
    Icon(graphics = {Rectangle(origin = {-3, -61}, lineColor = {0, 0, 255}, fillColor = {0, 255, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-71, 7}, {69, -5}}), Rectangle(origin = {-3, 59}, lineColor = {255, 0, 0}, fillColor = {255, 170, 255}, fillPattern = FillPattern.HorizontalCylinder, extent = {{-71, 7}, {69, -5}}), Rectangle(origin = {58, -11}, lineColor = {255, 170, 0}, fillColor = {255, 255, 127}, fillPattern = FillPattern.VerticalCylinder, extent = {{-4, 77}, {8, -55}}), Polygon(origin = {-53.12, -38.05}, fillColor = {0, 85, 255}, fillPattern = FillPattern.Solid, points = {{-16.8763, 2.05038}, {3.12371, 2.05038}, {3.12371, 10.0504}, {17.1237, -1.94962}, {3.12371, -11.9496}, {3.12371, -5.94962}, {-16.8763, -5.94962}, {-16.8763, 2.05038}, {-16.8763, 2.05038}}), Polygon(origin = {-55.12, 37.95}, rotation = 180, fillColor = {255, 0, 0}, fillPattern = FillPattern.Solid, points = {{-16.8763, 2.05038}, {3.12371, 2.05038}, {3.12371, 10.0504}, {17.1237, -1.94962}, {3.12371, -11.9496}, {3.12371, -5.94962}, {-16.8763, -5.94962}, {-16.8763, 2.05038}, {-16.8763, 2.05038}}), Text(origin = {-31, -11}, extent = {{-45, 9}, {81, -21}}, textString = "Cool Water In"), Text(origin = {-31, 27}, extent = {{-45, 9}, {81, -21}}, textString = "Hot Water Out"), Text(origin = {-37, -83}, extent = {{-27, 13}, {27, -13}}, textString = "Tamb"), Text(origin = {59, -80}, extent = {{-35, 16}, {35, -16}}, textString = "yBoiler")}));end HeatingLoop;
