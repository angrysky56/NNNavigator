import numpy as np
import matplotlib.pyplot as plt

def kuramoto_oscillators(N, K, dt, theta):
    """
    Simulate one step of the Kuramoto model.
    """
    omega = np.random.normal(0, 1, N)
    sin_diff = np.sin(theta[:, None] - theta)
    theta += dt * (omega + (K/N) * np.sum(sin_diff, axis=1))
    return theta

def draw_tree(x, y, angle, depth, max_depth, theta):
    """
    Recursively draw a tree fractal. Branching angle is influenced by Kuramoto model.
    """
    if depth > max_depth:
        return
    branch_length = 0.5 ** depth
    new_x = x + np.cos(np.radians(angle)) * branch_length
    new_y = y + np.sin(np.radians(angle)) * branch_length

    plt.plot([x, new_x], [y, new_y], lw=max_depth-depth+1, color=plt.cm.viridis(theta[depth % len(theta)] / (2*np.pi)))

    # Recursively draw the next branches
    new_angle_variation = np.sin(theta[depth % len(theta)]) * 45  # Kuramoto influences angle
    draw_tree(new_x, new_y, angle - new_angle_variation, depth + 1, max_depth, theta)
    draw_tree(new_x, new_y, angle + new_angle_variation, depth + 1, max_depth, theta)

# Parameters for tree
max_depth = 10

# Parameters for Kuramoto model
N = 10
K = 2
dt = 0.01
theta = np.random.uniform(0, 2*np.pi, N)

# Simulate Kuramoto model for a few steps
for _ in range(100):
    theta = kuramoto_oscillators(N, K, dt, theta)

# Draw the tree fractal influenced by Kuramoto model
plt.figure(figsize=(6, 6))
draw_tree(0, 0, 90, 0, max_depth, theta)
plt.axis('off')
plt.show()
