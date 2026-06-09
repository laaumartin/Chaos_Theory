import numpy as np
import matplotlib.pyplot as plt

# Corresponds to Figure 2.5: phase portrait for the Lotka-Volterra
# competition model (Rabbits vs. Sheep)
# dx/dt = x(3 - x - 2y), dy/dt = y(2 - x - y)

# Build a uniform 100x100 grid over [0, 3.5] x [0, 3.5]
w = 3.5
Y, X = np.mgrid[0:w:100j, 0:w:100j]

# Evaluate the vector field at each grid point
U = X * (3 - X - 2*Y)   # dx/dt
V = Y * (2 - X - Y)     # dy/dt

fig, ax = plt.subplots(figsize=(6, 6))

# Streamplot of the vector field: flow lines are curves tangent to
# (dx/dt, dy/dt) at every point, computed via ax.streamplot()
ax.streamplot(X, Y, U, V, density=1.5, color='gray', linewidth=0.8, arrowsize=1)

# Nullclines
x_vals = np.linspace(0, 4, 100)

# x-nullcline: dx/dt = 0 => x = 0 (vertical axis)
# or 3 - x - 2y = 0 => y = (3-x)/2 (blue dashed)
ax.plot([0, 0], [0, w], 'b--', label='x-nullcline')
ax.plot(x_vals, (3 - x_vals) / 2, 'b--')

# y-nullcline: dy/dt = 0 => y = 0 (horizontal axis)
# or 2 - x - y = 0 => y = 2 - x (green dashed)
ax.plot([0, w], [0, 0], 'g--', label='y-nullcline')
ax.plot(x_vals, 2 - x_vals, 'g--')

# Fixed points: (0,0), (0,2), (3,0) are stable nodes (black)
# (1,1) is a saddle point (red), since Delta < 0 at that point
fps = [(0, 0), (0, 2), (3, 0), (1, 1)]
for point in fps:
    color = 'red' if point == (1, 1) else 'black'
    ax.plot(point[0], point[1], 'o', color=color, markersize=8, zorder=10)

# Aesthetics
ax.set_xlabel('Rabbits (x)', fontsize=14)
ax.set_ylabel('Sheep (y)', fontsize=14)
ax.set_xlim(0, 3.5)
ax.set_ylim(0, 2.5)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('rabbits_sheep.pdf', dpi=300)
print("Imagen guardada como 'rabbits_sheep.pdf'")
