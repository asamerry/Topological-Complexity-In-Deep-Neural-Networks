#!/usr/bin/env ./python-env/bin/python3

import random
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

random.seed(13)

def parametrize(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

def create_manifold():
    r = 3
    theta = np.linspace(0, np.pi, 250)
    phi = np.linspace(0, 2*np.pi, 500)
    theta, phi = np.meshgrid(theta, phi)
    return parametrize(r, theta, phi)

def create_data_set():
    n = 750
    r = 3.05
    rng = np.random.default_rng()
    u = rng.uniform(-1.0, 1.0, size=n)
    phi = rng.uniform(0.0, 2*np.pi, size=n)
    theta = np.arccos(u)
    return parametrize(r, theta, phi)

def d2(data_set, i, j):
    dx = data_set[0][i] - data_set[0][j]
    dy = data_set[1][i] - data_set[1][j]
    dz = data_set[2][i] - data_set[2][j]
    return dx*dx + dy*dy + dz*dz

def vietoris_rips(data_set, eps):
    x, y, z = data_set
    segments = []
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            if d2(data_set, i, j) < 4*eps*eps:
                segments.append([[x[i], y[i], z[i]], [x[j], y[j], z[j]]])
    return segments

def main():
    manifold = create_manifold()
    data_set = create_data_set()
    segments = vietoris_rips(data_set, 0.23)
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(*manifold, color="orange", alpha=0.5)
    ax.scatter(*data_set, color="black")
    if segments:
        lc = Line3DCollection(segments, colors="black", linewidths=1)
        ax.add_collection3d(lc)
    
    ax.set_box_aspect([1, 1, 1])
    plt.show()

if __name__ == "__main__":
    main()
