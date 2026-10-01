(*
====================================================================================
  PROJECT   : Industrial Microgrid Controller
              Intelligent Battery Energy Storage System (BESS) Dispatch
  MODULE    : FB_Microgrid_BESS_Dispatch
  PLATFORM  : IEC 61131-3 Structured Text
              Written against Siemens SCL (TIA Portal, S7-1500) syntax,
              portable to CODESYS-based substation/microgrid controllers.
  AUTHOR    : Sipho Lucky Sibanda
  CONTEXT   : A factory with rooftop solar and a behind-the-meter battery
              energy storage system needs its battery to do three jobs
              at once, in a fixed priority order: protect itself, shave
              demand peaks that drive the utility bill's single biggest
              line item, and only after that, arbitrage cheap off-peak
              energy against expensive on-peak energy. A separate,
              largely independent control loop corrects the site's
              power factor using the battery inverter's reactive power
              capability, sharing the same physical inverter's apparent
              power limit with the active power dispatch above it.

  ENGINEERING BASIS (simulated against, for realism only):
    - Demand charges: many industrial utility tariffs bill on the
      single highest 15/30-minute average kW demand in the billing
      period, not just total kWh - making "peak shaving" often the
      single largest lever a BESS has on the bill.
    - Time-of-use (TOU) energy arbitrage: charging on cheap off-peak
      energy and discharging during expensive on-peak periods.
    - Power factor correction: PF = P / sqrt(P^2 + Q^2). Utilities
      commonly penalise PF below a threshold (often 0.90-0.95);
      injecting reactive power (Q) corrects it toward unity.
    - Four-quadrant inverter capability curve: a real BESS inverter has
      one shared apparent power rating S_rated; active power (P) and
      reactive power (Q) dispatch are NOT independent - they must
      satisfy sqrt(P^2 + Q^2) <= S_rated at every instant.
====================================================================================
*)

TYPE E_RatePeriod : (PERIOD_OFFPEAK, PERIOD_SHOULDER, PERIOD_ONPEAK); END_TYPE

TYPE E_BESS_Mode :
(
    MODE_IDLE,
    MODE_PEAK_SHAVE,
    MODE_ARBITRAGE_DISCHARGE,
    MODE_ARBITRAGE_CHARGE,
    MODE_SOLAR_CHARGE,
    MODE_PROTECT
);
END_TYPE

TYPE ST_MicrogridConfig :
STRUCT
    DemandThreshold_kW           : REAL;   // Peak-shave ceiling (billing demand target)
    OnPeak_Start_hr                : REAL;   // TOU schedule, decimal hours
    OnPeak_End_hr                    : REAL;
    OffPeak_Start_hr                   : REAL;
    OffPeak_End_hr                       : REAL;
    Target_PF                              : REAL;   // e.g. 0.95
    Min_SOC_Pct                              : REAL;   // Battery health floor, e.g. 20.0
    Max_SOC_Pct                                : REAL;   // Battery health ceiling, e.g. 95.0
    Battery_Rated_kW                             : REAL;   // Max charge/discharge power
    Battery_Rated_kVA                              : REAL;   // Inverter apparent power rating
    Arbitrage_Charge_SOC_Target_Pct                  : REAL;   // Off-peak charge target
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Microgrid_BESS_Dispatch
VAR_INPUT
    Config                     : ST_MicrogridConfig;   // Downloaded from SCADA
    AI_FactoryLoad_kW            : REAL;
    AI_SolarGeneration_kW          : REAL;
    AI_BatterySOC_Pct                : REAL;
    AI_ReactivePower_kVAR              : REAL;   // Measured at the point of common coupling
    AI_HourOfDay_Decimal                 : REAL;   // 0.0-24.0, local clock time
    DI_NetMeteringAllowed                  : BOOL;   // Utility interconnection agreement
    DI_System_Enable                         : BOOL;
END_VAR

VAR_OUTPUT
    AO_Battery_ActivePower_kW    : REAL := 0.0;   // + = discharge, - = charge
    AO_Battery_ReactivePower_kVAR  : REAL := 0.0;   // + = capacitive (corrects lagging PF)
    AO_SolarCurtailment_Pct          : REAL := 0.0;   // % of solar curtailed, if export not allowed
    BESS_Mode                          : E_BESS_Mode := MODE_IDLE;
    RatePeriod                           : E_RatePeriod := PERIOD_OFFPEAK;
    Calculated_PF                          : REAL := 1.0;
    Alarm_SOC_Low                            : BOOL := FALSE;
    Alarm_SOC_High                             : BOOL := FALSE;
    Alarm_DemandExceeded                         : BOOL := FALSE;
    Alarm_PF_OutOfSpec                             : BOOL := FALSE;
    SystemStatus                                     : STRING[28] := 'STANDBY';
END_VAR

VAR
    NetLoad_kW               : REAL;   // Factory load net of solar
    Available_Discharge_kW     : REAL;
    Available_Charge_kW          : REAL;
    RequiredShave_kW                : REAL;
    GridImport_kW                     : REAL;

    // --- Reactive power / capability curve ---
    Available_S_kVA                     : REAL;   // Remaining apparent power headroom
    RequiredQ_kVAR                        : REAL;
    ActivePowerMagnitude_kW                 : REAL;
END_VAR

// ------------------------------------------------------------------
// 1. RATE PERIOD FROM TIME-OF-USE SCHEDULE
// ------------------------------------------------------------------
IF (AI_HourOfDay_Decimal >= Config.OnPeak_Start_hr) AND (AI_HourOfDay_Decimal < Config.OnPeak_End_hr) THEN
    RatePeriod := PERIOD_ONPEAK;
ELSIF (AI_HourOfDay_Decimal >= Config.OffPeak_Start_hr) OR (AI_HourOfDay_Decimal < Config.OffPeak_End_hr) THEN
    RatePeriod := PERIOD_OFFPEAK;
ELSE
    RatePeriod := PERIOD_SHOULDER;
END_IF

// ------------------------------------------------------------------
// 2. NET LOAD AND BATTERY HEADROOM (SOC / POWER LIMITS)
//    Nothing downstream is allowed to violate these regardless of
//    how attractive the economics look - battery protection comes
//    first, unconditionally.
// ------------------------------------------------------------------
NetLoad_kW := AI_FactoryLoad_kW - AI_SolarGeneration_kW;

IF AI_BatterySOC_Pct > Config.Min_SOC_Pct THEN
    Available_Discharge_kW := Config.Battery_Rated_kW;
ELSE
    Available_Discharge_kW := 0.0;
END_IF

IF AI_BatterySOC_Pct < Config.Max_SOC_Pct THEN
    Available_Charge_kW := Config.Battery_Rated_kW;
ELSE
    Available_Charge_kW := 0.0;
END_IF

Alarm_SOC_Low  := AI_BatterySOC_Pct <= Config.Min_SOC_Pct;
Alarm_SOC_High := AI_BatterySOC_Pct >= Config.Max_SOC_Pct;

// ------------------------------------------------------------------
// 3. ACTIVE POWER DISPATCH - FIXED PRIORITY ORDER
//    Peak shaving outranks arbitrage outranks solar-charging outranks
//    idle. This is the literal "when do we draw from the battery vs.
//    buy from the grid" decision tree.
// ------------------------------------------------------------------
IF NOT DI_System_Enable THEN
    AO_Battery_ActivePower_kW := 0.0;
    BESS_Mode := MODE_IDLE;

ELSIF NetLoad_kW > Config.DemandThreshold_kW THEN
    // PRIORITY 1: Peak shaving - the highest-value use of the battery,
    // because demand charges are billed on a single peak, not kWh.
    RequiredShave_kW := NetLoad_kW - Config.DemandThreshold_kW;
    IF RequiredShave_kW <= Available_Discharge_kW THEN
        AO_Battery_ActivePower_kW := RequiredShave_kW;
        Alarm_DemandExceeded := FALSE;
    ELSE
        // Battery cannot fully cover this peak - discharge everything
        // it safely can and flag the shortfall honestly rather than
        // pretending the peak was fully shaved.
        AO_Battery_ActivePower_kW := Available_Discharge_kW;
        Alarm_DemandExceeded := TRUE;
    END_IF
    BESS_Mode := MODE_PEAK_SHAVE;

ELSIF NetLoad_kW < 0.0 THEN
    // Excess solar generation beyond current factory load.
    Alarm_DemandExceeded := FALSE;
    IF Available_Charge_kW > 0.0 THEN
        AO_Battery_ActivePower_kW := MAX(NetLoad_kW, -Available_Charge_kW);   // Negative = charging
        BESS_Mode := MODE_SOLAR_CHARGE;
        AO_SolarCurtailment_Pct := 0.0;
    ELSIF NOT DI_NetMeteringAllowed THEN
        // Battery full and export not permitted by the interconnection
        // agreement - the only remaining option is to curtail solar.
        AO_Battery_ActivePower_kW := 0.0;
        BESS_Mode := MODE_PROTECT;
        AO_SolarCurtailment_Pct := 100.0 * (ABS(NetLoad_kW) / MAX(AI_SolarGeneration_kW, 0.1));
    ELSE
        AO_Battery_ActivePower_kW := 0.0;
        BESS_Mode := MODE_IDLE;
        AO_SolarCurtailment_Pct := 0.0;
    END_IF

ELSIF (RatePeriod = PERIOD_ONPEAK) AND (Available_Discharge_kW > 0.0) THEN
    // PRIORITY 2: TOU arbitrage discharge - even below the demand
    // threshold, on-peak energy is expensive enough that discharging
    // the battery instead of buying from the grid is worth doing.
    AO_Battery_ActivePower_kW := MIN(NetLoad_kW, Available_Discharge_kW);
    BESS_Mode := MODE_ARBITRAGE_DISCHARGE;
    Alarm_DemandExceeded := FALSE;

ELSIF (RatePeriod = PERIOD_OFFPEAK) AND (AI_BatterySOC_Pct < Config.Arbitrage_Charge_SOC_Target_Pct)
      AND (Available_Charge_kW > 0.0) THEN
    // PRIORITY 3: TOU arbitrage charge - buy cheap off-peak energy to
    // have capacity ready for tomorrow's peak-shaving and on-peak
    // discharge opportunities.
    AO_Battery_ActivePower_kW := -Available_Charge_kW;
    BESS_Mode := MODE_ARBITRAGE_CHARGE;
    Alarm_DemandExceeded := FALSE;

ELSE
    AO_Battery_ActivePower_kW := 0.0;
    BESS_Mode := MODE_IDLE;
    Alarm_DemandExceeded := FALSE;
END_IF

GridImport_kW := NetLoad_kW - AO_Battery_ActivePower_kW;

// ------------------------------------------------------------------
// 4. REACTIVE POWER / POWER FACTOR CORRECTION
//    Runs independently of the active-power decision above, but
//    shares the same inverter's apparent-power ceiling with it.
// ------------------------------------------------------------------
ActivePowerMagnitude_kW := ABS(AO_Battery_ActivePower_kW);
Available_S_kVA := SQRT(MAX(0.0, (Config.Battery_Rated_kVA * Config.Battery_Rated_kVA)
                                   - (ActivePowerMagnitude_kW * ActivePowerMagnitude_kW)));

IF ABS(AI_FactoryLoad_kW) > 0.01 THEN
    Calculated_PF := AI_FactoryLoad_kW
        / SQRT((AI_FactoryLoad_kW * AI_FactoryLoad_kW) + (AI_ReactivePower_kVAR * AI_ReactivePower_kVAR));
ELSE
    Calculated_PF := 1.0;
END_IF

IF Calculated_PF < Config.Target_PF THEN
    // Simplified reactive power requirement to correct toward target PF,
    // clamped to whatever apparent-power headroom the active power
    // dispatch above has left available on the shared inverter.
    RequiredQ_kVAR := AI_ReactivePower_kVAR * (1.0 - (Calculated_PF / Config.Target_PF));
    IF RequiredQ_kVAR > Available_S_kVA THEN
        AO_Battery_ReactivePower_kVAR := Available_S_kVA;
    ELSE
        AO_Battery_ReactivePower_kVAR := RequiredQ_kVAR;
    END_IF
    Alarm_PF_OutOfSpec := (AO_Battery_ReactivePower_kVAR < RequiredQ_kVAR);   // Headroom was insufficient
ELSE
    AO_Battery_ReactivePower_kVAR := 0.0;
    Alarm_PF_OutOfSpec := FALSE;
END_IF

// ------------------------------------------------------------------
// 5. STATUS TEXT
// ------------------------------------------------------------------
IF NOT DI_System_Enable THEN
    SystemStatus := 'STANDBY';
ELSIF Alarm_DemandExceeded THEN
    SystemStatus := 'PEAK SHAVE - CAPACITY LIMIT';
ELSE
    CASE BESS_Mode OF
        MODE_PEAK_SHAVE:            SystemStatus := 'PEAK SHAVING ACTIVE';
        MODE_ARBITRAGE_DISCHARGE:     SystemStatus := 'TOU ARBITRAGE - DISCHARGING';
        MODE_ARBITRAGE_CHARGE:          SystemStatus := 'TOU ARBITRAGE - CHARGING';
        MODE_SOLAR_CHARGE:                 SystemStatus := 'CHARGING FROM EXCESS SOLAR';
        MODE_PROTECT:                         SystemStatus := 'SOLAR CURTAILED - BATTERY FULL';
        ELSE                                    SystemStatus := 'IDLE';
    END_CASE
END_IF

END_FUNCTION_BLOCK
