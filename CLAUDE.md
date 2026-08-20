# EV Comparison Project

## Overview

Interactive visualization tool for comparing electric vehicles sold new in Sweden (last verified August 2026). Uses a parallel coordinates plot to compare EVs across multiple dimensions.

## Files

- `evs.yaml` - EV dataset with 195 vehicles, specs, pricing (SEK), and references
- `index.html` - D3.js visualization with interactive parallel coordinates plot

## Data Structure

Each EV entry in `evs.yaml` contains:
- **Identity**: make, model, submodel, year
- **Size**: segment (ev-database.org segment code, e.g. `JC`; the letter gives the size class - A: Mini, B: Compact, C: Medium, D: Large, E: Executive, F: Luxury, N: Passenger Van, S: Sports - and a leading `J` means SUV body)
- **Pricing**: price_sek (Swedish Krona)
- **Range/Battery**: range_km_wltp, battery_kwh
- **Charging**: dc_charge_max_kw, charge_10_80_min
- **Performance**: power_hp, acceleration_0_100, top_speed_kmh, drive
- **Practical**: cargo_liters, seats, tow_capacity_kg
- **Meta**: notes, references (for verification)

## Current Makes

Audi, BMW, BYD, Cupra, Ford, Hyundai, Jeep, Kia, Mercedes-Benz, MG, Mini, Nissan, Peugeot, Polestar, Porsche, Renault, Skoda, Smart, Subaru, Tesla, Toyota, Volkswagen, Volvo

## Data Sources

- Primary: [ev-database.org](https://ev-database.org) - verified specs
- Secondary: Manufacturer websites (audi.se, etc.), Swedish dealers

## Running the Visualization

```bash
python -m http.server 8000
```
Then open http://localhost:8000

## Visualization Features

- Parallel coordinates across: Price, Range, Battery, Charge Speed, Charge Time, Power, Acceleration, Top Speed, Cargo, Seats, Tow Capacity
- Color by: Make (brand-inspired colors), Drive type, or Seats
- Interactive filtering via brush selection on axes
- Size filter (ev-database.org size classes derived from segment codes; toggle chips in the Filters section)
- Legend toggle to show/hide brands (click to toggle, Hide All/Show All buttons)
- Click axis labels to invert scale (e.g., Price)
- Fuzzy hover detection (20px hitarea on PC, 8px on touch devices)
- Touch/iPad support with tap to select

## Brand Colors

Colors are brand-inspired while maintaining visual distinction:
- Audi: Red, BMW: Blue, BYD: Soft pink, Cupra: Copper
- Ford: Violet, Hyundai: Cyan, Jeep: Olive, Kia: Orange
- Mercedes-Benz: Silver, MG: Racing green, Mini: Lime
- Nissan: Warm grey, Peugeot: Indigo, Polestar: Ice blue, Porsche: Burgundy
- Renault: Yellow, Skoda: Green, Smart: Teal, Subaru: Blue
- Tesla: Magenta-red, Toyota: Deep orange
- Volkswagen: Dark blue, Volvo: Blue-grey

## Maintenance

When updating EV data:
1. Verify specs against ev-database.org or manufacturer sites
2. Use usable battery capacity (not nominal)
3. Use WLTP range values
4. Swedish prices from official Swedish sites (e.g., audi.se)
5. Update the "Verified" date in evs.yaml header
