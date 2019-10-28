within TestSys;

model ControlUnit
  //parameter Boolean defaultSATSP = true "Use default setpoints, uses SASP_H and SASP_L instead of SASP";
  //parameter Modelica.SIunits.Temperature SASP_H = 273.15+13 "Supply Air Temperature Setpoint(OAT>=18)";
  //parameter Modelica.SIunits.Temperature SASP_L = 273.15+16 "Supply Air Temperature Setpoint(OAT<=13)";
  //parameter Modelica.SIunits.Temperature SASP = 273.15+13 "Supply Air Temperature Setpoint";
  
  parameter Modelica.SIunits.Temperature CSP = 273.15+18 "Cooling Setpoint";
  parameter Modelica.SIunits.Temperature HSP = 273.15+13 "Heating Setpoint";
  parameter Modelica.SIunits.Temperature ESP = 273.15+18 "Economizer Setpoint";
  parameter Modelica.SIunits.Temperature CmaxSP = 273.15+21 "Cooling Max Setpoint";
  parameter Modelica.SIunits.Temperature HmaxSP = 273.15+10 "Heating Max Setpoint";
  
  parameter Real minOAD = 0.2 "min OAD position for ventilation";

  //Boolean COF = false "Cooling ON/OFF";
  //Boolean HOF = false "Heating ON/OFF";
  Boolean EOF(start = false) "Economizer ON/OFF";
  
  Modelica.Blocks.Interfaces.RealInput uOAT "Outside Air Temperature" annotation(
    Placement(visible = true, transformation(origin = {-80, 70}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-60, 78}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput uRAT "Return Air Temperature" annotation(
    Placement(visible = true, transformation(origin = {-80, 30}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-60, 26}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput uSAT "Supply Air Temperature" annotation(
    Placement(visible = true, transformation(origin = {-80, -10}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-60, -28}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yOAD(min=0,max=1) "Outside Air Damper control signal (0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, 70}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, 80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ySAD(min=0,max=1) "Supply Air Damper control signal (0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, 50}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yRAD(min=0,max=1) "Return Air Damper control signal (0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yEAD(min=0,max=1) "Exhaust Air Damper control signal (0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, 20}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yFan(min=0) "Fan control signal (dp[Pa])" annotation(
    Placement(visible = true, transformation(origin = {30, -10}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yHeating(min=0,max=1) "Heating control signal (0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput yCooling(min=0,max=1) "Cooling control signal (0-1)" annotation(
    Placement(visible = true, transformation(origin = {30, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {70, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  /*Modelica.Blocks.Interfaces.RealInput uSATSP(min=0,max=1) "Supply Air Temperature Setpoint(optional, used when defaultSATSP=false)" annotation(
    Placement(visible = true, transformation(origin = {-80, -50}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-60, -78}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  */
equation
  //uSATSP = 273.15+20; //temp


// Controls
  yEAD = yOAD;
  yRAD = if EOF then 0 else 1; // if Economizer is on, no need to reuse return air
  ySAD = 1; // usually is openned
  //yOAD = if EOF then ((1-minOAD)*(uOAT-HSP)/(ESP-HSP) + minOAD) else minOAD; // if Economizer is on OAD opens linearly, else min position to preserve energy
  //yOAD = if EOF then 1 else minOAD; // if Economizer is on OAD fully open, else min position to preserve energy
  yFan = 800; // Fixed value for now
  //yFan = max(yHeating,yCooling);//800; // Fixed value for now
  //yHeating = if (uOAT <= HSP and uOAT >= HmaxSP) then (HSP-uOAT)/(HSP-HmaxSP) elseif (uOAT>HSP) then 0 elseif (uOAT<HmaxSP) then 1;
  //yCooling = if (uOAT <= CmaxSP and uOAT >= CSP) then (uOAT-CSP)/(CmaxSP-CSP) elseif (uOAT>CmaxSP) then 1 elseif (uOAT<CSP) then 0;
  /*if (uOAT <= HSP and uOAT >= HmaxSP) then
    yHeating = (HSP-uOAT)/(HSP-HmaxSP);
  elseif (uOAT>HSP) then
    yHeating = 0;
  elseif (uOAT<HmaxSP) then
    yHeating = 1;
  end if;
  
  if (uOAT <= CmaxSP and uOAT >= CSP) then
    yCooling = (uOAT-CSP)/(CmaxSP-CSP);
  elseif (uOAT>CmaxSP) then
    yCooling = 1;
  elseif (uOAT<CSP) then
    yCooling = 0;
  end if;*/

algorithm
/*
// Cooling ON/OFF
  if (uOAT > CSP) and ((not EOF) or (yOAD >= 1)) and (not HOF) then
    COF = true;
  else
    COF = false;
  end if;
  
// Heatinging ON/OFF
  if (uOAT < HSP) and (not COF) then
    HOF = true;
  else
    HOF = false;
  end if;
*/  
// Economizer ON/OFF
  if (uOAT < ESP) and (uOAT < uRAT) then
    EOF := true;
  else
    EOF := false;
  end if;
  
  //yOAD = if EOF then ((1-minOAD)*(uOAT-HSP)/(ESP-HSP) + minOAD) else minOAD;
  if EOF then
    if (uOAT < HSP) then
      yOAD := minOAD;
    elseif (uOAT > ESP) then
      yOAD := 1;
    else
      yOAD := ((1-minOAD)*(uOAT-HSP)/(ESP-HSP) + minOAD);
    end if;
  else
    yOAD := minOAD;
  end if;
  
  // using uRAT or uSAT seems more reasonable than uOAT
  if (uRAT>HSP) then
    yHeating := 0;
  elseif (uRAT<HmaxSP) then
    yHeating := 1;
  else
    yHeating := (HSP-uRAT)/(HSP-HmaxSP);
  end if;
  
  if (uRAT>CmaxSP) then
    yCooling := 1;
  elseif (uRAT<CSP) then
    yCooling := 0;
  else
    yCooling := (uRAT-CSP)/(CmaxSP-CSP);
  end if;
  
  /* According to book use uOAT
  if (uOAT>HSP) then
    yHeating := 0;
  elseif (uOAT<HmaxSP) then
    yHeating := 1;
  else
    yHeating := (HSP-uOAT)/(HSP-HmaxSP);
  end if;
  
  if (uOAT>CmaxSP) then
    yCooling := 1;
  elseif (uOAT<CSP) then
    yCooling := 0;
  else
    yCooling := (uOAT-CSP)/(CmaxSP-CSP);
  end if;
  */

annotation(
    Icon(graphics = {Rectangle(origin = {8, 0}, fillColor = {202, 202, 202}, fillPattern = FillPattern.Solid, extent = {{-44, 80}, {44, -80}}), Text(origin = {5, 0}, extent = {{-53, 22}, {53, -22}}, textString = "ControlUnit")
    ,
    // Name for component: annotation>Icon>graphics{}
     Text(
        extent={{-150,150},{150,110}},
        textString="%name",
        lineColor={0,0,255})
    }));
end ControlUnit;
