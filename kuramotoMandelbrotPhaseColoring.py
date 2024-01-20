import numpy as np
import matplotlib.pyplot as plt

def kuramoto_oscillators(N, K, dt, theta):
    omega = np.random.normal(0, 1, N)
    sin_diff = np.sin(theta[:, None] - theta)
    theta += dt * (omega + (K/N) * np.sum(sin_diff, axis=1))
    return theta

def mandelbrot(size=(800, 600), maxiter=50, theta=None):
    xmin, xmax, ymin, ymax = -2.5, 1.5, -1.5, 1.5
    x, y = np.meshgrid(np.linspace(xmin, xmax, size[0]), np.linspace(ymin, ymax, size[1]))
    c = x + 1j * y
    z = np.zeros_like(c, dtype=np.complex128)
    divtime = np.zeros(z.shape, dtype=int)
    color = np.zeros(z.shape)

    for i in range(maxiter):
        z = z**2 + c
        diverge = np.abs(z) > 2
        div_now = diverge & (divtime == 0)
        divtime[div_now] = i
        color[div_now] = theta[i % len(theta)] / (2*np.pi)  # Assign color based on oscillator phase
        z[diverge] = 2

    return x, y, color

# Parameters for Kuramoto model
N = 50
K = 2
dt = 0.01
theta = np.random.uniform(0, 2*np.pi, N)

# Simulate Kuramoto model for a few steps
for _ in range(100):
    theta = kuramoto_oscillators(N, K, dt, theta)

# Generate Mandelbrot set
x, y, color = mandelbrot(size=(800, 600), maxiter=50, theta=theta)

# Plotting
plt.imshow(color, extent=(-2.5, 1.5, -1.5, 1.5), cmap='hsv')
plt.colorbar()
plt.title('Mandelbrot Set with Kuramoto Model Phase-Dependent Coloring')
plt.show()
