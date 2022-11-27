from matrices import *
from operations import *


# finds error vector u that will be added to our codeword to correct distortion
def find_u(word, mat_B, decode_mat):
    zeros_vec = np.zeros(12)

    # compute syndrome
    s = vm_dot_mod_2(word, decode_mat)

    if vector_weight(s) <= 3:
        u = np.concatenate((s, zeros_vec))
        return u

    for idx, vector in enumerate(mat_B):
        # add syndrome to every vector from matrix B
        snb = vv_add_mod_2(s, vector)
        if vector_weight(snb) <= 2:
            zeros_vec[idx] = 1
            u = np.concatenate((snb, zeros_vec))
            return u

    # compute second syndrome
    sB = vm_dot_mod_2(s, mat_B)

    if vector_weight(sB) <= 3:
        u = np.concatenate((zeros_vec, sB))
        return u

    for idx, vector in enumerate(mat_B):
        # add second syndrome to every vector from matrix B
        sBnb = vv_add_mod_2(sB, vector)
        if vector_weight(sBnb) <= 2:
            zeros_vec[idx] = 1
            u = np.concatenate((zeros_vec, sBnb))
            return u


# weigh every vector in given array, add 0 or 1 to the end of each
def convert_vector_array_to_C24(vector_array):
    extra_dim = []
    for vector in vector_array:
        if vector_weight(vector) % 2 == 0:
            extra_dim.append(1)
        else:
            extra_dim.append(0)

    extra_dim = np.array(extra_dim)
    return np.column_stack((vector_array, extra_dim))


# decode C24 vector array by finding u and adding it to our distorted codeword
def decode_C24_to_C23(vector_array_C24):
    # for decoding we generate full C24 matrices
    matrix_B = generate_B(full=True)
    decode_matrix = generate_H(True)

    decoded_vector_array = []
    for vector in vector_array_C24:
        u = find_u(vector, matrix_B, decode_matrix)
        # add distorted codeword to our error vector u
        decoded_codeword = vv_add_mod_2(vector, u)
        # remove last digit to return to C23
        decoded_codeword = decoded_codeword[:-1]
        # take only the first 12 digits since they represented the initial vector
        decoded_value = decoded_codeword[:12]
        decoded_vector_array.append(decoded_value)

    # return our decoded vector array where every vector is decoded and in C23
    return decoded_vector_array


# decode vector array where every vector is of length 23
def decode_vector_array(distorted_vector_array):
    # as per given algorithm, first we convert our C23 codewords to C24 codewords
    distorted_vector_array_C24 = convert_vector_array_to_C24(
        distorted_vector_array)

    decoded_vector_array = decode_C24_to_C23(distorted_vector_array_C24)

    return decoded_vector_array
