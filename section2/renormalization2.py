import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.use('Agg')

# Corresponds to Figure 2.11: renormalization of the second iterate at r = 3.55
# Left panel: f^(2)(x) and f^(4)(x) with a green box around the central peak
# Right panel: the rescaled and inverted central peak overlaid on f^(2)(x)

r = 3.55  # parameter value where the stable 4-cycle exists
x_center = 0.5

def f(x):  return r * x * (1 - x)
def f2(x): return f(f(x))
def f4(x): return f2(f2(x))

# Evaluate on a uniform grid of 1000 points over [0.1, 0.9]
x = np.linspace(0.1, 0.9, 1000)
y2 = f2(x)
y4 = f4(x)

# Green box around the central peak of f^(4)(x)
box_x = 0.35
box_width = 0.3
box_y = 0.33
box_height = 0.21

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Left panel: f^(2)(x) and f^(4)(x) with the green box ---
# f^(2)(x) plays the role of the "parent" function
# f^(4)(x) is the "child" function whose central peak will be renormalised
ax1.plot(x, y2, 'b-', linewidth=2, label='$f^{(2)}(x)$')
ax1.plot(x, y4, 'r-', linewidth=2, label='$f^{(4)}(x)$')

rect = patches.Rectangle((box_x, box_y), box_width, box_height,
                          linewidth=1.5, edgecolor='green', facecolor='none',
                          linestyle='--', zorder=5)
ax1.add_patch(rect)

ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_xlim(0.1, 0.9)
ax1.set_ylim(0, 1)
ax1.legend(loc='upper left', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)

# --- Right panel: renormalised central peak of f^(4) overlaid on f^(2) ---
ax2.plot(x, y2, 'b-', linewidth=2, label='$f^{(2)}(x)$', alpha=0.5)

# Extract f^(4)(x) restricted to the box domain
x_box = np.linspace(box_x, box_x + box_width, 400)
y_box = f4(x_box)

# Renormalisation transformation: horizontal rescaling centred at x=0.5
scale_x = (0.83 - 0.17) / box_width
x_zoomed = 0.5 + (x_box - 0.5) * scale_x

# Vertical rescaling and inversion to match the shape of f^(2)(x)
y_min_f2 = f2(0.5)
y_max_f2 = f2(0.17)
box_y_max = f4(0.5)

scale_y = (y_max_f2 - y_min_f2) / (box_y_max - np.min(y_box))
y_flipped = y_min_f2 + (box_y_max - y_box) * scale_y

ax2.plot(x_zoomed, y_flipped, 'g--', linewidth=2.5,
         label=r'$-\alpha f^{(4)}\left(\frac{x}{\alpha}\right)$')

ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$y$', fontsize=12)
ax2.set_xlim(0.1, 0.9)
ax2.set_ylim(0, 1)
ax2.legend(loc='lower center', fontsize=11)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('renormalization_f2_f4.pdf', dpi=300, bbox_inches='tight')
print("Imagen guardada como 'renormalization_f2_f4.pdf'")