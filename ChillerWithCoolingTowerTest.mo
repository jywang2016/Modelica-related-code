within TestSys;

model ChillerWithCoolingTowerTest
  package water = Buildings.Media.Water "Medium model";  

  Buildings.Fluid.HeatExchangers.CoolingTowers.FixedApproach CoolingTower(redeclare package Medium = water,TApp = -12, dp(start = 300), dp_nominal = 300, m_flow(start = 0.1), m_flow_nominal = 0.3)  annotation(
    Placement(visible = true, transformation(origin = {0, 50}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Chillers.Carnot_TEva chiller(redeclare package Medium1 = water, redeclare package Medium2 = water,QEva_flow_nominal = -1e6, dp1_nominal = 300, dp2_nominal = 300, energyDynamics = Modelica.Fluid.Types.Dynamics.DynamicFreeInitial, etaCarnot_nominal = 0.3)  annotation(
    Placement(visible = true, transformation(origin = {0, -34}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source(redeclare package Medium = water,T = 273.15 + 25, m_flow = 0.3, nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {68, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Sources.FixedBoundary sink(redeclare package Medium = water,nPorts = 1)  annotation(
    Placement(visible = true, transformation(origin = {-70, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant TAir(k = 273.15 + 23)  annotation(
    Placement(visible = true, transformation(origin = {36, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Constant TEva(k = 273.15 + 6)  annotation(
    Placement(visible = true, transformation(origin = {-38, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Movers.FlowControlled_m_flow pump(redeclare package Medium = water,dp(start = 100), inputType = Buildings.Fluid.Types.InputType.Continuous, m_flow(start = 0.1), m_flow_nominal = 0.3)  annotation(
    Placement(visible = true, transformation(origin = {-72, 28}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Ramp massflow(duration = 1, height = 0.3)  annotation(
    Placement(visible = true, transformation(origin = {-28, 28}, extent = {{-8, -8}, {8, 8}}, rotation = 180)));
  Modelica.Fluid.Vessels.OpenTank tank(redeclare package Medium = water,crossArea = 1, height = 2, nPorts = 2, use_portsData = false)  annotation(
    Placement(visible = true, transformation(origin = {73, 65}, extent = {{-15, -15}, {15, 15}}, rotation = 0)));
equation
  connect(chiller.port_b1, tank.ports[1]) annotation(
    Line(points = {{10, -28}, {76, -28}, {76, 50}, {73, 50}}, color = {0, 127, 255}));
  connect(source.ports[1], chiller.port_a2) annotation(
    Line(points = {{58, -48}, {43, -48}, {43, -50}, {28, -50}, {28, -42}, {10, -42}, {10, -40}}, color = {0, 127, 255}));
  connect(chiller.port_b2, sink.ports[1]) annotation(
    Line(points = {{-10, -40}, {-60, -40}, {-60, -48}}, color = {0, 127, 255}));
  connect(TEva.y, chiller.TSet) annotation(
    Line(points = {{-27, 0}, {-21, 0}, {-21, -2}, {-13, -2}, {-13, -24}, {-13, -24}}, color = {0, 0, 127}));
  connect(pump.port_b, chiller.port_a1) annotation(
    Line(points = {{-72, 18}, {-72, 18}, {-72, 16}, {-72, 16}, {-72, -28}, {-10, -28}, {-10, -28}}, color = {0, 127, 255}));
  connect(tank.ports[2], CoolingTower.port_a) annotation(
    Line(points = {{73, 50}, {10, 50}}, color = {0, 127, 255}));
  connect(TAir.y, CoolingTower.TAir) annotation(
    Line(points = {{25, 26}, {20, 26}, {20, 24}, {15, 24}, {15, 44}, {14, 44}, {14, 46}, {13, 46}}, color = {0, 0, 127}));
  connect(CoolingTower.port_b, pump.port_a) annotation(
    Line(points = {{-10, 50}, {-41, 50}, {-41, 48}, {-72, 48}, {-72, 36}, {-72, 36}, {-72, 38}, {-72, 38}}, color = {0, 127, 255}));
  connect(massflow.y, pump.m_flow_in) annotation(
    Line(points = {{-36.8, 28}, {-59.8, 28}}, color = {0, 0, 127}));
end ChillerWithCoolingTowerTest;
