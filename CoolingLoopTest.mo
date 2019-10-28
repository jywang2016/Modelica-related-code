within TestSys;

model CoolingLoopTest
  package water = Buildings.Media.Water "Medium model";
  Buildings.Fluid.Movers.FlowControlled_m_flow pumpChiller(redeclare package Medium = water, dp(start = 100), m_flow(start = 0.01), m_flow_nominal = 0.5) annotation(
    Placement(visible = true, transformation(origin = {-76, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe1(redeclare package Medium = water,lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05)  annotation(
    Placement(visible = true, transformation(origin = {-38, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Chillers.Carnot_TEva chiller(redeclare package Medium1 = water, redeclare package Medium2 = water,QEva_flow_nominal = -1e6, dp1_nominal = 100, dp2_nominal = 100, energyDynamics = Modelica.Fluid.Types.Dynamics.DynamicFreeInitial, etaCarnot_nominal = 0.3)  annotation(
    Placement(visible = true, transformation(origin = {2, 12}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Fluid.Vessels.OpenTank tank1(redeclare package Medium = water,crossArea = 1, height = 2, nPorts = 2, use_portsData = false)  annotation(
    Placement(visible = true, transformation(origin = {2, 82}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.FixedResistances.Pipe pipe2(redeclare package Medium = water,lambdaIns = 0.1, length = 10, m_flow_nominal = 0.2, thicknessIns = 0.05)  annotation(
    Placement(visible = true, transformation(origin = {-36, 72}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Ramp ramp1(duration = 5)  annotation(
    Placement(visible = true, transformation(origin = {-76, 2}, extent = {{-6, -6}, {6, 6}}, rotation = -90)));
  Buildings.Fluid.Movers.FlowControlled_m_flow pumpCoolingTower(redeclare package Medium = water,dp(start = 100),init = Modelica.Blocks.Types.Init.NoInit, m_flow(start = 0.1), m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {52, 64}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Fluid.Vessels.OpenTank tank2(redeclare package Medium = water,crossArea = 0.36, height = 1.5, nPorts = 2, use_portsData = false)  annotation(
    Placement(visible = true, transformation(origin = {23, -15}, extent = {{-11, -11}, {11, 11}}, rotation = 0)));
  Buildings.Fluid.HeatExchangers.CoolingTowers.FixedApproach CoolingTower(redeclare package Medium = water,TApp = CoolingTower.vol.T - Tamb.k, dp_nominal = 100, m_flow_nominal = 0.5)  annotation(
    Placement(visible = true, transformation(origin = {54, -52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Ramp ramp2(duration = 5, height = 1)  annotation(
    Placement(visible = true, transformation(origin = {52, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Blocks.Sources.Constant TEva_const(k = 273.15 + 6)  annotation(
    Placement(visible = true, transformation(origin = {-14, 42}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant Tamb(k = 273.15 + 22)  annotation(
    Placement(visible = true, transformation(origin = {6, -58}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(Tamb.y, CoolingTower.TAir) annotation(
    Line(points = {{18, -58}, {34, -58}, {34, -48}, {42, -48}, {42, -48}}, color = {0, 0, 127}));
  connect(TEva_const.y, chiller.TSet) annotation(
    Line(points = {{-2, 42}, {12, 42}, {12, 24}, {12, 24}}, color = {0, 0, 127}));
  connect(ramp2.y, pumpCoolingTower.m_flow_in) annotation(
    Line(points = {{52, 38}, {52, 38}, {52, 52}, {52, 52}}, color = {0, 0, 127}));
  connect(CoolingTower.port_b, pumpCoolingTower.port_a) annotation(
    Line(points = {{64, -52}, {80, -52}, {80, 64}, {62, 64}, {62, 64}}, color = {0, 127, 255}));
  connect(pumpCoolingTower.port_b, chiller.port_a1) annotation(
    Line(points = {{42, 64}, {8, 64}, {8, 22}}, color = {0, 127, 255}));
  connect(tank2.ports[2], CoolingTower.port_a) annotation(
    Line(points = {{24, -26}, {24, -26}, {24, -52}, {44, -52}, {44, -52}}, color = {0, 127, 255}));
  connect(chiller.port_b1, tank2.ports[1]) annotation(
    Line(points = {{8, 2}, {8, 2}, {8, -26}, {24, -26}, {24, -26}}, color = {0, 127, 255}));
  connect(ramp1.y, pumpChiller.m_flow_in) annotation(
    Line(points = {{-76, -5}, {-76, -24}}, color = {0, 0, 127}));
  connect(pipe2.port_b, pumpChiller.port_a) annotation(
    Line(points = {{-46, 72}, {-86, 72}, {-86, -36}}, color = {0, 127, 255}));
  connect(pumpChiller.port_b, pipe1.port_a) annotation(
    Line(points = {{-66, -36}, {-48, -36}}, color = {0, 127, 255}));
  connect(tank1.ports[2], pipe2.port_a) annotation(
    Line(points = {{2, 72}, {-26, 72}}, color = {0, 127, 255}));
  connect(chiller.port_b2, tank1.ports[1]) annotation(
    Line(points = {{-4, 22}, {2, 22}, {2, 72}, {2, 72}}, color = {0, 127, 255}));
  connect(pipe1.port_b, chiller.port_a2) annotation(
    Line(points = {{-28, -36}, {-4, -36}, {-4, 2}, {-4, 2}}, color = {0, 127, 255}));
end CoolingLoopTest;
