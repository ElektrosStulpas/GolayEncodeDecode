import numpy as np


def vm_dot_mod_2(vector, matrix, m, n):
    res_vector = []

    for m_col_idx in range(n):
        temp_res = 0
        for vec_idx in range(m):
            temp_res += vector[vec_idx]*matrix[vec_idx][m_col_idx]
            if temp_res % 2 == 0:
                temp_res = 0
        res_vector.append(temp_res)

    return np.array(res_vector)


def vector_add_mod_2(vector_A, vector_B):
    new_vector = []
    # assumption here that both vectors are the same length
    for idx in range(len(vector_A)):
        new_vector.append((vector_A[idx] + vector_B[idx]) % 2)

    return np.array(new_vector)


def vector_weight(vector):
    return sum(vector)
