import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 3.16: Grassberger-Procaccia algorithm for the Lorenz system
# Left panel: sampled points on the Lorenz attractor
# Right panel: log-log plot of C(r) vs r with linear fit for Dc

# Lorenz system: RK4 integrator
def lorenz_derivatives(state, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = state
    return np.array([sigma*(y-x), x*(rho-z)-y, x*y-beta*z])

def rk4_step(state, dt):
    k1 = lorenz_derivatives(state)
    k2 = lorenz_derivatives(state + 0.5*dt*k1)
    k3 = lorenz_derivatives(state + 0.5*dt*k2)
    k4 = lorenz_derivatives(state + dt*k3)
    return state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

# Integration parameters
dt_int = 0.01           # internal RK4 step size
tau_sample = 0.25       # sampling interval to reduce temporal correlations
N_target = 15000        # number of points sampled from the attractor
steps_per_sample = int(tau_sample / dt_int)  # 25 internal steps per saved point

# Discard transient: integrate for 5000 steps without saving
state = np.array([1.0, 1.0, 1.0])
for _ in range(5000):
    state = rk4_step(state, dt_int)

# Sample N_target points from the attractor
points = np.zeros((N_target, 3))
for i in range(N_target):
    for _ in range(steps_per_sample):
        state = rk4_step(state, dt_int)
    points[i] = state

# Grassberger-Procaccia correlation dimension
distances = pdist(points, metric='euclidean')
r_min = np.min(distances[distances > 0])
r_max = np.max(distances)
rs = np.logspace(np.log10(r_min*10), np.log10(r_max/3), 40)

# Compute correlation sum C(r) for each radius
C_r = []
total_pairs = len(distances)
for r in rs:
    C_r.append(np.sum(distances < r) / total_pairs)

C_r = np.array(C_r)
valid = C_r > 0
rs = rs[valid]
C_r = C_r[valid]

log_r  = np.log(rs)
log_Cr = np.log(C_r)

# Linear fit in the scaling region to estimate Dc
linear_region = (log_r > 0.0) & (log_r < 1.5)
slope, intercept = np.polyfit(log_r[linear_region],
                               log_Cr[linear_region], 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: sampled points on the attractor projected onto the (x,z) plane
ax1.plot(points[:, 0], points[:, 2], ',', color='royalblue',
         markersize=0.5, alpha=0.5)
ax1.set_title(f'Lorenz Attractor (Sampled Points)\n'
              f'N = {N_target}, $\\Delta\\tau$ = {tau_sample}')
ax1.set_xlabel('$x$')
ax1.set_ylabel('$z$')
ax1.grid(True, linestyle='--', alpha=0.5)

# Right panel: log-log plot of C(r) with linear fit
ax2.plot(log_r, log_Cr, 'o-', color='black', markersize=4,
         label=r'Data points $\ln C(r)$')
ax2.plot(log_r[linear_region],
         slope*log_r[linear_region] + intercept,
         color='red', linewidth=2.5,
         label=rf'Linear fit ($D_c \approx {slope:.3f}$)')
ax2.set_title('Correlation Dimension')
ax2.set_xlabel(r'$\ln(r)$')
ax2.set_ylabel(r'$\ln C(r)$')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('lorenz_grassberger_procaccia.pdf', format='pdf',
            bbox_inches='tight', dpi=300)
print(f"Dc estimated: {slope:.3f}")
