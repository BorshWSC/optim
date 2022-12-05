import random
import time

import numpy as np
from numba import int32
from numba.experimental import jitclass

SIZE = 300

spec = [
    ('size', int32),
    ('tensor', int32[:, :, :])
]


@jitclass(spec)
class CubeTensor(object):

    def __init__(self, tensor):
        self.tensor = tensor
        self.size = SIZE

    def generate_temp_tensor(self):
        return [[[0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

    def __add__(self, other):
        temp = self.generate_temp_tensor()
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    if isinstance(other, int):
                        temp[i][j][k] = self.tensor[i][j][k] + other
                    else:
                        temp[i][j][k] = self.tensor[i][j][k] + other.tensor[i][j][k]
        return temp

    def __mul__(self, other):
        temp = self.generate_temp_tensor()
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    if isinstance(other, int):
                        temp[i][j][k] = self.tensor[i][j][k] * other
                    else:
                        temp[i][j][k] = self.tensor[i][j][k] * other.tensor[i][j][k]
        return temp

    def __sub__(self, other):
        temp = self.generate_temp_tensor()
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    temp[i][j][k] = self.tensor[i][j][k] - other.tensor[i][j][k]
        return temp

    def T(self):
        temp_a = self.generate_temp_tensor()
        temp_b = self.generate_temp_tensor()
        temp_c = self.generate_temp_tensor()
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    temp_a[i][j][k] = self.tensor[j][i][k]
                    temp_b[i][j][k] = self.tensor[k][i][i]
                    temp_c[i][j][k] = self.tensor[i][k][j]
        return temp_a, temp_b, temp_c


def generate_tensor():
    start = time.time()
    arr = np.array([[[random.randint(1, 100) for _ in range(SIZE)] for _ in range(SIZE)] for _ in range(SIZE)])
    print(f'Тензор размером {SIZE} был сгенерирован за {time.time() - start} с.')
    return arr


def main():
    a = CubeTensor(generate_tensor())
    b = CubeTensor(generate_tensor())

    start = time.time()
    sum = a + b
    print(f'Сложение было выполнено за {time.time() - start} с.')

    start = time.time()
    sum1 = a + 5
    print(f'Сложение было выполнено за {time.time() - start} с.')

    start = time.time()
    sub = a - b
    print(f'Вычитание было выполнено за {time.time() - start} с.')

    start = time.time()
    mul = a * 5
    print(f'Умножение было выполнено за {time.time() - start} с.')

    start = time.time()
    mul = a * b
    print(f'Умножение было выполнено за {time.time() - start} с.')

    start = time.time()
    c, d, e = a.T()
    print(f'Перестановка индексов была выполнена за {time.time() - start} с.')


if __name__ == '__main__':
    main()
