import numpy as np
import matplotlib.pyplot as plt

# Corresponds to Figure 3.6: orbit diagram for the logistic map
# x_{n+1} = r*x_n(1 - x_n) over the range r in [3.0, 4.0]

# --- Simulation parameters ---
n_r = 10000          # number of r values (horizontal resolution of the diagram)
r_min, r_max = 3.0, 4.0
n_iteraciones = 1000  # transient iterations discarded before plotting
n_trazos = 200        # iterations plotted after the transient

# Discretise the parameter range
r = np.linspace(r_min, r_max, n_r)

# Initialise the population at a small value for all r simultaneously
x = 1e-5 * np.ones(n_r)

# --- Phase 1: discard the transient ---
# Iterate 1000 times without plotting so that the system reaches
# its asymptotic regime (fixed point, periodic orbit or chaotic attractor)
for i in range(n_iteraciones):
    x = r * x * (1 - x)

# --- Phase 2: plot the attractor ---
fig, ax = plt.subplots(figsize=(10, 6))

# Iterate 200 more times and plot each state as a black pixel
# The low alpha value (0.1) reveals density differences between
# periodic and chaotic regions
for i in range(n_trazos):
    x = r * x * (1 - x)
    ax.plot(r, x, ',k', alpha=0.1)

# Aesthetics
ax.set_title(f"Orbit diagram for the Logistic map "
             f"({r_min} $\\leq$ r $\\leq$ {r_max})")
ax.set_xlabel("growth rate (r)")
ax.set_ylabel("long-term population (x)")
ax.set_xlim(r_min, r_max)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig("orbit_diagram_logistic_map.pdf", format='pdf', dpi=300)
print("Diagrama guardado como 'orbit_diagram_logistic_map.pdf'.")
