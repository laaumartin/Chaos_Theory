import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 3.10: renormalization of the logistic map at r = 3.4
# Left panel: f(x) and f^(2)(x) with a green box around the central peak of f^(2)
# Right panel: the rescaled and inverted central peak overlaid on f(x)

r = 3.4
x_center = 0.5  # maximum of the logistic map

def f(x):
    """Logistic map f(x) = rx(1-x)"""
    return r * x * (1 - x)

def f2(x):
    """Second iterate f(f(x))"""
    return f(f(x))

# Evaluate both functions on a uniform grid of 1000 points over [0,1]
x = np.linspace(0, 1, 1000)
y1 = f(x)
y2 = f2(x)

# Define the green box around the central peak of f^(2)(x)
box_width = 0.35
box_height = 0.45
box_x = x_center - box_width / 2
y_min = f2(x_center)
box_y = y_min - 0.02

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left panel: f(x) and f^(2)(x) with the green box 
ax1.plot(x, y1, 'b-', linewidth=2, label='$f(x)$')
ax1.plot(x, y2, 'r-', linewidth=2, label='$f^{(2)}(x)$')
ax1.plot(x, x, 'k--', alpha=0.3)  # diagonal y = x for reference

# Green dashed rectangle marking the central peak of f^(2)(x) to be renormalised
rect = patches.Rectangle((box_x, box_y), box_width, box_height,
                          linewidth=1.5, edgecolor='green', facecolor='none',
                          linestyle='--', zorder=5)
ax1.add_patch(rect)

ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.legend(loc='lower right', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)

# Right panel: renormalised central peak overlaid on f(x) 
ax2.plot(x, y1, 'b-', linewidth=2, label='$f(x)$', alpha=0.5)

# Extract f^(2)(x) restricted to the box domain
x_box = np.linspace(box_x, box_x + box_width, 400)
y_box = f2(x_box)

# Apply the renormalisation transformation:
# horizontal rescaling: stretch the box to fill [0,1] centred at x=0.5
scale_x = 1.0 / box_width
x_zoomed = 0.5 + (x_box - 0.5) * scale_x

# vertical rescaling and inversion: flip the peak upward to match f(x)
y_max_orig = f(0.5)
scale_y = y_max_orig / (box_y + box_height - y_min)
y_flipped = y_max_orig - (y_box - y_min) * scale_y

ax2.plot(x_zoomed, y_flipped, 'g--', linewidth=2.5,
         label=r'$-\alpha f^{(2)}\left(\frac{x}{\alpha}\right)$')

ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$y$', fontsize=12)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.legend(loc='lower center', fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('renormalization_side_by_side.pdf', dpi=300, bbox_inches='tight')
print("Imagen guardada como 'renormalization_side_by_side.pdf'")
