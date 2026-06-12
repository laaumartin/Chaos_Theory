import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# ============================================================
# Numerical Convergence Analysis for the Forced SEIR Model
# Testing the effect of absolute tolerance (atol) on long-term
# integration accuracy for the fractional population scale.
# ============================================================

# ── Parameters ──
epsilon = 0.19
mu = 0.02
beta0 = 1241.0
sigma = 365.0 / 8.0
gamma = 73.0
omega = 2.0 * np.pi

t_transient = 950
t_sample = 50
total_years = t_transient + t_sample
pts_per_yr = 200
t_full = np.linspace(0, total_years, total_years * pts_per_yr)

# Initial condition for the trajectory that showed sensitivity (E0 = 0.001)
y0 = [0.06, 0.001, 0.001]

# ── Model ──
def forced_seir(y, t):
    S = max(y[0], 0)
    E = max(y[1], 0)
    I = max(y[2], 0)
    beta_t = beta0 * (1.0 - epsilon * np.cos(omega * t))
    dS = mu * (1.0 - S) - beta_t * S * I
    dE = beta_t * S * I - (mu + sigma) * E
    dI = sigma * E - (mu + gamma) * I
    return [dS, dE, dI]

# ── Convergence Test ──
atols = [1e-10, 1e-14, 1e-17, 1e-19]
sols = []

print(f"Running numerical convergence test for epsilon = {epsilon}")
print(f"Initial conditions: {y0}\n")

for tol in atols:
    print(f"Integrating with atol = {tol}...")
    sol = odeint(forced_seir, y0, t_full, atol=tol, rtol=1e-8, hmax=0.02)
    sols.append(sol)

# Extract the stationary regime (last 50 years)
idx_start = t_transient * pts_per_yr
t_plot = t_full[idx_start:]

# ── Calculate Differences ──
print("\nMaximum difference between successive tolerances (last 50 years):")
for i in range(len(atols)-1):
    diff = np.max(np.abs(sols[i+1][idx_start:, 2] - sols[i][idx_start:, 2]))
    print(f"  |atol({atols[i]}) - atol({atols[i+1]})| = {diff:.2e}")

# ── Plot ──
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_facecolor('#f8f9fa')

# Colors and line weights to make the overlap obvious
colors = ['#E53935', '#FB8C00', '#43A047', '#1E88E5']
lineweights = [4, 2.5, 1.5, 0.8]

for i, tol in enumerate(atols):
    I_t = sols[i][idx_start:, 2]
    ax.plot(t_plot, I_t, color=colors[i], linewidth=lineweights[i], alpha=0.8,
            label=f'atol = {tol}')

ax.set_title(f"Numerical Convergence Test ($\epsilon = {epsilon}$, $E(0) = 0.001$)", 
             fontweight='bold', pad=12)
ax.set_xlabel("Time (Years)", fontweight='bold')
ax.set_ylabel("Infected Fraction (I)", fontweight='bold')
ax.set_xlim(t_transient, total_years)
ax.legend(loc='upper right')
ax.grid(True, color='white', linewidth=1.4)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('convergence_test.png', dpi=300)
print("\nSaved: convergence_test.png")
