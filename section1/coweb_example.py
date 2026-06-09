import numpy as np
import matplotlib.pyplot as plt

# Corresponds to Figure 2.1: Cobweb diagram for the map f (x) = x^2.
def plot_cobweb_x2(ax, x_range, x0, n_iter, title):
    """
    Draws a cobweb diagram for the map f(x) = x^2.

    Parameters
    ----------
    ax     : matplotlib axis object on which the diagram is drawn
    x_range: tuple (x_min, x_max) defining the plotting domain
    x0     : initial condition x_0
    n_iter : number of iterations of the cobweb algorithm
    title  : title displayed on the subplot
    """

    # Discretise the domain with 500 equally spaced points for smooth plotting
    t = np.linspace(x_range[0], x_range[1], 500)
    func = lambda x: x**2

    # Plot the map f(x) = x^2 and the diagonal y = x
    # Intersections of these two curves are the fixed points of the map
    ax.plot(t, func(t), 'b-', linewidth=2, label='$f(x) = x^2$')
    ax.plot(t, t, 'k--', linewidth=1.5, label='$y = x$')

    # Cobweb iteration: starting from x0, alternate between
    # vertical segments (x -> f(x)) and horizontal segments (f(x) -> y=x)
    x = x0
    y = 0  # initial height on the x-axis
    for _ in range(n_iter):
        fy = func(x)
        # Vertical segment from current point up to the curve y = f(x)
        ax.plot([x, x], [y, fy], 'r-', linewidth=1.2, alpha=0.7)
        # Horizontal segment from the curve back to the diagonal y = x
        ax.plot([x, fy], [fy, fy], 'r-', linewidth=1.2, alpha=0.7)
        # Mark the intersection point on the curve for clarity
        ax.plot(x, fy, 'ro', markersize=3, alpha=0.5)
        # Update: the new input is the previous output
        x, y = fy, fy

    # Axis labels, title, legend and grid
    ax.set_xlim(x_range[0], x_range[1])
    ax.set_ylim(x_range[0], x_range[1])
    ax.set_xlabel('$x_n$', fontsize=12)
    ax.set_ylabel('$x_{n+1}$', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)

# Figure illustrating the two fixed points of f(x) = x^2

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: stable fixed point x* = 0
# Initial condition x0 = 0.8, inside (0,1), converges to 0
# 10 iterations are sufficient to show clear convergence
plot_cobweb_x2(ax1, x_range=(0, 1.1), x0=0.8, n_iter=10,
               title='stable fixed point ($x^*=0$)')

# Right panel: unstable fixed point x* = 1
# Initial condition x0 = 1.05, slightly above 1, diverges away from 1
# 5 iterations are enough to show clear divergence before escaping the frame
plot_cobweb_x2(ax2, x_range=(0, 1.5), x0=1.05, n_iter=5,
               title='unstable fixed point ($x^*=1$)')

plt.tight_layout()
plt.savefig('cobweb_x2_example.pdf', dpi=300, bbox_inches='tight')
