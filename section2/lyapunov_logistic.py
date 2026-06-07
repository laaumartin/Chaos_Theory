import numpy as np
import matplotlib.pyplot as plt

# Corresponds to Figure 2.7: Lyapunov exponent for the logistic map
# x_{n+1} = r*x_n(1 - x_n) as a function of the growth rate r

# --- Simulation parameters ---
r_values = np.linspace(0.1, 4.0, 4000)  # 4000 equally spaced values of r
lyapunov = np.zeros(len(r_values))

n_transient = 1000  # transient iterations discarded before computation
n_iter = 1000       # iterations used to estimate the Lyapunov exponent

for i, r in enumerate(r_values):
    x = 0.1  # fixed initial condition across all r values

    # Phase 1: discard the transient to reach the asymptotic regime
    for _ in range(n_transient):
        x = r * x * (1 - x)

    # Phase 2: accumulate the sum of log|f'(x_i)| = log|r(1-2x)|
    # following the formula lambda = (1/n) * sum_{i=0}^{n-1} log|f'(x_i)|
    lyap_sum = 0
    for _ in range(n_iter):
        derivada = abs(r * (1 - 2 * x))
        # Avoid log(0) at superstable points where f'(x*) = 0
        # by replacing zero derivatives with a small floor value
        if derivada < 1e-12:
            lyap_sum += np.log(1e-12)
        else:
            lyap_sum += np.log(derivada)
        x = r * x * (1 - x)

    # Lyapunov exponent: time average of log|f'|
    lyapunov[i] = lyap_sum / n_iter

# --- Print key values at selected r points ---
print("--- LYAPUNOV EXPONENTS ---")
analyzed_r = [0.5, 1, 2.0, 2.8, 3, 3.2, 3.81, 3.83, 4.0]
analyzed_lyap = []

for pr in analyzed_r:
    idx = (np.abs(r_values - pr)).argmin()
    valor_lyap = lyapunov[idx]
    analyzed_lyap.append(valor_lyap)
    if pr == 2.0:
        print(f"r = {pr:.2f} -> Exponent: -inf (superstable fixed point)")
    else:
        print(f"r = {pr:.2f} -> Exponent: {valor_lyap:.4f}")
print("---------------------------------------------------------")

# --- Plot ---
plt.figure(figsize=(12, 6))

# Plot the Lyapunov exponent curve
plt.plot(r_values, lyapunov, 'k-', linewidth=0.3)

# Horizontal reference line at lambda = 0: separates stable from chaotic regimes
plt.axhline(0, color='red', linestyle='--', linewidth=1.5,
            label=r'$\lambda = 0$ (bifurcations/chaos)')

# Mark the analysed r values as blue dots
plt.scatter(analyzed_r, analyzed_lyap, color='blue', s=40, zorder=5,
            label='analysed points')

# Annotate each analysed point
for pr, pl in zip(analyzed_r, analyzed_lyap):
    if pl > -3:
        plt.annotate(f'r={pr}', (pr, pl), xytext=(0, 10),
                     textcoords='offset points', fontsize=10,
                     ha='center', color='blue')
    elif pr == 2.0:
        plt.annotate('r=2.0\n', (pr, -3), xytext=(0, 10),
                     textcoords='offset points', fontsize=10,
                     ha='center', color='blue')

# Aesthetics
plt.xlabel("Growth rate ($r$)", fontsize=12)
plt.ylabel("Lyapunov exponent ($\\lambda$)", fontsize=12)
plt.ylim(-3.5, 1.0)
plt.xlim(0, 4.0)
plt.grid(True, alpha=0.3)
plt.legend()

plt.savefig('liapunov_plot.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Gráfica guardada como 'liapunov_plot.pdf'")