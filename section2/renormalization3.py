import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 2.12: renormalization of the logistic map
# at the exact superstable parameters R0 and R1

# Superstable parameters:
# R0 = 2.0: the fixed point x* = 0.5 is superstable (f'(x*) = 0)
# R1 = 1 + sqrt(5) ≈ 3.236: the 2-cycle passing through x = 0.5 is superstable
R0 = 2.0
R1 = 1.0 + np.sqrt(5)

# The local rescaling factor alpha for the first renormalisation step R0 -> R1
# converges to the universal value 2.5029 as n -> infinity;
# at this first step its exact value equals R1
alpha_1 = R1

def f(x, r):  return r * x * (1 - x)
def f2(x, r): return f(f(x, r), r)

# Evaluate on a uniform grid of 1000 points over [0,1]
x = np.linspace(0, 1, 1000)
y_f_R0  = f(x, R0)
y_f2_R1 = f2(x, R1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Left panel: direct comparison of f(x, R0) and f^(2)(x, R1) ---
# Both curves pass through (0.5, 0.5) by the superstability condition
ax1.plot(x, y_f_R0,  'b-', linewidth=2,
         label=f'$f(x, R_0)$, $R_0 = 2.0$')
ax1.plot(x, y_f2_R1, 'r-', linewidth=2,
         label=f'$f^{{(2)}}(x, R_1)$, $R_1 \\approx 3.236$')
# Mark the common point (0.5, 0.5)
ax1.plot(0.5, 0.5, 'ko', markersize=6, zorder=5)

ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.legend(loc='lower left', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)

# --- Right panel: renormalisation transformation ---
ax2.plot(x, y_f_R0, 'b-', linewidth=3, label='$f(x, R_0)$', alpha=0.4)

# Apply the renormalisation operator centred at x = 0.5:
# rescale the input by 1/alpha_1 and invert the output by -alpha_1
x_zoomed     = 0.5 + (x - 0.5) / alpha_1
y_f2_zoomed  = f2(x_zoomed, R1)
y_renormalized = 0.5 - alpha_1 * (y_f2_zoomed - 0.5)

ax2.plot(x, y_renormalized, 'g--', linewidth=2.5,
         label=r'$-\alpha_1 \left[ f^{(2)}'
               r'\left(\frac{x}{\alpha_1}, R_1\right) \right]$')

ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$y$', fontsize=12)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.legend(loc='lower center', fontsize=12)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('renormalization_exact_R0_R1.pdf', dpi=300, bbox_inches='tight')
print("Imagen guardada como 'renormalization_exact_R0_R1.pdf'")