# Non-linear Dynamical Systems with Chaotic Behaviour

This repository contains all Python scripts used to generate the figures in the Bachelor's Thesis on chaos theory and its application on rumour spreading on social media.

## Repository Structure

The repository is organised into three folders, one per chapter of the thesis.

```
├── section1/
│   ├── results/
│   ├── coweb_example.py
│   ├── phase_portrait_1d_example.py
│   ├── phase_portrait_2d_example.py
│   ├── phase_portrait_rabbits_vs_sheep.py
│   └── pitchfork_bifurcation.py
│
├── section2/
│   ├── results/
│   ├── cobweb_logistic.py
│   ├── dimension_logistic.py
│   ├── dimension_lorenz1.py
│   ├── lorenz_attractor.py
│   ├── lyapunov_logistic.py
│   ├── orbit_logistic.py
│   ├── orbit_sine.py
│   ├── renormalization.py
│   ├── renormalization2.py
│   └── renormalization3.py
│
└── section3/
    ├── results/
    ├── SEIR-MLE.py
    ├── SEIR-bifurcation.py
    └── SEIR-phase-portrait.py
```

## Description

### Section 1 — Basic concepts of dynamical systems
Scripts corresponding to the figures in Chapter 2 of the thesis.

- **coweb_example.py** — Cobweb diagram for the map f(x) = x², illustrating the stability of its fixed points (Figure 2.1).
- **phase_portrait_1d_example.py** — Vector field and phase portrait for the one-dimensional system dx/dt = sin(x) (Figure 2.2).
- **pitchfork_bifurcation.py** — Bifurcation diagram for the supercritical pitchfork bifurcation dx/dt = rx - x³ (Figure 2.3).
- **phase_portrait_2d_example.py** — Phase portrait for a linear two-dimensional system with a saddle point (Figure 2.4).
- **phase_portrait_rabbits_vs_sheep.py** — Phase portrait for the Lotka-Volterra competition model (Figure 2.5).

### Section 2 — Chaos Theory
Scripts corresponding to the figures in Chapter 3 of the thesis.

- **cobweb_logistic.py** — Time series and cobweb diagrams for the logistic map for r = 0.5, 2.8, 3.3, 3.8 and 4.0 (Figures 3.1-3.5). To generate the figure for a different value of r, change the parameter at the top of the script.
- **orbit_logistic.py** — Orbit diagram for the logistic map (Figure 3.6).
- **lyapunov_logistic.py** — Lyapunov exponent for the logistic map as a function of the growth rate r (Figure 3.7).
- **orbit_sine.py** — Orbit diagram for the sine map x_{n+1} = r*sin(pi*x_n) (Figure 3.8).
- **renormalization.py** — Renormalization of the logistic map at r = 3.4: comparison of f(x) and f^(2)(x) (Figure 3.10).
- **renormalization2.py** — Renormalization of the second iterate at r = 3.55: comparison of f^(2)(x) and f^(4)(x) (Figure 3.11).
- **renormalization3.py** — Renormalization at the exact superstable parameters R0 and R1 (Figure 3.12).
- **dimension_logistic.py** — Correlation dimension analysis of the logistic map at the Feigenbaum accumulation point r_inf ≈ 3.5699456 (Figure 3.15).
- **dimension_lorenz1.py** — Grassberger-Procaccia algorithm for the Lorenz system (Figure 3.16).
- **lorenz_attractor.py** — Global view of the Lorenz strange attractor with sigma=10, rho=28, beta=8/3 (Figure 3.17).

### Section 3 — Simulating Chaotic Behaviour: an application on rumour spreading on social media.
Scripts corresponding to the figures in Chapter 4 of the thesis.

- **SEIR-bifurcation.py** — Bifurcation diagrams for the seasonally forced SEIR model for four parameter configurations (Figures 4.1-4.5). To generate the diagram for a different case, change the parameters at the top of the script.
- **SEIR-MLE.py** — Maximal Lyapunov exponent for the forced SEIR model for four parameter configurations (Figures 4.6-4.9). To generate the figure for a different case, change the parameters at the top of the script.
- **SEIR-phase-portrait.py** — Phase portrait and time series for Case 2 of the forced SEIR model, for four values of the forcing amplitude epsilon (Figures 4.10-4.13). To generate the figure for a different epsilon, change the parameter at the top of the script.

## Requirements

All scripts are written in Python 3 and require the following libraries:

```
numpy
scipy
matplotlib
pandas
```

They can be installed with:

```bash
pip install numpy scipy matplotlib pandas
```

## Output

Each script saves its output as a PDF file in the `results/` subfolder of the corresponding section. No graphical display is required; all figures are saved directly to disk.

## Licence

This work is licensed under Creative Commons Attribution – Non Commercial – Non Derivatives.
