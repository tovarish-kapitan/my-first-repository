import numpy as np
from mayavi.mlab import *

def test_plot3d():
    """Generates a pretty set of lines."""
    n_mer, n_long = 6, 11
    dphi = np.pi / 1000.0
    phi = np.arange(0.0, 2 * np.pi + 0.5 * dphi, dphi)
    mu = phi * n_mer
    x = np.cos(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
    y = np.sin(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
    z = np.sin(n_long * mu / n_mer) * 0.5

    l = plot3d(x, y, z, np.sin(mu), tube_radius=0.025, colormap='Spectral')
    return l


def points_3d():
    t = np.linspace(0, 4 * np.pi, 20)

    x = np.sin(2 * t)
    y = np.cos(t)
    z = np.cos(2 * t)
    s = 2 + np.sin(t)
    u = np.empty_like(x)
    u.fill(2)
    v = np.empty_like(y)
    v.fill(0)
    w = np.empty_like(z)
    w.fill(0)
    obj = quiver3d(x, y, z, u, v, w, line_width=3, scale_factor=1)

    return points3d(x, y, z, s, colormap="copper", scale_factor=.25)
def test_quiver3d():
    x, y, z = np.mgrid[-2:3, -2:3, -2:3]
    r = np.sqrt(x ** 2 + y ** 2 + z ** 4)
    u = y * np.sin(r) / (r + 0.001)
    v = -x * np.sin(r) / (r + 0.001)
    w = np.zeros_like(z)
    obj = quiver3d(x, y, z, u, v, w, line_width=3, scale_factor=1)
    return obj


if __name__ == "__main__":
   # test_plot3d()
    points_3d()
    #test_quiver3d()
    show()