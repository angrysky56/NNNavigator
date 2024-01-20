import numpy as np
import matplotlib.pyplot as plt

def kuramoto_oscillators(N, K, dt, theta):
    omega = np.random.normal(0, 1, N)
    sin_diff = np.sin(theta[:, None] - theta)
    theta += dt * (omega + (K/N) * np.sum(sin_diff, axis=1))
    return theta

def koch_snowflake(order, scale=10, theta=None):
    def koch_curve(points, order, theta, depth):
        if order == 0:
            return points
        else:
            new_points = []
            for i in range(0, len(points) - 1, 2):
                start, end = np.array(points[i], dtype=np.float64), np.array(points[i+1], dtype=np.float64)
                vec = (end - start) / 3.0

                angle = np.pi / 3 * np.sin(theta[depth % len(theta)])  # Vary angle based on Kuramoto phase

                # Calculate the three new points
                p1 = start + vec
                p2 = start + vec / 2.0 + np.array([np.cos(angle), np.sin(angle)]) * np.linalg.norm(vec) / np.sqrt(3)
                p3 = start + vec * 2.0

                new_points.extend([start.tolist(), p1.tolist(), p2.tolist(), p3.tolist(), end.tolist()])
            return koch_curve(new_points, order - 1, theta, depth + 1)

    # Initial triangle points
    points = [[0, 0], [scale / 2, scale * np.sqrt(3) / 2], [scale, 0], [0, 0]]
    points = koch_curve(points, order, theta, 0)
    
    # Plot each line segment with color based on Kuramoto phase
    for i in range(0, len(points) - 1, 2):
        start, end = points[i], points[i+1]
        plt.plot([start[0], end[0]], [start[1], end[1]], color=plt.cm.viridis(theta[(i//2) % len(theta)] / (2*np.pi)))

# Parameters for Kuramoto model
N = 50
K = 2
dt = 0.01
theta = np.random.uniform(0, 2*np.pi, N)

# Simulate Kuramoto model for a few steps
for _ in range(100):
    theta = kuramoto_oscillators(N, K, dt, theta)

# Generate and plot Koch snowflake
plt.figure(figsize=(8, 8))
koch_snowflake(order=5, scale=10, theta=theta)
plt.axis('equal')
plt.axis('off')
plt.show()
