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
        self.amp = np.ones(shape=(nx,ny), dtype=float)
        self.phase = np.zeros(shape=(nx,ny), dtype=float)
        self.rad = np.zeros(shape = (nx,ny,2), dtype=float)
        y = np.linspace(- (ny - 1) * 0.5 * dy, (ny - 1) * 0.5 * dy, ny)
        x = np.linspace(- (nx - 1) * 0.5 * dx, (nx - 1) * 0.5 * dx, nx)
        for i in range(ny):
            self.rad[:, i, 0] = x
        for j in range(nx):
            self.rad[j, :, 1] = y

    def set_phase_lin(self, alpha, betta):
        alpha = alpha * np.pi / 180
        betta = betta * np.pi / 180
        dphx = - 2 * np.pi / self.lamb * np.sin(alpha) * np.cos(betta)
        dphy = - 2 * np.pi / self.lamb * np.sin(alpha) * np.sin(betta)
        for i in range(self.nx):
            for j in range(self.ny):
                self.phase[i, j] = dphx * self.rad[i, j, 0] + dphy * self.rad[i, j, 1]

    def diagramm(self, theta, phi):
        f = 0
        for i in range(self.nx):
            for j in range(self.ny):
                a = self.rad[i, j, 0]*np.sin(theta)*np.cos(phi)
                b = self.rad[i, j, 1]*np.cos(theta)*np.sin(phi)
                f = f + self.amp[i, j] * np.exp(1j*((2*np.pi/self.lamb)*(a + b) + self.phase[i, j]))

        f = abs(f) ** 2
        return f
        #F = np.log10((F**2)
        #return np.heaviside(F,0)*F

    def show3d_diag(self):
        dphi, dtheta = np.pi / 300.0, np.pi / 300.0
        [phi, theta] = np.mgrid[0:np.pi:dphi, 0:2 * np.pi:dtheta]
        x = self.diagramm(theta, phi) / self.diagramm(0, 0) * np.cos(phi) * np.sin(theta)
        y = self.diagramm(theta, phi) / self.diagramm(0, 0) * np.sin(theta) * np.sin(phi)
        z = self.diagramm(theta, phi) / self.diagramm(0, 0) * np.cos(theta)
        s = mesh(x, y, z)
        return s

    def show2d_diag(self):
        theta = np.linspace(-0.5*np.pi,0.5*np.pi,1000)
        fx = self.diagramm(theta, 0)/self.diagramm(0, 0)
        fy = self.diagramm(theta, np.pi*0.5)/self.diagramm(0, 0)
        fx, fy = 10 * np.log10(fx), 10 * np.log10(fy)
        plt.plot(theta, fx)
        plt.grid(True)
        #plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.show()
        #plt.subplot(211)
        plt.plot(theta, fy)
        plt.grid(True)
        plt.show()

if __name__ == "__main__":

        aa = AntennArray(16,16,1.7,1.9,3)
        aa.set_phase_lin(0, 0)
        aa.show2d_diag()
        show()



