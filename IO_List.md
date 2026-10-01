# I/O List — Industrial Microgrid Controller (BESS Dispatch)

**Project:** Intelligent Battery Energy Storage System Dispatch
**Author:** Sipho Lucky Sibanda
**Target platform:** Siemens S7-1500 (TIA Portal / SCL) — portable to a CODESYS-based
substation/microgrid controller

## Configuration Parameters (downloaded from SCADA)

| Field                       | Description                              | Typical Value |
|----------------------------------|---------------------------------------------|------------------|
| `DemandThreshold_kW`               | Peak-shave ceiling (billing demand target)      | 800 kW             |
| `OnPeak_Start_hr` / `OnPeak_End_hr`  | On-peak tariff window                              | 14.0 / 20.0           |
| `OffPeak_Start_hr` / `OffPeak_End_hr`  | Off-peak tariff window                                | 22.0 / 6.0               |
| `Target_PF`                              | Minimum acceptable power factor                          | 0.95                       |
| `Min_SOC_Pct` / `Max_SOC_Pct`               | Battery health limits                                       | 20.0 / 95.0                   |
| `Battery_Rated_kW`                            | Maximum charge/discharge power                                 | 500 kW                           |
| `Battery_Rated_kVA`                              | Inverter apparent power rating                                    | 550 kVA                             |
| `Arbitrage_Charge_SOC_Target_Pct`                  | Target SOC to reach during off-peak charging                         | 90.0 %                                 |

## Inputs

| Tag Name                    | Description                                | Signal Type      | Range / Units       |
|---------------------------------|------------------------------------------------|--------------------|-------------------------|
| `AI_FactoryLoad_kW`               | Factory active power demand (main meter)          | 4-20mA               | 0-2000 kW                 |
| `AI_SolarGeneration_kW`             | Rooftop solar PV active power output                 | 4-20mA                 | 0-1000 kW                   |
| `AI_BatterySOC_Pct`                   | Battery state of charge                                 | CAN/Modbus from BMS       | 0-100 %                       |
| `AI_ReactivePower_kVAR`                 | Reactive power at the point of common coupling            | 4-20mA                      | -500 to +500 kVAR               |
| `AI_HourOfDay_Decimal`                     | Local clock time, decimal hours                              | From RTC                       | 0.0-24.0                          |
| `DI_NetMeteringAllowed`                       | Utility interconnection agreement permits export                | Digital (24VDC)                    | 0/1                                    |
| `DI_System_Enable`                                | Master enable                                                      | Digital (24VDC)                      | 0/1                                      |

## Outputs

| Tag Name                       | Description                              | Signal Type      |
|-------------------------------------|------------------------------------------------|--------------------|
| `AO_Battery_ActivePower_kW`           | Battery active power command (+discharge / -charge) | 4-20mA (bipolar) |
| `AO_Battery_ReactivePower_kVAR`         | Battery reactive power command (PF correction)          | 4-20mA (bipolar) |
| `AO_SolarCurtailment_Pct`                 | Commanded solar curtailment when export is blocked          | 4-20mA |
| `BESS_Mode`                                  | Current dispatch mode (enumeration)                             | Internal / HMI tag |
| `RatePeriod`                                    | Current tariff period (enumeration)                                | Internal / HMI tag |
| `Calculated_PF`                                    | Site power factor as measured at the PCC                             | REAL, HMI trend |
| `Alarm_SOC_Low` / `Alarm_SOC_High`                    | Battery approaching its protective SOC limits                            | Digital x2 |
| `Alarm_DemandExceeded`                                   | Battery could not fully cover a peak-shaving event                          | Digital |
| `Alarm_PF_OutOfSpec`                                        | Inverter reactive headroom insufficient to hit target PF                       | Digital |
| `SystemStatus`                                                 | Human-readable status text                                                        | STRING |

## Notes for reviewers

- **Active and reactive power dispatch share one inverter's apparent power rating.**
  `Available_S_kVA` is computed from the *remaining* headroom after active power is
  already committed — this reflects a real four-quadrant inverter's capability curve
  (`sqrt(P² + Q²) ≤ S_rated`), not two independent power outputs.
- **The dispatch priority order is fixed and deliberate**: battery protection limits,
  then peak shaving, then TOU arbitrage, then solar self-consumption, then idle. See
  the project manual, Chapter 5, for why this specific order reflects real BESS
  economics rather than an arbitrary choice.
- `Alarm_DemandExceeded` is raised **honestly** whenever the battery cannot fully cover
  a peak — the function block never silently under-reports how much shaving was
  actually achieved.
