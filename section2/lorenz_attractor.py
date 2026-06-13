import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 3.17: global view of the Lorenz strange attractor
# sigma=10, rho=28, beta=8/3 

sigma = 10.0
rho   = 28.0
beta  = 8.0 / 3.0

def lorenz(t, state):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

# Integrate over t in [0, 100] with 100000 evaluation points
# using the adaptive RK45 method, which automatically controls
# the local truncation error at each step
t_span = (0, 100)
t_eval = np.linspace(0, 100, 100000)
initial_state = [1.0, 1.0, 1.0]

sol = solve_ivp(lorenz, t_span, initial_state,
                t_eval=t_eval, method='RK45')
x, y, z = sol.y

# Discard the first 2000 points as transient to ensure
# the trajectory has converged to the attractor
x = x[2000:]
y = y[2000:]
z = z[2000:]

fig = plt.figure(figsize=(10, 8))
ax  = fig.add_subplot(111, projection='3d')

# Plot the trajectory as a very thin line to reveal the
# fine structure of the attractor without obscuring it
ax.plot(x, y, z, color='#003366', linewidth=0.15, alpha=0.6)

ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$y$', fontsize=14)
ax.set_zlabel('$z$', fontsize=14)

# Camera angle chosen to display both wings of the butterfly clearly
ax.view_init(elev=25, azim=-45)

plt.tight_layout()
plt.savefig('lorenz_global.pdf', dpi=300, bbox_inches='tight')
