import numpy as np
import matplotlib.pyplot as plt

# Corresponds to Figures 2.1-2.5: time series and cobweb diagrams
# for the logistic map x_{n+1} = r*x_n(1 - x_n)
# for r = 0.5, 2.8, 3.3, 3.8 and 4.0 respectively.
# This script generates one figure at a time by changing the parameter r.

def mapa_logistico(r, x):
    """One iteration of the logistic map f(x) = rx(1-x)."""
    return r * x * (1 - x)

# Parameters
r = 4       # growth rate (change to 0.5, 2.8, 3.3, 3.8 for other figures)
x0 = 0.1   # initial condition, fixed across all figures for comparability
n_iter = 50 # number of iterations, sufficient to reveal the asymptotic behaviour

# Iterate the map from x0
x_values = np.zeros(n_iter)
x_values[0] = x0
for i in range(1, n_iter):
    x_values[i] = mapa_logistico(r, x_values[i-1])
n_values = np.arange(n_iter)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: time series x_n vs n
ax1.plot(n_values, x_values, 'o-', markersize=4, color='b')
ax1.set_title(f"time series of the Logistic map (r = {r})")
ax1.set_xlabel("generation (n)")
ax1.set_ylabel("population (x_n)")
ax1.grid(True)

# Right panel: cobweb diagram
# Evaluate f(x) = rx(1-x) and the diagonal y = x on [0,1]
# with 400 equally spaced points for a smooth curve
x_rango = np.linspace(0, 1, 400)
y_rango = mapa_logistico(r, x_rango)

ax2.plot(x_rango, y_rango, 'r', label=f'f(x) = {r}x(1-x)')
ax2.plot(x_rango, x_rango, 'k', label='y = x')

# Cobweb iteration: alternate vertical segments (x -> f(x))
# and horizontal segments (f(x) -> y=x)
px, py = x0, 0
for i in range(n_iter):
    nx = px
    ny = mapa_logistico(r, nx)
    ax2.plot([px, nx], [py, ny], 'b', alpha=0.6)  # vertical segment
    ax2.plot([nx, ny], [ny, ny], 'b', alpha=0.6)  # horizontal segment
    px, py = ny, ny

ax2.set_title(f"Cobweb (r = {r})")
ax2.set_xlabel("x_n")
ax2.set_ylabel("x_{n+1}")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig(f"logistic_map_{r}.pdf", format='pdf', bbox_inches='tight')
print(f"Gráfico guardado como 'logistic_map_{r}.pdf'.")