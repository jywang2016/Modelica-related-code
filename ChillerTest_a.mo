within TestSys;

model ChillerTest_a
  // As of version 1.11.0(64-bit), Chiller component in Buildings library cannot run. Use Jmodelica as an alternative.
  // "Cyclically dependent constants or parameters found in scope" error
  // The model allows to either specify the Carnot effectivness ηCarnot,0, or a COP0 at the nominal conditions
  // make sure that the condenser has sufficient mass flow rate
  // make sure that QEva_flow_nominal is set to a reasonable value.
  // QEva_flow_nominal is used to assign the default value for the mass flow rates, which are used for the pressure drop calculations.
  // It is also used to compute the part load efficiency. Hence, make sure that QEva_flow_nominal is set to a reasonable value
  // Select Modelica.Fluid.Types.Dynamics.DynamicFreeInitial for dynamics to make it work!
  package Medium1 = Buildings.Media.Water "Medium model";
  package Medium2 = Buildings.Media.Water "Medium model";
  Buildings.Fluid.Chillers.Carnot_TEva chi(redeclare package Medium1 = Medium1, redeclare package Medium2 = Medium2, QEva_flow_nominal = -1e5, dp1_nominal = 6e3, dp2_nominal = 6e3, energyDynamics = Modelica.Fluid.Types.Dynamics.DynamicFreeInitial, etaCarnot_nominal = 0.3, use_eta_Carnot_nominal = true) annotation(
    Placement(visible = true, transformation(origin = {2, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source1(redeclare package Medium = Medium1, T = 273.15 + 15, m_flow = 2, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {-48, 24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.MassFlowSource_T source2(redeclare package Medium = Medium1, T = 273.15 + 30, m_flow = 1, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {60, -28}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Buildings.Fluid.Sources.FixedBoundary sink2(redeclare package Medium = Medium1, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {-54, -28}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Fluid.Sources.FixedBoundary sink1(redeclare package Medium = Medium1, nPorts = 1) annotation(
    Placement(visible = true, transformation(origin = {60, 24}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Sources.Ramp ramp1(height = 3, offset = 273.15 + 5) annotation(
    Placement(visible = true, transformation(origin = {-30, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(ramp1.y, chi.TSet) annotation(
    Line(points = {{-18, 52}, {-10, 52}, {-10, 10}, {-10, 10}}, color = {0, 0, 127}));
  connect(chi.port_b1, sink1.ports[1]) annotation(
    Line(points = {{12, 6}, {28, 6}, {28, 24}, {50, 24}, {50, 24}}, color = {0, 127, 255}));
  connect(source1.ports[1], chi.port_a1) annotation(
    Line(points = {{-38, 24}, {-20, 24}, {-20, 6}, {-8, 6}, {-8, 6}}, color = {0, 127, 255}));
  connect(chi.port_b2, sink2.ports[1]) annotation(
    Line(points = {{-8, -6}, {-20, -6}, {-20, -28}, {-44, -28}, {-44, -28}}, color = {0, 127, 255}));
  connect(source2.ports[1], chi.port_a2) annotation(
    Line(points = {{50, -28}, {28, -28}, {28, -6}, {12, -6}, {12, -6}}, color = {0, 127, 255}));
end ChillerTest_a;
