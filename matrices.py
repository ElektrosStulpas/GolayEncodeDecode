import numpy as np


class Matrices:

    def __init__(self, full_B):
        self.I = self._generate_I()
        self.B = self._generate_B(full_B)
        self.G = self._generate_G()
        if full_B:
            self.H = self._generate_H()

    def get_B(self):
        return self.B

    def get_G(self):
        return self.G

    def get_H(self):
        return self.H

    def _generate_I(self, n=12):
        return np.identity(n)

    def _generate_B(self, full=True):
        extra_dim = np.ones(11)
        matrix_B = []
        gen_row = np.array([1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0])
        if full:
            for _ in range(11):
                matrix_B.append(np.concatenate((gen_row, np.array([1]))))
                gen_row = np.roll(gen_row, -1)
            matrix_B.append(np.concatenate((extra_dim, np.array([0]))))
        else:
            for _ in range(11):
                matrix_B.append(gen_row)
                gen_row = np.roll(gen_row, -1)
            matrix_B.append(extra_dim)

        return np.array(matrix_B)

    def _generate_G(self):
        return np.concatenate((self.I, self.B), axis=1)

    # incorrect on encode due to 12x23 G structure
    def _generate_H(self):
        # or just G.t
        return np.concatenate((self.I, self.B), axis=0)
