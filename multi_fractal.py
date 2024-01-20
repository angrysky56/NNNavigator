import numpy as np
import matplotlib.pyplot as plt
import random

def tree_like_fractal(levels, size=(10, 10), offset=(0.5, 0.5)):
        # The fractal will be stored as a list of lines to draw
    lines = []

    # Starting line
    lines.append([(offset[0], offset[1] - size[1] / 2), (offset[0], offset[1] + size[1] / 2)])

    # Generate fractal
    for _ in range(levels):
        new_lines = []
        for line in lines:
            # Calculate midpoint
            midpoint = ((line[0][0] + line[1][0]) / 2, (line[0][1] + line[1][1]) / 2)

            # Calculate new points
            angle = random.uniform(0, np.pi / 2)
            length = size[0] / (2 ** (_ + 1))
            delta_x = length * np.cos(angle)
            delta_y = length * np.sin(angle)

            new_lines.append([midpoint, (midpoint[0] + delta_x, midpoint[1] + delta_y)])
            new_lines.append([midpoint, (midpoint[0] - delta_x, midpoint[1] + delta_y)])

        lines.extend(new_lines)

    # Extract the x and y coordinates of line endpoints
    x_coords = []
    y_coords = []
    for line in lines:
        x_coords.extend([line[0][0], line[1][0], None])  # None to break the line segment
        y_coords.extend([line[0][1], line[1][1], None])

    return x_coords, y_coords

def sierpinski_triangle(iterations):
    # Define the three vertices of the initial triangle
    vertices = [(0, 0), (0.5, 0.866), (1, 0)]
    # Start with an arbitrary point inside the triangle
    point = (0.25, 0.5)
    points = [point]

    for _ in range(iterations):
        # Randomly select one of the three triangle vertices
        vertex = random.choice(vertices)
        # Compute the midpoint between the current point and the selected vertex
        point = ((point[0] + vertex[0]) / 2, (point[1] + vertex[1]) / 2)
        points.append(point)

    return zip(*points)  # Unzip the list of points into two lists

# Number of iterations to plot the Sierpinski Triangle
iterations = 10000

# Generate the points for the Sierpinski Triangle
x, y = sierpinski_triangle(iterations)

def mandelbrot(size=(800, 600), maxiter=50):
    xmin, xmax, ymin, ymax = -2.5, 1.5, -1.5, 1.5
    dx = (xmax - xmin) / size[0]
    dy = (ymax - ymin) / size[1]

    x, y = np.meshgrid(np.linspace(xmin, xmax, size[0]), np.linspace(ymin, ymax, size[1]))
    c = x + 1j * y
    z = np.zeros_like(c, dtype=np.complex128)
    divtime = np.zeros(z.shape, dtype=int)

    for i in range(maxiter):
        z = z**2 + c
        diverge = np.abs(z) > 2  # Who is diverging
        div_now = diverge & (divtime == 0)  # Who is diverging now
        divtime[div_now] = i  # Note when
        z[diverge] = 2  # Avoid diverging too much

    return x, y, divtime

def koch_snowflake(order, scale=10):
    def koch_curve(points, order):
        if order == 0:
            return points
        else:
            new_points = []
            for i in range(0, len(points) - 1, 2):
                start, end = points[i], points[i+1]
                vec = np.array(end) - np.array(start)
                vec /= 3

                # Calculate the three new points
                p1 = start + vec
                p2 = start + vec / 2 + np.array([vec[1] * np.sqrt(3) / 2, -vec[0] * np.sqrt(3) / 2]) / 2
                p3 = start + vec * 2

                new_points.extend([start, p1, p2, p3, end])
            return koch_curve(new_points, order - 1)

    # Initial triangle points
    points = [[0, 0], [scale / 2, scale * np.sqrt(3) / 2], [scale, 0]]
    points = koch_curve(points, order)
    x, y = zip(*points)
    return x, y

def cantor_set(length, height, depth, ypos=0, line_thickness=1):
    if depth == 0:
        plt.hlines(ypos, 0, length, linewidth=line_thickness)
    else:
        plt.hlines(ypos, 0, length/3, linewidth=line_thickness)
        plt.hlines(ypos, 2*length/3, length, linewidth=line_thickness)
        cantor_set(length/3, height, depth-1, ypos - height, line_thickness)
        
def plot_fractals(figsize=(12, 9), save=False):
    plt.figure(figsize=figsize)

    # Tree-Like Fractal
    plt.subplot(2, 3, 1)  # First subplot in a 2x3 grid
    plt.title('Tree-Like Fractal')
    x, y = tree_like_fractal(levels=3, size=(10, 10), offset=[0.5, 0.5])
    plt.plot(x, y, color='blue')
    plt.axis('equal')
    plt.axis('off')

    # Sierpinski Triangle
    plt.subplot(2, 3, 2)  # Second subplot in a 2x3 grid
    plt.title('Sierpinski Triangle')
    x, y = sierpinski_triangle(iterations=10000)
    plt.scatter(x, y, color='blue', s=0.1)
    plt.axis('equal')
    plt.axis('off')

    # Mandelbrot Set
    plt.subplot(2, 3, 3)  # Third subplot in a 2x3 grid
    plt.title('Mandelbrot Set')
    x, y, divtime = mandelbrot(size=(800, 600), maxiter=50)
    plt.imshow(divtime, extent=[-2.5, 1.5, -1.5, 1.5], cmap='hot', origin='lower')
    plt.axis('off')

    # Plotting Koch Snowflake
    plt.subplot(2, 3, 4)  # Fourth subplot in a 2x3 grid
    plt.title('Koch Snowflake')
    x, y = koch_snowflake(order=4)
    plt.plot(x, y)
    plt.axis('equal')
    plt.axis('off')

    # Plotting Cantor Set
    plt.subplot(2, 3, 5)  # Fifth subplot in a 2x3 grid
    plt.title('Cantor Set')
    cantor_set(length=1, height=0.1, depth=6)
    plt.axis('equal')
    plt.axis('off')

    # The 6th subplot remains empty
    plt.subplot(2, 3, 6)
    plt.axis('off')

    plt.tight_layout()  # Adjust the layout of the plots
    if save:
        plt.savefig("fractals.png")
    else:
        plt.show()

if __name__ == "__main__":
    plot_fractals(figsize=(12, 9), save=False)
    
    
