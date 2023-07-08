import random
import numpy as np
import matplotlib.pyplot as plt

k = int(input("Enter the value for k: "))
d = int(input("Enter the value for d: "))

def B(k, d, nodes):
    if d == 0:
        return lambda u: 1 if nodes[k] <= u < nodes[k + 1] else 0
    Bk0 = B(k, d - 1, nodes)
    Bk1 = B(k + 1, d - 1, nodes)
    return lambda u: ((u - nodes[k]) / (nodes[k + d] - nodes[k])) * Bk0(u) + ((nodes[k + d + 1] - u) / (nodes[k + d + 1] - nodes[k + 1])) * Bk1(u)

nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def calculate_points(k, d, nodes):
    b = B(k, d, nodes)
    points = []
    for u in np.arange(-1, 10, 0.05):
        points.append({"u": u, "b": b(u)})
    return points

points = calculate_points(k, d, nodes)

def draw(pts):
    plt.clf()
    for x, y in pts:
        plt.plot(x, y, 'ko')
    sample = sample_curve(pts)
    for x, y in sample:
        plt.plot(x, y, 'ro')
    for i, (x, y) in enumerate(pts):
        plt.text(x + 4, y - 4, str(i), fontsize=12)
    plt.xlim(0, 800)
    plt.ylim(0, 600)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()

def sample_curve(pts, step=0.01):
    n = len(pts)
    b = [B(k, parms['d'], nodes) for k in range(n)]
    sample = []
    for u in frange(parms['d'], n, step):
        sum_x, sum_y = 0, 0
        for k, p in enumerate(pts):
            w = b[k](u)
            sum_x += w * p[0]
            sum_y += w * p[1]
        sample.append((sum_x, sum_y))
    return sample

def frange(start, stop, step):
    current = start
    while current <= stop:
        yield current
        current += step

def create_control_points():
    width = 800
    height = 600
    pts = []
    for i in range(6):
        x = 100 + ((width - 200) / 5) * i
        y = height / 2 + (random.random() - 0.5) * (height - 200)
        pts.append((x, y))
    return pts

parms = {'d': 1}
control_points = create_control_points()
draw(control_points)

