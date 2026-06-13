import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint

# Corresponds to Figures 4.6 - 4.9: maximal Lyapunov exponent
# for the seasonally forced SEIR model for rumour spread on
# social media, for four different parameter configurations (Cases 1-4).
# Method: Benettin et al. (1980) — single perturbation with periodic renormalisation.
# Lambda = 0 indicates a periodic orbit.
# Lambda < 0 indicates a stable fixed point or limit cycle.
# To generate the figure for a different case, change ONLY
# the parameters in the "User parameters" section below


# User parameters (change these for each case)

mu         = 0.02           # demographic turnover rate (yr^-1)
sigma      = 365.0 / 8.0    # E->I transition rate (yr^-1), latency ~8 days
gamma      = 73.0           # disengagement rate (yr^-1), mean ~5 days
case_label      = 'Case 2'
output_filename = 'lyapunov_case2'   # extension added automatically below

# Case 1: mu=0.10,  sigma=365/3,  gamma=120, case_label='Case 1', output='lyapunov_case1'
# Case 2: mu=0.02,  sigma=365/8,  gamma=73,  case_label='Case 2', output='lyapunov_case2'
# Case 3: mu=0.01,  sigma=365/15, gamma=36,  case_label='Case 3', output='lyapunov_case3'
# Case 4: mu=0.005, sigma=365/25, gamma=18,  case_label='Case 4', output='lyapunov_case4'

# Fixed parameters (common to all cases)
beta0 = 1241.0        # baseline transmission rate (yr^-1)
omega = 2.0 * np.pi   # annual forcing frequency (rad/yr)

# Time structure
t_transient  = 950      # years discarded as transient
t_lyapunov   =  50      # years used for lambda computation
tau          =  0.01    # renormalisation interval (years, ~3.6 days)
                        # short enough to keep trajectories in the linear regime
n_steps      = int(t_lyapunov / tau)   # number of renormalisation steps
pts_per_step = 50       # integration points per renormalisation interval

delta0 = 1e-8           # initial perturbation magnitude (applied to S)

y0 = [0.06, 0.001, 0.001]   # fixed initial condition for all runs

# SEIR model 
def forced_seir(y, t, eps):
    """
    Right-hand side of the forced SEIR system.

    Parameters
    ----------
    y   : list [S, E, I] - current state (fractions of total population)
    t   : float          - current time (years)
    eps : float          - forcing amplitude
    """
    S = max(y[0], 0)
    E = max(y[1], 0)
    I = max(y[2], 0)
    beta_t = beta0 * (1.0 - eps * np.cos(omega * t))
    dS = mu * (1.0 - S) - beta_t * S * I
    dE = beta_t * S * I - (mu + sigma) * E
    dI = sigma * E - (mu + gamma) * I
    return [dS, dE, dI]

# Benettin method for one value of eps 
def compute_lyapunov(eps):
    """
    Returns the maximal Lyapunov exponent (yr^-1) for a given eps,
    using the Benettin renormalisation algorithm.

    Steps:
      1. Integrate the reference trajectory for t_transient years
         to reach the attractor.
      2. Initialise the shadow trajectory by perturbing S by delta0.
      3. Over t_lyapunov years, alternate between:
           a. Integrating both trajectories for tau years.
           b. Measuring the distance d between them.
           c. Accumulating log(d / delta0).
           d. Rescaling the shadow trajectory back to distance delta0
              from the reference, in the same direction.
      4. Return lambda = accumulated_sum / t_lyapunov.

    Renormalisation steps where d grows by more than a factor of 1e6
    relative to delta0 are discarded to avoid numerical errors.
    """

    # Step 1: reach the attractor
    t_trans   = np.linspace(0, t_transient, t_transient * pts_per_step)
    sol_trans = odeint(forced_seir, y0, t_trans,
                       args=(eps,), atol=1e-10, rtol=1e-8, hmax=0.02)
    y_ref = sol_trans[-1].copy()
    t_now = t_transient

    # Step 2: initialise shadow trajectory
    y_shad = y_ref + np.array([delta0, 0.0, 0.0])

    # Steps 3-4: integrate, measure, renormalise
    log_sum    = 0.0
    n_accepted = 0

    for _ in range(n_steps):
        t_seg = np.linspace(t_now, t_now + tau, pts_per_step + 1)

        sol_ref  = odeint(forced_seir, y_ref,  t_seg,
                          args=(eps,), atol=1e-10, rtol=1e-8, hmax=0.02)
        sol_shad = odeint(forced_seir, y_shad, t_seg,
                          args=(eps,), atol=1e-10, rtol=1e-8, hmax=0.02)

        y_ref  = sol_ref[-1].copy()
        y_shad = sol_shad[-1].copy()

        diff = y_shad - y_ref
        d    = np.linalg.norm(diff)

        if d == 0:
            # Trajectories collapsed: reinitialise perturbation
            y_shad = y_ref + np.array([delta0, 0.0, 0.0])
        elif d / delta0 > 1e6:
            # Numerical blowup: discard this step and reinitialise
            y_shad = y_ref + delta0 * (diff / d)
        else:
            log_sum    += np.log(d / delta0)
            n_accepted += 1
            # Renormalise shadow back to distance delta0
            y_shad = y_ref + delta0 * (diff / d)

        t_now += tau

    if n_accepted == 0:
        return 0.0
    return log_sum / t_lyapunov   # yr^-1

# Sweep over epsilon
eps_vals  = np.linspace(0.0, 0.30, 120)
lyap_vals = []

print(f"Computing Lyapunov exponents for {case_label}...")
print(f"  {len(eps_vals)} values of eps, {n_steps} renormalisation steps each\n")

for i, eps in enumerate(eps_vals):
    lam = compute_lyapunov(eps)
    lyap_vals.append(lam)
    if i % 20 == 0 or i == len(eps_vals) - 1:
        print(f"  eps = {eps:.3f}  ->  lambda = {lam:+.4f} yr^-1")

lyap_vals = np.array(lyap_vals)

# Save raw values
df = pd.DataFrame({"epsilon": eps_vals, "lambda_yr": lyap_vals})
df.to_csv(f"{output_filename}.csv", index=False)
print(f"\nSaved: {output_filename}.csv")

# Figure
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#f8f9fa')

# Colour points by sign: red = chaos (lambda > 0), teal = stable (lambda <= 0)
colors = np.where(lyap_vals > 0, '#E53935', '#00897B')
ax.scatter(eps_vals, lyap_vals, c=colors, s=18, zorder=3, edgecolors='none')

# Reference line at lambda = 0
ax.axhline(0, color='#333333', linewidth=1.2, linestyle='--',
           zorder=2, label=r'$\lambda = 0$')

ax.set_title(
    rf"Maximal Lyapunov exponent — {case_label}"
    "\n"
    rf"($\gamma={gamma},\ \sigma={sigma:.1f},\ \mu={mu},\ \beta_0={beta0}$)",
    fontsize=12, fontweight='bold', color='#222222', pad=10
)
ax.set_xlabel(r"Algorithmic forcing amplitude ($\varepsilon$)",
              fontsize=11, fontweight='bold', color='#333333')
ax.set_ylabel(r"Maximal Lyapunov exponent $\lambda$  (yr$^{-1}$)",
              fontsize=11, fontweight='bold', color='#333333')
ax.set_xlim(0, 0.30)
ax.grid(True, color='white', linewidth=1.3, zorder=1)
ax.legend(fontsize=9, framealpha=0.9)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#cccccc')

plt.tight_layout()
plt.savefig(f"{output_filename}.png", dpi=180, bbox_inches='tight')
print(f"Saved: {output_filename}.png")
plt.close()

# Summary
n_chaos = (lyap_vals > 0).sum()
print(f"\nSummary for {case_label}:")
print(f"  Values with lambda > 0 (chaos): {n_chaos} / {len(eps_vals)}")
if n_chaos > 0:
    print(f"  First chaos onset at eps ~ {eps_vals[lyap_vals > 0][0]:.3f}")
    print(f"  Max lambda = {lyap_vals.max():.4f} yr^-1")
print(f"  Min lambda = {lyap_vals.min():.4f} yr^-1")
