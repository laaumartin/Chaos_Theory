import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import find_peaks

# Corresponds to Figures 4.1 - 4.4: bifurcation diagrams for
# the seasonally forced SEIR model for rumour spread on social media.
# To generate the diagram for a different case, change ONLY
# the parameters in the "User parameters" section below.
# The model is:
#   dS/dt = mu*(1-S) - beta(t)*S*I
#   dE/dt = beta(t)*S*I - (mu+sigma)*E
#   dI/dt = sigma*E - (mu+gamma)*I
#
# with time-varying transmission rate:
#   beta(t) = beta0 * (1 - epsilon * cos(2*pi*t))   [t in years]
#
# The bifurcation diagram records the local maxima of I(t) in
# the stationary regime as a function of the forcing amplitude
# epsilon, plotted on a log10 scale.

# User parameters (change these for each case) 

mu        = 0.02          # demographic turnover rate (yr^-1)
sigma     = 365.0 / 8.0   # E->I transition rate (yr^-1), latency ~8 days
gamma     = 73.0          # disengagement rate (yr^-1), mean ~5 days
case_label     = 'Case 2'
output_filename = '02_bifurcation.png'

# Case 1: mu=0.10,  sigma=365/3,  gamma=120, case_label='Case 1', output='01_bifurcation.png'
# Case 2: mu=0.02,  sigma=365/8,  gamma=73,  case_label='Case 2', output='02_bifurcation.png'
# Case 3: mu=0.01,  sigma=365/15, gamma=36,  case_label='Case 3', output='03_bifurcation.png'
# Case 4: mu=0.005, sigma=365/25, gamma=18,  case_label='Case 4', output='04_bifurcation.png'

# Fixed parameters (common to all cases)
beta0 = 1241.0        # baseline transmission rate (yr^-1)
omega = 2.0 * np.pi   # annual forcing frequency (rad/yr)

# Time windows
t_transient = 950     # years discarded as transient
t_sample    =  50     # years used for analysis
total_years = t_transient + t_sample
pts_per_yr  = 500     # time points per year (resolution)

t_full = np.linspace(0, total_years, total_years * pts_per_yr)
y0     = [0.06, 0.001, 0.001]   # fixed initial condition for all runs

# SEIR model 
def forced_seir(y, t, eps, mu, sigma, gamma):
    """
    Right-hand side of the forced SEIR system.

    Parameters
    ----------
    y     : list [S, E, I] - current state (fractions of total population)
    t     : float          - current time (years)
    eps   : float          - forcing amplitude
    mu    : float          - demographic turnover rate (yr^-1)
    sigma : float          - E->I transition rate (yr^-1)
    gamma : float          - disengagement rate (yr^-1)
    """
    S = max(y[0], 0)
    E = max(y[1], 0)
    I = max(y[2], 0)
    beta_t = beta0 * (1.0 - eps * np.cos(omega * t))
    dS = mu * (1.0 - S) - beta_t * S * I
    dE = beta_t * S * I - (mu + sigma) * E
    dI = sigma * E - (mu + gamma) * I
    return [dS, dE, dI]

# Bifurcation computation
n_eps   = 250          # number of epsilon values (horizontal resolution)
eps_max = 0.30         # maximum forcing amplitude

eps_vals  = np.linspace(0.0, eps_max, n_eps)
eps_plot, I_plot = [], []
idx_start = t_transient * pts_per_yr   # index where stationary regime begins

print(f"Computing bifurcation diagram for {case_label} ({n_eps} values of epsilon)...")
for i, eps in enumerate(eps_vals):
    if i % 60 == 0:
        print(f"  epsilon = {eps:.3f}  ({i}/{n_eps})")

    sol = odeint(
        forced_seir, y0, t_full,
        args=(eps, mu, sigma, gamma),
        atol=1e-10, rtol=1e-8, hmax=0.02
    )
    # Extract the stationary part of the I(t) time series
    I_steady = sol[idx_start:, 2]

    # Identify local maxima and record their log10 values
    peaks, _ = find_peaks(I_steady)
    for p in peaks:
        v = I_steady[p]
        if v > 1e-16:   # discard numerical zeros
            eps_plot.append(eps)
            I_plot.append(np.log10(v))

print(f"  {len(eps_plot)} peaks recorded.")

# Figure
fig, ax = plt.subplots(figsize=(11, 6))
ax.set_facecolor('#f8f9fa')

ax.scatter(eps_plot, I_plot, s=5, color='#008080', alpha=0.45,
           edgecolors='none',
           label='Peaks of I (stationary regime)', zorder=2)

ax.set_title(
    f"Bifurcation diagram – Forced SEIR model for rumour spread\n"
    f"{case_label} parameters: "
    rf"$\mu={mu},\ \sigma={sigma:.1f},\ \gamma={gamma},\ "
    rf"\beta_0={beta0}$,  annual forcing cycle",
    fontsize=11, fontweight='bold', pad=12, color='#222222'
)
ax.set_xlabel(r"Algorithmic forcing amplitude ($\varepsilon$)",
              fontsize=11, fontweight='bold', color='#333333')
ax.set_ylabel(r"Viral peaks  $\log_{10}(I^*)$",
              fontsize=11, fontweight='bold', color='#333333')
ax.set_xlim(0, 0.30)
ax.set_ylim(-16, -2)
ax.grid(True, color='white', linewidth=1.4, zorder=1)
ax.legend(loc='lower left', fontsize=9, framealpha=0.92, ncol=2)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#cccccc')

plt.tight_layout()
plt.savefig(output_filename, dpi=180, bbox_inches='tight')
print(f"Saved: {output_filename}")
plt.close()
