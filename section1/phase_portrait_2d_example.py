import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Corresponds to Figure 1.4: phase portrait for the linear system
# dx/dt = x + y, dy/dt = 4x - 2y, which has a saddle point at the origin
matplotlib.use('Agg')

# Define the linear vector field
# Matrix A = [[1, 1], [4, -2]], eigenvalues lambda_1 = 2, lambda_2 = -3
def sys(X, Y):
    u = X + Y       # dx/dt = x + y
    v = 4*X - 2*Y   # dy/dt = 4x - 2y
    return u, v

# Build a uniform 100x100 grid over [-4, 4] x [-4, 4]
w = 4
Y, X = np.mgrid[-w:w:100j, -w:w:100j]
U, V = sys(X, Y)

fig, ax = plt.subplots(figsize=(8, 8))

# Streamplot of the vector field
# density=1.5 provides enough flow lines to reveal the saddle structure
# without overcrowding the figure
ax.streamplot(X, Y, U, V, color='royalblue', linewidth=1.2,
              arrowsize=1.5, arrowstyle='->', density=1.5)

# Eigenvector directions (manifolds through the origin)
x_vals = np.array([-w, w])

# Unstable manifold: eigenvector v1 = (1,1) for lambda_1 = 2, slope = 1
y_vals_v1 = x_vals * 1
ax.plot(x_vals, y_vals_v1, 'r--', linewidth=2.5,
        label=r'Unstable Manifold ($v_1$)')

# Stable manifold: eigenvector v2 = (1,-4) for lambda_2 = -3, slope = -4
y_vals_v2 = x_vals * -4
ax.plot(x_vals, y_vals_v2, 'r-.', linewidth=2.5,
        label=r'Stable Manifold ($v_2$)')

# Fixed point at the origin
ax.plot(0, 0, 'ko', markersize=8, zorder=10, label='Fixed Point (Saddle)')

# Aesthetics
ax.set_xlim(-w, w)
ax.set_ylim(-w, w)
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$y$', fontsize=14)
ax.set_title(r'Phase Portrait: Saddle Point ($\Delta < 0$)', fontsize=16)
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('saddle_point_phase_portrait.pdf', dpi=300)