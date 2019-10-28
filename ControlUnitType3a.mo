within TestSys;

model ControlUnitType3a
  // 3a:
  // Based on v3, add the option to turn off economizer, default is false
  parameter Boolean setSAT = false "Set SAT/RAT(true/false) as PID controller feedback(control SAT/RAT)";
  parameter Real minOAD = 0.2 "min OAD position for ventilation";
  parameter Real kp = 0.01 "PID proportional parameter";
  parameter Real ki = 0.01 "PID integral parameter";
  parameter Real kd = 0.1 "PID differential parameter";
  parameter Real minPower = 0.05 "Min heating/cooling power to avoid chattering";
  parameter Real maxPower = 0.8 "Limit max power of heating/cooling";
  parameter Real uFan = 25 "Assigned fan pressure(Pa)";
  
  // The following parameters are for Economizer and OAD control
  //parameter Modelica.SIunits.Temperature CSP = 273.15+18 "Cooling Setpoint";
  parameter Modelica.SIunits.Temperature HSP = 273.15+13 "Heating Setpoint";
  parameter Modelica.SIunits.Temperature ESP = 273.15+18 "Economizer Setpoint";
  //parameter Modelica.SIunits.Temperature CmaxSP = 273.15+21 "Cooling Max Setpoint";
  //parameter Modelica.SIunits.Temperature HmaxSP = 273.15+10 "Heating Max Setpoint";
  
  parameter Boolean useEconomizer = false "Whether to use economizer";
  //Boolean COF = false "Cooling ON/OFF";
  //Boolean HOF = false "Heating ON/OFF";
  Boolean EOF(start = false) "Economizer ON/OFF";
  //Real feedback(start = 0) "PID feedback";
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
  Modelica.Blocks.Interfaces.RealInput uSP(min=0,max=1) "Setpoint" annotation(
    Placement(visible = true, transformation(origin = {-80, -50}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-60, -78}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Continuous.LimPID PID(Td = kd / kp, Ti = kp /ki, k = kp,yMax = 1, yMin = -1)  annotation(
    Placement(visible = true, transformation(origin = {-20, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  
equation
/*
  if setSAT then
    feedback = uSAT;
  else
    feedback = uRAT;
  end if;
  */
//feedback = if setSAT then uSAT else uRAT;
  PID.u_m = if setSAT then uSAT else uRAT;
  PID.u_s = uSP;
// Controls
  yEAD = yOAD;
  yRAD = if EOF then 0 else 1;
// if Economizer is on, no need to reuse return air
  ySAD = 1;//yOAD;
// usually is openned
//yFan = 400*abs(PID.y) + 400; // variable fan speed(pressure Pa)
//yFan = 800; // Fixed value for now
  yFan = uFan; //
  
  yOAD = minOAD;
  EOF = false;
algorithm
// Economizer ON/OFF
  /*if useEconomizer then  
    if uOAT < uSP and uOAT < uRAT then
      EOF := true;
    else
      EOF := false;
    end if;  
    
    if EOF then
      if uOAT < uSP then
        yOAD := 1;
      elseif uOAT > uSP then
        yOAD := minOAD;
      else
        yOAD := (1 - minOAD) * (uOAT - HSP) / (ESP - HSP) + minOAD;
      end if;
    else
      yOAD := minOAD;
      //yOAD := max(1 - max(yHeating,yCooling),minOAD)
    end if;
  else
    EOF := false;
    yOAD := minOAD;
  end if;*/
  
  /*if uOAT < uRAT then
    EOF := true;
  else
    EOF := false;
  end if;  
  
  if EOF then
    if uOAT < uSP then
      yOAD := 1;
    elseif uOAT > uSP and uOAT >= uSAT then
      yOAD := minOAD;
    else
      yOAD := (1 - minOAD) * (uOAT - HSP) / (ESP - HSP) + minOAD;
    end if;
  else
    yOAD := minOAD;
    //yOAD := max(1 - max(yHeating,yCooling),minOAD)
  end if;*/
  
  yHeating := min(max(PID.y,minPower),maxPower);
// uSP - uSAT > 0  => Heating
  yCooling := min(-min(PID.y, -minPower), maxPower);
// uSP - uSAT < 0  => Cooling
  //ySAD := max(yHeating,yCooling);
  //yOAD := max(yCooling, minOAD);
// Name for component: annotation>Icon>graphics{}

annotation(
    Icon(graphics = {Rectangle(origin = {8, 0}, fillColor = {202, 202, 202}, fillPattern = FillPattern.Solid, extent = {{-44, 80}, {44, -80}}), Text(origin = {5, 0}, extent = {{-53, 22}, {53, -22}}, textString = "ControlUnit")
    ,
Text(
        extent={{-150,150},{150,110}},
        textString="%name",
        lineColor={0,0,255})
    }));
end ControlUnitType3a;
