# encs4380-dynamics--Mazion-
# encs4380-dynamics--Mazion-

Dynamic Characteristics Interactive Toolkit — ENCS4380 Interfacing Techniques, Birzeit University (Homework 1, Dr. Wasel Ghanem).

**Live site:** https://sarah-jack05.github.io/encs4380-dynamics--Mazion-/

## Team

| Member | ID | Module |
|---|---|---|
| Sarah Abd Al-Muhsen | 1230170 | Module 1,2,3,4 — python calculation then translated to js after having a problem in connecting html to python |
| Beesan Abutouq | 1230819 | Module 1,2,3,4 — plotting using python |
| Omayma Altaweel | 1230099 | Module 1,2,3,4 — html&CSS |



## What is inside

- `index.html` — the whole page: the four module cards, the four simulators and the validation table.
- `calc.js` — all the math (port of `calculations.py`): first-order step/ramp, frequency response, second-order step, poles and eigenvalues, the Module 4 random-sensor game.
- `plot.js` — every Plotly drawing (step/ramp, error fraction on a log axis, sines, Bode, s-plane, phase plane, Module 4).
- `ui.js` — sliders, buttons, the dynamic-error calculator and the six validation checks.
- `calculations.py` — the original Python reference calculations.
- `python/` — the Module 1 and 2 Jupyter/Colab simulations.
- `CSS_codes/` — page styles (`base.css`) and simulator styles (`modules.css`).

## Running it

The site is fully static: GitHub Pages serves it as-is, nothing to install and no server needed. Locally, just open `index.html` in a browser (an internet connection is needed for the Plotly and KaTeX CDNs).

## AI use

An AI coding assistant was used to port the Python calculations in `calculations.py` to `calc.js`/`plot.js`/`ui.js` and to set up this README. Every formula and validation number comes from the course lecture slides.
