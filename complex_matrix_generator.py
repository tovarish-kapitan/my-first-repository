import numpy as np
import math

class OurMatrix:
    def __init__(self, x_dim, y_dim, nx, ny, sigma, intensity, frames):
        self.Data = np.ndarray(shape=(x_dim, y_dim, frames,), dtype = complex)#массив комплексных матриц
        for t in range(frames):
            x_max = x_dim // 2 + math.ceil(x_dim // 3 * np.sin(nx * 0.1 * t))  #координаты двигающейся точки
            y_max = y_dim // 2 + math.ceil(y_dim // 3 * np.cos(ny * 0.1 * t))  #фигуры Лиссажу

            impletion = np.ndarray(shape=(x_dim, y_dim), dtype = complex)  #формируем заполнение
            impletion[:, :].real = 2 * np.random.rand(x_dim, y_dim) - 1
            impletion[:, :].imag = 2 * np.random.rand(x_dim, y_dim) - 1
        
            for n in range(x_dim):
                self.Data[n, :, t] = (np.exp( - ((n - x_max) ** 2) / sigma)) * impletion[n, :]  #модулируем заполнение по столбцам,
            for k in range(y_dim):
                self.Data[:, k, t] = intensity * (np.exp(-((k - y_max)**2) / sigma)) * self.Data[:, k, t]  #а затем результат модулируем по строкам

            self.Data[:, :, t] = self.Data[:, :, t] + impletion[:, :]
            
            print(t, "st frame generated")


if __name__ == "__main__":
    om = OurMatrix(600,600,1,1,50,10, 63)

