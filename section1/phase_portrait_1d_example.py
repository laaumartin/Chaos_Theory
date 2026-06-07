import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Corresponds to Figure 1.2: vector field and phase portrait for dx/dt = sin(x)
matplotlib.use('Agg')

# Define the vector field f(x) = sin(x)
def f(x):
    return np.sin(x)

# Discretise the domain with 500 equally spaced points over [-2.5pi, 2.5pi]
# The extended domain ensures all relevant fixed points and flow arrows are visible
x = np.linspace(-2.5*np.pi, 2.5*np.pi, 500)
y = f(x)

fig, ax = plt.subplots(figsize=(10, 6))

# Plot the vector field f(x) = sin(x)
ax.plot(x, y, label=r'$\dot{x} = \sin(x)$', color='blue', linewidth=2, alpha=0.6)
ax.axhline(0, color='black', linewidth=1)

# Fixed points: sin(x) = 0 at x = k*pi for k in Z
# Unstable fixed points (even k): open red circles
unstable_points = [0, 2*np.pi, -2*np.pi]
stable_points = [np.pi, -np.pi]

ax.plot(unstable_points, [0]*len(unstable_points), 'ro', markersize=12,
        markerfacecolor='white', markeredgewidth=2.5,
        label='Unstable Fixed Point (Source)', zorder=10)

# Stable fixed points (odd k): filled green circles
ax.plot(stable_points, [0]*len(stable_points), 'go', markersize=12,
        label='Stable Fixed Point (Sink)', zorder=10)

# Flow arrows between fixed points (green)
# Placed at representative interior points of each interval between fixed points
# Direction determined by the sign of sin(x) on each interval
arrow_props_flow = dict(head_width=0.15, head_length=0.3,
                        fc='green', ec='green', alpha=0.7, width=0.02)
ax.arrow(np.pi/2, 0, 0.5, 0, **arrow_props_flow)    # (0, pi): sin > 0, flow right
ax.arrow(1.5*np.pi, 0, -0.5, 0, **arrow_props_flow)  # (pi, 2pi): sin < 0, flow left
ax.arrow(-np.pi/2, 0, -0.5, 0, **arrow_props_flow)   # (-pi, 0): sin < 0, flow left
ax.arrow(-1.5*np.pi, 0, 0.5, 0, **arrow_props_flow)  # (-2pi,-pi): sin > 0, flow right

# Repulsion arrows at unstable fixed points (red)
# Two arrows per unstable point, one in each direction, to emphasise instability
arrow_props_unstable = dict(head_width=0.12, head_length=0.25,
                            fc='red', ec='red', width=0.03, zorder=9)
dx_arrow = 0.4  # arrow length from the fixed point

for point in unstable_points:
    ax.arrow(point + 0.1, 0, dx_arrow, 0, **arrow_props_unstable)   # rightward
    ax.arrow(point - 0.1, 0, -dx_arrow, 0, **arrow_props_unstable)  # leftward

# Axis formatting
plt.xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
           [r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$'], fontsize=12)
plt.yticks(fontsize=12)
ax.set_xlabel('x', fontsize=16)
ax.set_ylabel(r'$\dot{x}$', fontsize=16, rotation=0, labelpad=15)
ax.set_title(r'Vector Field and Phase Portrait for $\dot{x} = \sin(x)$',
             fontsize=18, pad=20)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper right', frameon=True, shadow=True)
ax.set_xlim(-2.5*np.pi, 2.5*np.pi)
ax.set_ylim(-1.2, 1.4)

plt.tight_layout()
plt.savefig('sine_phase_portrait_with_unstable_arrows.pdf', dpi=300)