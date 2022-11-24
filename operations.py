import numpy as np


# multiplies vector with matrix with mod 2
def vm_dot_mod_2(vector, matrix):
    res_vector = []

    for m_col_idx in range(matrix.shape[1]):
        temp_res = 0
        for vec_idx in range(matrix.shape[0]):
            # every element in vector we multiply with every element of each column in the matrix for every column
            temp_res += vector[vec_idx]*matrix[vec_idx][m_col_idx]
            if temp_res % 2 == 0:
                temp_res = 0
        res_vector.append(temp_res)

    return np.array(res_vector)


# adds two vectors element-wise with mod 2
def vv_add_mod_2(vector_A, vector_B):
    new_vector = []
    # assumption here that both vectors are the same length
    for idx in range(len(vector_A)):
        new_vector.append((vector_A[idx] + vector_B[idx]) % 2)

    return np.array(new_vector)


# returns vector weight, which is a sum of all vector elements
def vector_weight(vector):
    return sum(vector)
