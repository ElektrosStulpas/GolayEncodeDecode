from matrices import *
from operations import vm_dot_mod_2


# multiplies given vector with given matrix
def encode_vector(vector, gen_matrix):
    return vm_dot_mod_2(vector, gen_matrix)


# encodes a vector array where every vector is of length 12 to C23
def encode_vector_array(vector_array):
    # generate C23 generation matrix
    gen_matrix = generate_G(False)
    encoded_vector_array = []
    # encode every vector with C23 generation matrix
    for idx in range(len(vector_array)):
        encoded_vector = encode_vector(vector_array[idx], gen_matrix)
        encoded_vector_array.append(encoded_vector)

    # return encoded vector array where every vector is in C23 format
    return np.array(encoded_vector_array)
