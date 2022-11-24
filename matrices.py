import numpy as np


# generate an identity matrix
def generate_I(n=12):
    return np.identity(n)


# generate B matrix, full is 12x12, not full is 12x11
def generate_B(full=True):
    extra_dim = np.ones(11)
    matrix_B = []
    # initial row which we will roll
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


# generate the generation matrix
def generate_G(full=False):
    I = generate_I()
    B = generate_B(full)
    # stack next to each other to return 12x24/12x23
    return np.concatenate((I, B), axis=1)


# generate control matrix
def generate_H(full=True):
    I = generate_I()
    B = generate_B(full)
    # stack on top of each other to return 24x12. 23x12 will break due to dimension mismatch
    return np.concatenate((I, B), axis=0)
