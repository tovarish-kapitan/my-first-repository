import numpy as np
import math

class OurMatrix:
    def __init__(self, Nx, Ny, Frames):
        self.Data = np.ndarray(shape=(Nx, Ny, Frames), dtype = complex)#массив комплексных матриц
        t = 0

        while t < Frames:
            x_max = 300 + math.ceil(200 * np.sin(0.1 * t))#координаты двигающейся точки
            y_max = 300 + math.ceil(200 * np.cos(0.2*t + 0.5 * np.pi))#фигуры Лиссажу
            n = 0
            while n < Nx:
                k = 0
                while k < Ny:
                    z0 = 2 * complex(np.random.rand() - 0.5, np.random.rand() - 0.5)
                    #случайное комплексное число с компонентами в диапазоне (-1, 1)
                    self.Data[n, k, t] = z0 * (1 + 10*np.exp( -((n - x_max)**2 + (k - y_max)**2) / 50))
                    #модулируем приподнятым гауссом
                    k = k+1
                n = n+1
            print(t, "st frame generated")#создание одной матрицы занимает секунды!
            t = t+1

  
    
