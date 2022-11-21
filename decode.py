import sys
import argparse
from matrices import *
from IO import *
from operations import *


# finds error vector u that will be added to our codeword to correct distortion
def find_u(word, mat_B, decode_mat):
    zeros_vec = np.zeros(12)

    # compute syndrome
    s = vm_dot_mod_2(word, decode_mat)

    if vector_weight(s) <= 3:
        print("syndrome weight was <=3")
        u = np.concatenate((s, zeros_vec))
        return u

    for idx, vector in enumerate(mat_B):
        snb = vv_add_mod_2(s, vector)
        if vector_weight(snb) <= 2:
            print("syndrome + bi weight was <=2")
            zeros_vec[idx] = 1
            u = np.concatenate((snb, zeros_vec))
            return u

    # compute second syndrome
    sB = vm_dot_mod_2(s, mat_B)

    if vector_weight(sB) <= 3:
        print("sB weight was <=3")
        u = np.concatenate((zeros_vec, sB))
        return u

    for idx, vector in enumerate(mat_B):
        sBnb = vv_add_mod_2(sB, vector)
        if vector_weight(sBnb) <= 2:
            print("sB + bi weight was <=2")
            zeros_vec[idx] = 1
            u = np.concatenate((zeros_vec, sBnb))
            return u


# weight every vector in distorted array, add 0 or 1 to end
def convert_vector_array_to_C24(vector_array):
    extra_dim = []
    for vector in vector_array:
        if vector_weight(vector) % 2 == 0:
            extra_dim.append(1)
        else:
            extra_dim.append(0)

    extra_dim = np.array(extra_dim)
    return np.column_stack((vector_array, extra_dim))


# send every distorted vector to decoding algo of C24.
def decode_C24(vector_array_C24):
    matrix_B = generate_B(full=True)
    decode_matrix = generate_H(True)

    decoded_vector_array = []
    for vector in vector_array_C24:
        u = find_u(vector, matrix_B, decode_matrix)
        decoded_codeword = vv_add_mod_2(vector, u)
        decoded_codeword = decoded_codeword[:-1]
        decoded_value = decoded_codeword[:12]
        decoded_vector_array.append(decoded_value)

    return decoded_vector_array


def decode_vector_array(distorted_vector_array):
    distorted_vector_array_C24 = convert_vector_array_to_C24(
        distorted_vector_array)

    return decode_C24(distorted_vector_array_C24)
