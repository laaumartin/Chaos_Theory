import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figures 3.10 - 3.13: phase portrait and time
# series for the seasonally forced SEIR model (Case 2), for four values of the forcing amplitude epsilon.
# To generate the figure for a different epsilon, change ONLY
# the value in the "User parameters" section below.

# User parameters (change these for each figure)

epsilon         = 0.28
output_filename = 'phase_portrait_eps028.pdf'

# Fixed parameters (Case 2)
mu    = 0.02
beta0 = 1241.0
sigma = 365.0 / 8.0
gamma = 73.0
omega = 2.0 * np.pi
# N     = 5000000     # total population size


# Time structure 
t_transient = 950       # years discarded as transient
t_sample    =  50       # years used for analysis
total_years = t_transient + t_sample
pts_per_yr  = 200       # integration points per year

t_full = np.linspace(0, total_years, total_years * pts_per_yr)

# Initial conditions 
S0   = 0.06 
I0   = 0.001 
E0_1 = 0.01    # trajectory 1
E0_2 = 0.001     # trajectory 2

y0_1 = [S0, E0_1, I0]
y0_2 = [S0, E0_2, I0]

# SEIR model
def forced_seir(y, t):
    S = max(y[0], 0)
    E = max(y[1], 0)
    I = max(y[2], 0)
    beta_t = beta0 * (1.0 - epsilon * np.cos(omega * t))
    dS = mu * (1.0 - S) - beta_t * S * I
    dE = beta_t * S * I - (mu + sigma) * E
    dI = sigma * E - (mu + gamma) * I
    return [dS, dE, dI]

# Integration
print(f"Integrating trajectory 1 (E0 = {E0_1})...")
sol1 = odeint(forced_seir, y0_1, t_full, atol=1e-17, rtol=1e-8, hmax=0.02)

print(f"Integrating trajectory 2 (E0 = {E0_2})...")
sol2 = odeint(forced_seir, y0_2, t_full, atol=1e-17, rtol=1e-8, hmax=0.02)
# Extract the stationary regime (last t_sample years)
idx_start = t_transient * pts_per_yr
t_plot = t_full[idx_start:]   # runs from 950 to 1000

S1, E1, I1 = sol1[idx_start:].T
S2, E2, I2 = sol2[idx_start:].T

# Log10 transformation for phase portrait
log_S1 = np.log10(np.maximum(S1, 1e-18))
log_E1 = np.log10(np.maximum(E1, 1e-18))
log_I1 = np.log10(np.maximum(I1, 1e-18))

log_S2 = np.log10(np.maximum(S2, 1e-18))
log_E2 = np.log10(np.maximum(E2, 1e-18))
log_I2 = np.log10(np.maximum(I2, 1e-18))

# Figure
color_1 = '#D4B847'   # yellow: E(0) = 0.01N
color_2 = '#5C2D6D'   # purple: E(0) = 0.001N

fig = plt.figure(figsize=(14, 6))

# Left panel: 3D phase portrait in log10 scale
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot(log_S1, log_E1, log_I1, color=color_1, linewidth=0.6,
         label='E(0)=0.01')
ax1.plot(log_S2, log_E2, log_I2, color=color_2, linewidth=1.5,
         label='E(0)=0.001')
ax1.set_xlabel('Susceptibles (log10)')
ax1.set_ylabel('Exposed (log10)')
ax1.set_zlabel('Infected (log10)')
ax1.set_title(f'Phase Portrait\n(Last {t_sample} years)',
              fontweight='bold')
ax1.legend()
ax1.view_init(elev=20, azim=-55)

# Right panel: time series of I(t) with real year labels (950-1000)
ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(t_plot, I1, color=color_1, linewidth=1.5, label='E(0)=0.01')
ax2.plot(t_plot, I2, color=color_2, linewidth=1.5, label='E(0)=0.001')
ax2.set_xlim(t_transient, total_years)
ax2.set_ylim(bottom=0)
ax2.set_xlabel('Time (Years)')
ax2.set_ylabel('Infected Fraction (I)')
ax2.set_title(f'Time Series of Infected Fraction\n(Last {t_sample} years)',
              fontweight='bold')
ax2.ticklabel_format(useOffset=False, style='plain')
ax2.grid(True, alpha=0.5)
ax2.legend()

plt.subplots_adjust(wspace=0.3)
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Saved: {output_filename}")
plt.close()
