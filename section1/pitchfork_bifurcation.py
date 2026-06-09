import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Corresponds to Figure 2.3: bifurcation diagram for the supercritical
# pitchfork bifurcation dx/dt = rx - x^3
matplotlib.use('Agg')

# Discretise the parameter range r in [-2, 2] with 400 equally spaced points
r_min, r_max = -2, 2
r = np.linspace(r_min, r_max, 400)

fig, ax = plt.subplots(figsize=(8, 6))

# --- Branch x* = 0 ---
# Stable (solid blue) for r <= 0: f'(0) = r < 0
r_stable_0 = r[r <= 0]
x_stable_0 = np.zeros_like(r_stable_0)
ax.plot(r_stable_0, x_stable_0, 'b-', linewidth=2.5, label='Stable Fixed Point')

# Unstable (dashed red) for r > 0: f'(0) = r > 0
r_unstable_0 = r[r > 0]
x_unstable_0 = np.zeros_like(r_unstable_0)
ax.plot(r_unstable_0, x_unstable_0, 'r--', linewidth=2.5, label='Unstable Fixed Point')

# --- Parabolic branches x* = ±sqrt(r) ---
# Only exist for r > 0, where the bifurcation has occurred
# Both branches are stable: f'(±sqrt(r)) = -2r < 0
r_branches = r[r > 0]
x_upper = np.sqrt(r_branches)
x_lower = -np.sqrt(r_branches)

ax.plot(r_branches, x_upper, 'b-', linewidth=2.5)
ax.plot(r_branches, x_lower, 'b-', linewidth=2.5)

# Aesthetics
ax.set_title(r'Supercritical Pitchfork Bifurcation ($\dot{x} = rx - x^3$)',
             fontsize=16)
ax.set_xlabel('Parameter $r$', fontsize=14)
ax.set_ylabel('Fixed Points $x^*$', fontsize=14)
ax.axvline(0, color='gray', linestyle=':', alpha=0.5)  # bifurcation point r = 0
ax.grid(True, linestyle='--', alpha=0.5)

# Remove duplicate legend entries arising from multiple plot calls
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('pitchfork_bifurcation.pdf', dpi=300)
