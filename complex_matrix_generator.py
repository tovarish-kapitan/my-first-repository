import numpy as np
import math

class OurMatrix:
    def __init__(self, nx, ny, frames, sigma):
        self.Data = np.ndarray(shape=(nx, ny, frames), dtype = complex)#массив комплексных матриц
        t = 0

        while t < frames:
            x_max = 300 + math.ceil(200 * np.sin(0.1 * t))  #координаты двигающейся точки
            y_max = 300 + math.ceil(200 * np.cos(0.2 * t + 0.5 * np.pi))  #фигуры Лиссажу

            impletion = np.ndarray(shape=(nx, ny), dtype = complex)  #формируем заполнение
            impletion[:, :].real = 2 * np.random.rand(nx, ny) - 1
            impletion[:, :].imag = 2 * np.random.rand(nx, ny) - 1
        
            n = 0
            while n < nx:
                self.Data[n, :, t] = (np.exp(-((n - x_max)**2) / sigma)) * impletion[n, :]  #модулируем заполнение по столбцам,
                n = n + 1
            k = 0    
            while k < ny:
                self.Data[:, k, t] = 10*(np.exp(-((k - y_max)**2) / sigma)) * self.Data[:, k, t]  #а затем результат модулируем по строкам
                k = k + 1

            self.Data[:, :, t] = self.Data[:, :, t] + impletion[:, :]
            
            print(t, "st frame generated")
            t = t + 1


    
