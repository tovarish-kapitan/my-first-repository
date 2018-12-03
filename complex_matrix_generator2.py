import numpy as np
import math


class OurMatrix2:
    def __init__(self, xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize):

        self.data = np.ndarray(shape=(xdim, ydim, frames,), dtype=complex)  # массив комплексных матриц
        dt = 2 * np.pi / frames
        x_max = np.zeros(shape=(4))
        y_max = np.zeros(shape=(4))
        #self.vel = vel
        #self.sigma = sigma
        #self.intensity = intensity
        #self.nx = nx
        #self.ny = ny
        for t in range(frames):
            for j in range(4):
                x_max[j] = xdim * (1 + 2 * (j % 2)) // 4 + math.ceil(xdim // 5 * np.sin(dt * nx[j] * vel[j] * t))  # координаты двигающейся точки
                y_max[j] = ydim * (1 + 2 * (j // 2)) // 4 + math.ceil(ydim // 5 * np.cos(dt * ny[j] * vel[j] * t))  # фигуры Лиссажу

                impletion = np.ndarray(shape=(xdim, ydim), dtype=complex)  # формируем заполнение
                impletion[:, :].real = 1#(2 * np.random.rand(xdim, ydim) - 1) / (2 ** 0.5)
                impletion[:, :].imag = 1#(2 * np.random.rand(xdim, ydim) - 1) / (2 ** 0.5)

                for n in range(xdim):
                    impletion[n,:] = (np.exp(- ((n - x_max[j]) ** 2) / sigma[j])) * impletion[n,:]  # модулируем заполнение по столбцам,
                for k in range(ydim):
                    impletion[:, k] = intensity[j] * (np.exp(-((k - y_max[j]) ** 2) / sigma[j])) * impletion[:, k]  # а затем результат модулируем по строкам

                self.data[:, :, t] = self.data[:, :, t] + impletion

            impletion = np.ndarray(shape=(xdim, ydim), dtype=complex)  # формируем заполнение
            impletion[:, :].real = (2 * np.random.rand(xdim, ydim) - 1) / (2 ** 0.5)
            impletion[:, :].imag = (2 * np.random.rand(xdim, ydim) - 1) / (2 ** 0.5)
            self.data[:, :, t] = self.data[:, :, t] + noize * impletion
            print(t, "st frame generated")


if __name__ == "__main__":
    om2 = OurMatrix2(200, 200, [1,1,1,1], [1,1,1,1],[1,1,1,1],[10,10,10,10],[10,10,10,10], 50)
    #print(om2.generate_name())