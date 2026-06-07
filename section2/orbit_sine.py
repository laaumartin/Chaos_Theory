import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 2.8: orbit diagram for the sine map
# x_{n+1} = r*sin(pi*x_n) over the range r in [0.70, 1.00]

# --- Simulation parameters ---
n_r = 8000           # number of r values (horizontal resolution)
r_min, r_max = 0.70, 1.00
n_transient = 1000   # transient iterations discarded
n_plot = 200         # iterations plotted after transient

# Discretise the parameter range
r = np.linspace(r_min, r_max, n_r)

# Initialise at a small value for all r simultaneously
x = 1e-5 * np.ones(n_r)

# Phase 1: discard the transient
for _ in range(n_transient):
    x = r * np.sin(np.pi * x)

# Phase 2: plot the attractor
fig, ax = plt.subplots(figsize=(10, 6))

for _ in range(n_plot):
    x = r * np.sin(np.pi * x)
    ax.plot(r, x, ',', color='royalblue', alpha=0.15, markersize=0.5)

# Aesthetics
ax.set_xlabel("Parameter r", fontsize=12)
ax.set_ylabel("x", fontsize=12)
ax.set_xlim(r_min, r_max)
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('orbit_diagram_sine_map.pdf', format='pdf', dpi=300,
            facecolor='white')
print("Imagen guardada como 'orbit_diagram_sine_map.pdf'")