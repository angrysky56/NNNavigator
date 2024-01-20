import numpy as np
import matplotlib.pyplot as plt

def kuramoto_oscillators(N, K, dt, theta):
    omega = np.random.normal(0, 1, N)
    sin_diff = np.sin(theta[:, None] - theta)
    theta += dt * (omega + (K/N) * np.sum(sin_diff, axis=1))
    return theta

def cantor_set(length, height, depth, ypos=0, line_thickness=1, theta=None, depth_counter=0):
    if depth == 0:
        plt.hlines(ypos, 0, length, linewidth=line_thickness, color=plt.cm.viridis(theta[depth_counter % len(theta)] / (2*np.pi)))
    else:
        # Adjust the position of the cut based on the Kuramoto phase
        cut_position = 1/3 + np.sin(theta[depth_counter % len(theta)]) * 1/6
        plt.hlines(ypos, 0, cut_position * length, linewidth=line_thickness, color=plt.cm.viridis(theta[depth_counter % len(theta)] / (2*np.pi)))
        plt.hlines(ypos, (1 - cut_position) * length, length, linewidth=line_thickness, color=plt.cm.viridis(theta[depth_counter % len(theta)] / (2*np.pi)))

        cantor_set(cut_position * length, height, depth-1, ypos - height, line_thickness, theta, depth_counter + 1)
        cantor_set(cut_position * length, height, depth-1, ypos - height, line_thickness, theta, depth_counter + 1)

# Parameters for Kuramoto model
N = 10
K = 2
dt = 0.01
theta = np.random.uniform(0, 2*np.pi, N)

# Simulate Kuramoto model for a few steps
for _ in range(100):
    theta = kuramoto_oscillators(N, K, dt, theta)

# Generate and plot Cantor set
plt.figure(figsize=(10, 5))
cantor_set(length=1, height=0.1, depth=6, ypos=0, line_thickness=2, theta=theta)
plt.axis('off')
plt.show()
