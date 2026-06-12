import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Script to compute the 'repetition error' of the time series for epsilon = 0.19, 
# which is in the bistable / period-2 regime. 
# The repetition error is computed by comparing I(t) with I(t - 2 years) 
# over a window of 10 years, and calculating the maximum absolute difference.

# ── Fixed Parameters ──
mu, beta0, sigma, gamma, omega = 0.02, 1241.0, 365.0/8.0, 73.0, 2.0*np.pi
t_transient, t_sample = 950, 50
pts_per_yr = 200
total_years = t_transient + t_sample
t_full = np.linspace(0, total_years, total_years * pts_per_yr)

y0 = [0.06, 0.001, 0.001] # Initial condition
eps = 0.19

def forced_seir(y, t):
    S, E, I = max(y[0], 0), max(y[1], 0), max(y[2], 0)
    beta_t = beta0 * (1.0 - eps * np.cos(omega * t))
    return [mu*(1.0-S) - beta_t*S*I, beta_t*S*I - (mu+sigma)*E, sigma*E - (mu+gamma)*I]

print(f"Integrating epsilon = {eps}...")
sol = odeint(forced_seir, y0, t_full, atol=1e-17, rtol=1e-8, hmax=0.02)

# Extract the stationary regime (last 50 years)
idx_start = t_transient * pts_per_yr
I_steady = sol[idx_start:, 2]
t_steady = t_full[idx_start:]

# compute the "repetition error" by comparing I(t) with I(t - 2 years)
shift_indices = 2 * pts_per_yr

# Take a window of 10 years to compare
window_start = 10 * pts_per_yr  # Year 960
window_end = 20 * pts_per_yr    # Year 970

I_original = I_steady[window_start:window_end]
I_shifted  = I_steady[window_start - shift_indices : window_end - shift_indices]
t_window   = t_steady[window_start:window_end]

# Calculate the maximum absolute numerical error
max_error = np.max(np.abs(I_original - I_shifted))
print(f"  -> Maximum error when shifting by 2 years (eps={eps}): {max_error:.2e}")

# ── Plot ──
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('#f8f9fa')
ax.set_facecolor('#f8f9fa')

# Original line (Thicker to show the dashed line perfectly embedded)
ax.plot(t_window, I_original, color='#5C2D6D', linewidth=3.5, label='I(t) Original')
# Shifted "ghost" line
ax.plot(t_window, I_shifted, color='black', linestyle='--', linewidth=1.5, 
        label='I(t - 2 years)')

ax.set_title(r"Repetition Test: Bistability ($\varepsilon = 0.19$)" + f"\nMaximum Error = {max_error:.1e}", 
             fontweight='bold', pad=12)
ax.set_xlabel("Time (Years)", fontweight='bold')
ax.set_ylabel("Infected Fraction (I)", fontweight='bold')
ax.grid(True, color='white', linewidth=1.4)
ax.legend(loc='upper right')
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('repetition_test.png', dpi=300)
print("\nSaved: repetition_test.png")
