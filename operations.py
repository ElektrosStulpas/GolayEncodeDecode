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
