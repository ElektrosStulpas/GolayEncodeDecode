import sys
import argparse
from matrices import Matrices
from IO import *
from operations import *


def find_u(word):
    matrices = Matrices(full_B=True)
    matrix_B = matrices.get_B()
    decode_matrix = matrices.get_H()

    zeros_vec = np.zeros(12)
    # compute syndrome
    s = vm_dot_mod_2(word, decode_matrix, 24, 12)

    if vector_weight(s) <= 3:
        u = np.concatenate((s, zeros_vec))
        return u

    for idx, vector in enumerate(matrix_B):
        snb = vector_add_mod_2(s, vector)
        if vector_weight(snb) <= 2:
            zeros_vec[idx] = 1
            u = np.concatenate((snb, zeros_vec))
            return u

    ss = vm_dot_mod_2(s, matrix_B, 12, 12)


# parser = argparse.ArgumentParser()
# parser.add_argument("inputFile", type=str,
#                     help="Input txt file containing distorted encoded vector of 23 multitude length")
# parser.add_argument("-out", "--outputFile", type=str,
#                     help="Path where output file with decoded vector will be created. If none, decoded_output.txt will be created in the same directory as the script")
# args = parser.parse_args()

# inputFilePath = args.inputFile


# distorted_vector_array = read_vector_from_file(inputFilePath, 23)
distorted_vector_array = read_vector_from_file(
    "d:\\MIF\\7.semestras\\KodTe\\Praktinis\\GolayEncodeDecode\\distorted_encoded_output.txt", 23)


extra_dim = []
for idx, vector in enumerate(distorted_vector_array):
    if vector_weight(vector) % 2 == 0:
        extra_dim.append(1)
    else:
        extra_dim.append(0)

extra_dim = np.array(extra_dim)
distorted_vector_array = np.column_stack((distorted_vector_array, extra_dim))


print(distorted_vector_array)
# weight every vector in distorted array, add 0 or 1 to end
# send to decoding algo of C24

print(decode_matrix)

# sys.exit()
