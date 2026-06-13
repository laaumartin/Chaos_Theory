import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 3.15: correlation dimension analysis of the logistic map
# at the Feigenbaum accumulation point r ≈ 3.56994567


# Parameters 
r = 3.56994567
N_target = 10000
N_transient = 10000  # long transient to ensure convergence to the fractal attractor

# Discard the transient starting from the critical point x0 = 0.5
x_current = 0.5
for _ in range(N_transient):
    x_current = r * x_current * (1 - x_current)

# Record N_target points from the attractor
trajectory = np.zeros(N_target)
for i in range(N_target):
    x_current = r * x_current * (1 - x_current)
    trajectory[i] = x_current

# 2D embedding: (x_n, x_{n+1}) to compute pairwise distances
# This is the standard delay embedding used by Grassberger and Procaccia
points = np.column_stack((trajectory[:-1], trajectory[1:]))

# Grassberger-Procaccia correlation sum
distances = pdist(points, metric='euclidean')
r_min = np.min(distances[distances > 0])
r_max = np.max(distances)

# Evaluate C(r) over 40 logarithmically spaced values of r
rs = np.logspace(np.log10(r_min * 10), np.log10(r_max / 3), 40)

C_r = []
total_pairs = len(distances)
for rad in rs:
    C_r.append(np.sum(distances < rad) / total_pairs)

C_r = np.array(C_r)
valid = C_r > 0
rs    = rs[valid]
C_r   = C_r[valid]

log_r  = np.log(rs)
log_Cr = np.log(C_r)

# Linear fit in the fractal scaling region of the Cantor-like attractor
linear_region = (log_r > -4.5) & (log_r < -2.0)
if np.sum(linear_region) > 2:
    slope, intercept = np.polyfit(log_r[linear_region],
                                   log_Cr[linear_region], 1)
else:
    slope = 0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: fractal dust in the (x_n, x_{n+1}) embedding space
ax1.plot(points[:, 0], points[:, 1], 'o', markersize=0.5,
         color='darkblue', alpha=0.5)
ax1.set_title(f'Logistic Map ($r = {r}$)')
ax1.set_xlabel('$x_n$')
ax1.set_ylabel('$x_{{n+1}}$')
ax1.grid(True, linestyle='--', alpha=0.5)

# Right panel: log-log plot of C(r) with linear fit
ax2.plot(log_r, log_Cr, 'o-', color='black', markersize=4,
         label=r'Data points $\ln C(r)$')
ax2.plot(log_r[linear_region],
         slope * log_r[linear_region] + intercept,
         color='red', linewidth=2.5,
         label=rf'Linear fit ($D_c \approx {slope:.3f}$)')
ax2.set_title('Correlation Dimension of the Logistic Map')
ax2.set_xlabel(r'$\ln(r)$')
ax2.set_ylabel(r'$\ln C(r)$')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('logistic_feigenbaum_dimension.pdf', format='pdf',
            bbox_inches='tight', dpi=300)
print(f"Imagen guardada. Dc estimada: {slope:.3f} (esperado: ~0.500)")
