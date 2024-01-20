import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

def kuramoto_oscillators(N, K, dt, theta):
    omega = np.random.normal(0, 1, N)
    sin_diff = np.sin(theta[:, None] - theta)
    theta += dt * (omega + (K/N) * np.sum(sin_diff, axis=1))
    return theta

def draw_sierpinski(points, depth, max_depth, theta, ax):
    if depth > max_depth:
        return

    # Draw the triangle
    triangle = tri.Triangulation(points[:, 0], points[:, 1])
    ax.fill(triangle.x, triangle.y, color=plt.cm.viridis(theta[depth % len(theta)] / (2*np.pi)))

    # New points for the smaller triangles
    p1 = (points[0] + points[1]) / 2
    p2 = (points[1] + points[2]) / 2
    p3 = (points[0] + points[2]) / 2

    # Recursively draw the next triangles
    draw_sierpinski(np.array([points[0], p1, p3]), depth+1, max_depth, theta, ax)
    draw_sierpinski(np.array([p1, points[1], p2]), depth+1, max_depth, theta, ax)
    draw_sierpinski(np.array([p3, p2, points[2]]), depth+1, max_depth, theta, ax)

# Parameters for Sierpinski triangle
max_depth = 6
initial_points = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])

# Parameters for Kuramoto model
N = 10  # Number of oscillators
K = 2   # Coupling strength
dt = 0.01
theta = np.random.uniform(0, 2*np.pi, N)

# Simulate Kuramoto model for a few steps
for _ in range(100):
    theta = kuramoto_oscillators(N, K, dt, theta)

# Draw the Sierpinski triangle influenced by Kuramoto model
fig, ax = plt.subplots()
draw_sierpinski(initial_points, 0, max_depth, theta, ax)
ax.set_aspect('equal')
ax.axis('off')
plt.show()
