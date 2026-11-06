# PhysChem Calculator

A small tkinter desktop app for Physical Chemistry A1 (Zhejiang University of Science and Technology), built step by step while learning Python.

## Run

```bash
python3 physchem2.py
```

Requires Python 3 and tkinter. On Ubuntu / WSL:

```bash
sudo apt install python3-tk
```

## Versions

- `physchem.py` (v1): 4 formula tools — Ideal Gas, Gibbs Energy, Clausius-Clapeyron, Molar Mass from Freezing Point.
- `physchem2.py` (v2): the same 4 tools with step-by-step working, plus a Unit Converter (pressure / volume / energy / temperature) and Common Tables (gas constant R, water constants, vaporisation enthalpies, unit relations).

## Roadmap

- Fill in the missing Chapter 1-4 formula tools (First Law Q/W/U/H, entropy, Raoult/Henry, colligative properties).
- Per-field unit selection (automatic unit handling inside each tool).
- Symbolic layer with SymPy (partial derivatives, Maxwell relations).
- Automated solving: pick a problem type, the app handles formula choice, unit conversion, steps, and the result.
