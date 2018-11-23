import numpy as np
from mayavi.mlab import *
import matplotlib.pyplot as plt

class AntennArray:
    def __init__(self, nx, ny, dx, dy, lamb):
        self.nx = nx
        self.ny = ny
        self.dx = dx
        self.dy = dy
        self.lamb = lamb
        self.amp = np.ones(shape=(nx,ny), dtype=int)
        self.phy = np.zeros(shape=(nx,ny), dtype=int)
        self.rad = np.zeros(shape = (nx,ny,2), dtype=float)
        y = np.linspace(- (ny - 1) * 0.5 * dy, (ny - 1) * 0.5 * dy, ny)
        x = np.linspace(- (nx - 1) * 0.5 * dx, (nx - 1) * 0.5 * dx, nx)
        for i in range(ny):
            self.rad[:, i, 0] = x
        for j in range(nx):
            self.rad[j, :, 1] = y

    def diagramm(self, theta, phi):
        f = 0
        for i in range(self.nx):
            for j in range(self.ny):
                a = self.rad[i, j, 0]*np.sin(theta)*np.cos(phi)
                b = self.rad[i, j, 1]*np.sin(theta)*np.sin(phi)
                f = f + self.amp[i, j] * np.exp((1j*2*np.pi/self.lamb)*(a + b))

        #F = abs(f)
        F = np.log10(abs(f)**2)
        return np.heaviside(F,0)*F

    def show3d_diag(self):
        dphi, dtheta = np.pi / 300.0, np.pi / 300.0
        [phi, theta] = np.mgrid[0:np.pi:dphi, 0:2 * np.pi:dtheta]
        x = self.diagramm(theta, phi) * np.cos(phi) * np.sin(theta)
        y = self.diagramm(theta, phi) * np.sin(theta) * np.sin(phi)
        z = self.diagramm(theta, phi) * np.cos(theta)
        s = mesh(x, y, z)
        return s

    def show2d_diag(self):
        theta = np.linspace(-0.5*np.pi,0.5*np.pi,1000)
        fx = self.diagramm(theta, 0)/self.diagramm(0, 0)
        fy = self.diagramm(theta, np.pi*0.5)/self.diagramm(0, 0)
        plt.subplot(211)
        plt.plot(theta, fx)
        plt.subplot(212)
        plt.plot(theta, fy)
        plt.show()


if __name__ == "__main__":

        aa = AntennArray(16,16,1.7,1.9,3)
        #print(aa.diagramm(1,0))
        aa.show3d_diag()
        show()



