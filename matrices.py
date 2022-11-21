import numpy as np


def generate_I(n=12):
    return np.identity(n)


def generate_B(full=True):
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


def generate_G(full=False):
    I = generate_I()
    B = generate_B(full)
    return np.concatenate((I, B), axis=1)


# incorrect on encode due to 12x23 G structure
def generate_H(full=True):
    I = generate_I()
    B = generate_B(full)
    # or just G.t
    return np.concatenate((I, B), axis=0)
