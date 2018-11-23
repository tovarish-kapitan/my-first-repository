import numpy as np
import math


class OurMatrix2:
    def __init__(self, x_dim, y_dim, nx, ny, sigma, intensity, frames):
        self.data = np.ndarray(shape=(x_dim, y_dim, frames,), dtype=complex)  # массив комплексных матриц
        dt = 2 * np.pi / frames
        x_max = np.zeros(shape=(4))
        y_max = np.zeros(shape=(4))
        vel = [1,2,3,4]
        for t in range(frames):
            for j in range(4):

                x_max[j] = x_dim * (1 + 2 * (j % 2)) // 4 + math.ceil(x_dim // 5 * np.sin(dt * nx * vel[j] * t))  # координаты двигающейся точки
                y_max[j] = y_dim * (1 + 2 * (j // 2)) // 4 + math.ceil(y_dim // 5 * np.cos(dt * ny * vel[j] * t))  # фигуры Лиссажу

                impletion = np.ndarray(shape=(x_dim, y_dim), dtype=complex)  # формируем заполнение
                impletion[:, :].real = 2 * np.random.rand(x_dim, y_dim) - 1
                impletion[:, :].imag = 2 * np.random.rand(x_dim, y_dim) - 1

                for n in range(x_dim):
                    impletion[n,:] = (np.exp(- ((n - x_max[j]) ** 2) / sigma)) * impletion[n,
                                                                              :]  # модулируем заполнение по столбцам,
                for k in range(y_dim):
                    impletion[:, k] = intensity * (np.exp(-((k - y_max[j]) ** 2) / sigma)) * impletion[:, k]  # а затем результат модулируем по строкам

                self.data[:, :, t] = self.data[:, :, t] + impletion

            impletion = np.ndarray(shape=(x_dim, y_dim), dtype=complex)  # формируем заполнение
            impletion[:, :].real = 2 * np.random.rand(x_dim, y_dim) - 1
            impletion[:, :].imag = 2 * np.random.rand(x_dim, y_dim) - 1
            self.data[:, :, t] = self.data[:, :, t] + impletion
            print(t, "st frame generated")


if __name__ == "__main__":
    om = OurMatrix(600, 600, 0.1, 50, 10, 63)