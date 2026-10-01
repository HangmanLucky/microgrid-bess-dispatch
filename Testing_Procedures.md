# Functional Test Procedure — Microgrid BESS Dispatch

**Project:** Industrial Microgrid Controller (Intelligent BESS Dispatch)
**Document type:** Factory Acceptance Test (FAT) — simulated / desktop validation
**Author:** Sipho Lucky Sibanda

| # | Test Case | Precondition | Action | Expected Result | Pass/Fail |
|---|------------|----------------|---------|--------------------|-------------|
| 1 | Peak shaving engages above threshold | Net load exceeds `DemandThreshold_kW`, SOC healthy | Observe | `BESS_Mode = MODE_PEAK_SHAVE`; battery discharges exactly the excess above threshold | |
| 2 | Peak shaving respects SOC floor | Net load exceeds threshold, `AI_BatterySOC_Pct <= Min_SOC_Pct` | Observe | `Available_Discharge_kW = 0`; `Alarm_DemandExceeded = TRUE`; battery does not discharge | |
| 3 | Honest shortfall reporting | Required shave exceeds `Battery_Rated_kW` | Observe | Battery discharges at its full rated power; `Alarm_DemandExceeded = TRUE` reflects the shortfall | |
| 4 | Excess solar charges the battery first | `NetLoad_kW < 0`, SOC below max | Observe | `BESS_Mode = MODE_SOLAR_CHARGE`; battery charges at the lesser of excess solar or rated charge power | |
| 5 | Curtailment only when battery full and export blocked | `NetLoad_kW < 0`, SOC at max, `DI_NetMeteringAllowed = FALSE` | Observe | `BESS_Mode = MODE_PROTECT`; `AO_SolarCurtailment_Pct > 0` | |
| 6 | No curtailment when export is allowed | Same as Test 5 but `DI_NetMeteringAllowed = TRUE` | Observe | `AO_SolarCurtailment_Pct = 0`; excess exports to the grid instead | |
| 7 | On-peak arbitrage discharge below threshold | Net load below threshold, `RatePeriod = PERIOD_ONPEAK`, SOC healthy | Observe | `BESS_Mode = MODE_ARBITRAGE_DISCHARGE`; battery still discharges to offset grid import | |
| 8 | Off-peak arbitrage charging | `RatePeriod = PERIOD_OFFPEAK`, SOC below arbitrage target | Observe | `BESS_Mode = MODE_ARBITRAGE_CHARGE`; battery charges toward `Arbitrage_Charge_SOC_Target_Pct` | |
| 9 | Shoulder period defaults to idle | Net load below threshold, shoulder period, SOC already at arbitrage target | Observe | `BESS_Mode = MODE_IDLE`; no unnecessary cycling | |
| 10 | PF correction within inverter headroom | PF below target, ample apparent-power headroom remaining | Observe | `AO_Battery_ReactivePower_kVAR` corrects toward target; `Alarm_PF_OutOfSpec = FALSE` | |
| 11 | PF correction limited by active power dispatch | PF below target during a large peak-shave event (little headroom left) | Observe | Reactive dispatch clamped to `Available_S_kVA`; `Alarm_PF_OutOfSpec = TRUE` if insufficient | |
| 12 | System disable forces safe idle | `DI_System_Enable = FALSE` | Observe | `AO_Battery_ActivePower_kW = 0`; `BESS_Mode = MODE_IDLE` | |

## Why Test 11 matters as much as Test 10

A four-quadrant inverter's active and reactive power outputs are not independent —
they share one apparent-power ceiling. Test 10 alone could pass with logic that
treats P and Q as separate, unlimited outputs; Test 11 specifically proves the
capability-curve constraint is enforced, which is the difference between a
plausible-looking simulation and one that would actually respect real inverter
hardware limits.

## How to exercise these tests without physical hardware

As with the rest of this portfolio, these cases were run by forcing input tags in a
PLCSIM-style watch table (or an equivalent CODESYS soft-PLC harness), sweeping load,
solar, SOC, and time-of-day values to exercise the full dispatch priority chain
rather than only single fixed points.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Test performed by | Sipho Lucky Sibanda | |
| Reviewed by | | |
