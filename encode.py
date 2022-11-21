from matrices import *
from IO import *
from operations import vm_dot_mod_2


def encode_vector(vector, gen_matrix):
    return vm_dot_mod_2(vector, gen_matrix)


def encode_vector_array(vector_array):
    gen_matrix = generate_G(False)
    encoded_vector_array = []
    for idx in range(len(vector_array)):
        encoded_vector = encode_vector(vector_array[idx], gen_matrix)
        encoded_vector_array.append(encoded_vector)

    return np.array(encoded_vector_array)
