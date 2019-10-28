within TestSys;

model CoolingLoop_v5F
  // v2: adds a port for ambient temperature for cooling tower
  // v3: adds in on-off switch
  // v4: removes on-off switch, use direct power signal(0-1) instead, 0 is off
  // v5: adds in safety switch to avoid ambient temperature being less than 0
  // v5F5: same as v5 but changed parameters to simulate fault 5:
  //       leaking refrigerant by lowering efficiency(lower QEva_flow_nominal and etaCarnot_nominal)
  //       and raising TSet(TEva)
  package water = Buildings.Media.Water "Medium model";
  // WaterTinit is just setting the initial temperature to a different value
  //package water = WaterTinit30dC "Medium model";
  // Or use the "system" component in standard lib under Fluids
  // This is due to T_start in PartialLumpedVolume is written this way....
  Buildings.Fluid.Movers.FlowControlled_m_flow pumpChiller(redeclare package Medium = water, dp(start = 100), m_flow(start = 0.01), m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-76, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe1(redeclare package Medium = water, lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05) annotation(
    Placement(visible = true, transformation(origin = {-38, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Chillers.Carnot_TEva chiller(redeclare package Medium1 = water, redeclare package Medium2 = water, QEva_flow_nominal = -3e4, dp1_nominal = 100, dp2_nominal = 100, energyDynamics = Modelica.Fluid.Types.Dynamics.DynamicFreeInitial, etaCarnot_nominal = 0.2) annotation(
    Placement(visible = true, transformation(origin = {2, 12}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Fluid.Vessels.OpenTank tank1(redeclare package Medium = water, crossArea = 0.36, height = 1, nPorts = 2, use_portsData = false) annotation(
    Placement(visible = true, transformation(origin = {2, 82}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe2(redeclare package Medium = water, lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05) annotation(
    Placement(visible = true, transformation(origin = {-38, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Movers.FlowControlled_m_flow pumpCoolingTower(redeclare package Medium = water, dp(start = 100), init = Modelica.Blocks.Types.Init.NoInit, m_flow(start = 0.1), m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {52, 64}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Fluid.Vessels.OpenTank tank2(redeclare package Medium = water, crossArea = 0.64, height = 1.5, nPorts = 2, use_portsData = false) annotation(
    Placement(visible = true, transformation(origin = {23, -15}, extent = {{-11, -11}, {11, 11}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.CoolingTowers.FixedApproach CoolingTower(redeclare package Medium = water, dp_nominal = 100, m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {54, -52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant TEva_const(k = 279.15 + 2) annotation(
    Placement(visible = true, transformation(origin = {-14, 42}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_a port_a "Hot water in" annotation(
    Placement(visible = true, transformation(origin = {-86, -68}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Interfaces.FluidPort_b port_b "Chilled water out" annotation(
    Placement(visible = true, transformation(origin = {-86, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-80, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput T_ambient "Ambient temperature" annotation(
    Placement(visible = true, transformation(origin = {-40, -66}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-70, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  //initial equation
  //water.BaseProperties.T = T_ambient;
  Buildings.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature annotation(
    Placement(visible = true, transformation(origin = {-54, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Fluid.System system(T_ambient(displayUnit = "K") = T_ambient) annotation(
    Placement(visible = true, transformation(origin = {-58, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yCooling "Cooling power signal input (0-1)" annotation(
    Placement(visible = true, transformation(origin = {2, -82}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {2, -82}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Blocks.Sources.Constant constAntiFreezeTemp(k = 273.15 + 0.8) annotation(
    Placement(visible = true, transformation(origin = {-26, -74}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant constFreezeHighLimit(k = 273.15 + 1) annotation(
    Placement(visible = true, transformation(origin = {-26, -58}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  TestSys.SafetyBox_v2c safetyBox_v2c(reverseMode = true, y(start = 273.15 + 20)) annotation(
    Placement(visible = true, transformation(origin = {-2, -62}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(safetyBox_v2c.y, prescribedTemperature.T) annotation(
    Line(points = {{4, -62}, {14, -62}, {14, -30}, {-20, -30}, {-20, 8}, {-72, 8}, {-72, 32}, {-66, 32}, {-66, 32}}, color = {0, 0, 127}));
  connect(safetyBox_v2c.y, CoolingTower.TAir) annotation(
    Line(points = {{4, -62}, {30, -62}, {30, -48}, {42, -48}, {42, -48}}, color = {0, 0, 127}));
  connect(T_ambient, safetyBox_v2c.uSensor) annotation(
    Line(points = {{-40, -66}, {-16, -66}, {-16, -54}, {-6, -54}, {-6, -54}}, color = {0, 0, 127}));
  connect(T_ambient, safetyBox_v2c.u) annotation(
    Line(points = {{-40, -66}, {-6, -66}, {-6, -66}, {-6, -66}}, color = {0, 0, 127}));
  connect(constFreezeHighLimit.y, safetyBox_v2c.uHighLimit) annotation(
    Line(points = {{-22, -58}, {-6, -58}, {-6, -58}, {-6, -58}}, color = {0, 0, 127}));
  connect(constAntiFreezeTemp.y, safetyBox_v2c.uLowLimit) annotation(
    Line(points = {{-22, -74}, {-12, -74}, {-12, -62}, {-5, -62}}, color = {0, 0, 127}));
  connect(constAntiFreezeTemp.y, safetyBox_v2c.uNew) annotation(
    Line(points = {{-22, -74}, {-12, -74}, {-12, -70}, {-5, -70}}, color = {0, 0, 127}));
  connect(yCooling, pumpCoolingTower.m_flow_in) annotation(
    Line(points = {{2, -82}, {92, -82}, {92, 42}, {52, 42}, {52, 52}, {52, 52}}, color = {0, 0, 127}));
  connect(yCooling, pumpChiller.m_flow_in) annotation(
    Line(points = {{2, -82}, {-4, -82}, {-4, -98}, {-94, -98}, {-94, -16}, {-76, -16}, {-76, -24}, {-76, -24}}, color = {0, 0, 127}));
  connect(prescribedTemperature.port, tank2.heatPort) annotation(
    Line(points = {{-44, 32}, {-26, 32}, {-26, -16}, {12, -16}, {12, -14}}, color = {191, 0, 0}));
  connect(prescribedTemperature.port, tank1.heatPort) annotation(
    Line(points = {{-44, 32}, {-26, 32}, {-26, 82}, {-8, 82}, {-8, 82}}, color = {191, 0, 0}));
  connect(prescribedTemperature.port, pipe2.heatPort) annotation(
    Line(points = {{-44, 32}, {-38, 32}, {-38, 67}}, color = {191, 0, 0}));
  connect(tank1.ports[2], pipe2.port_a) annotation(
    Line(points = {{2, 72}, {-28, 72}}, color = {0, 127, 255}));
  connect(pipe2.port_b, port_b) annotation(
    Line(points = {{-48, 72}, {-86, 72}}, color = {0, 127, 255}));
  connect(prescribedTemperature.port, pipe1.heatPort) annotation(
    Line(points = {{-44, 32}, {-38, 32}, {-38, -30}, {-38, -30}}, color = {191, 0, 0}));
  connect(pumpChiller.port_a, port_a) annotation(
    Line(points = {{-86, -36}, {-86, -36}, {-86, -68}, {-86, -68}}, color = {0, 127, 255}));
  connect(TEva_const.y, chiller.TSet) annotation(
    Line(points = {{-2, 42}, {12, 42}, {12, 24}, {12, 24}}, color = {0, 0, 127}));
  connect(CoolingTower.port_b, pumpCoolingTower.port_a) annotation(
    Line(points = {{64, -52}, {80, -52}, {80, 64}, {62, 64}, {62, 64}}, color = {0, 127, 255}));
  connect(pumpCoolingTower.port_b, chiller.port_a1) annotation(
    Line(points = {{42, 64}, {8, 64}, {8, 22}}, color = {0, 127, 255}));
  connect(tank2.ports[2], CoolingTower.port_a) annotation(
    Line(points = {{24, -26}, {24, -26}, {24, -52}, {44, -52}, {44, -52}}, color = {0, 127, 255}));
  connect(chiller.port_b1, tank2.ports[1]) annotation(
    Line(points = {{8, 2}, {8, 2}, {8, -26}, {24, -26}, {24, -26}}, color = {0, 127, 255}));
  connect(pumpChiller.port_b, pipe1.port_a) annotation(
    Line(points = {{-66, -36}, {-48, -36}}, color = {0, 127, 255}));
  connect(chiller.port_b2, tank1.ports[1]) annotation(
    Line(points = {{-4, 22}, {2, 22}, {2, 72}, {2, 72}}, color = {0, 127, 255}));
  connect(pipe1.port_b, chiller.port_a2) annotation(
    Line(points = {{-28, -36}, {-4, -36}, {-4, 2}, {-4, 2}}, color = {0, 127, 255}));
  annotation(
    Icon(graphics = {Rectangle(origin = {-4, -59}, lineColor = {255, 0, 0}, fillColor = {255, 170, 255}, pattern = LinePattern.None, fillPattern = FillPattern.HorizontalCylinder, extent = {{-70, 5}, {70, -7}}), Rectangle(origin = {-4, 61}, lineColor = {0, 0, 255}, fillColor = {85, 255, 255}, pattern = LinePattern.None, fillPattern = FillPattern.HorizontalCylinder, extent = {{-70, 5}, {70, -7}}), Rectangle(origin = {60, 1}, lineColor = {255, 170, 0}, fillColor = {255, 255, 127}, pattern = LinePattern.None, fillPattern = FillPattern.VerticalCylinder, extent = {{-6, 65}, {6, -67}}), Polygon(origin = {-51.12, -35.95}, fillColor = {255, 0, 0}, fillPattern = FillPattern.Solid, points = {{19.1237, -2.05038}, {7.12371, 7.9496}, {7.12371, 1.94962}, {-16.8763, 1.94962}, {-16.8763, -6.05038}, {7.12371, -6.05038}, {7.12371, -12.0504}, {19.1237, -2.05038}}), Polygon(origin = {-49.12, 38.05}, rotation = 180, fillColor = {0, 85, 255}, fillPattern = FillPattern.Solid, points = {{19.1237, -2.05038}, {7.12371, 7.9496}, {7.12371, 1.94962}, {-16.8763, 1.94962}, {-16.8763, -6.05038}, {7.12371, -6.05038}, {7.12371, -12.0504}, {19.1237, -2.05038}}), Text(origin = {-6, -24}, extent = {{-62, 16}, {32, -6}}, textString = "Hot Water In"), Text(origin = {-4, 16}, extent = {{-62, 16}, {32, -6}}, textString = "Cool Water Out"), Text(origin = {-40, -82}, extent = {{-46, 10}, {46, -10}}, textString = "Tamb"), Text(origin = {44, -82}, extent = {{-46, 10}, {46, -10}}, textString = "yCooling")}, coordinateSystem(initialScale = 0.1)));
end CoolingLoop_v5F;
