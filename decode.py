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
        print("syndrome weight was <=3")
        u = np.concatenate((s, zeros_vec))
        return u

    for idx, vector in enumerate(matrix_B):
        snb = vv_add_mod_2(s, vector)
        if vector_weight(snb) <= 2:
            print("syndrome + bi weight was <=2")
            zeros_vec[idx] = 1
            u = np.concatenate((snb, zeros_vec))
            return u

    # compute second syndrome
    sB = vm_dot_mod_2(s, matrix_B, 12, 12)

    if vector_weight(sB) <= 3:
        print("sB weight was <=3")
        u = np.concatenate((zeros_vec, sB))
        return u

    for idx, vector in enumerate(matrix_B):
        sBnb = vv_add_mod_2(sB, vector)
        if vector_weight(sBnb) <= 2:
            print("sB + bi weight was <=2")
            zeros_vec[idx] = 1
            u = np.concatenate((zeros_vec, sBnb))
            return u


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


# weight every vector in distorted array, add 0 or 1 to end
extra_dim = []
for idx, vector in enumerate(distorted_vector_array):
    if vector_weight(vector) % 2 == 0:
        extra_dim.append(1)
    else:
        extra_dim.append(0)

extra_dim = np.array(extra_dim)
distorted_vector_array = np.column_stack((distorted_vector_array, extra_dim))


# send every distorted vector to decoding algo of C24. Ret
decoded_vector_array = []
for vector in distorted_vector_array:
    u = find_u(vector)
    decoded_codeword = vv_add_mod_2(vector, u)
    decoded_codeword = decoded_codeword[:-1]
    decoded_value = decoded_codeword[:12]
    decoded_vector_array.append(decoded_value)


# if args.outputFile:
#     write_ndarray_to_file(decoded_vector_array, args.outputFile)
# else:
write_ndarray_to_file(decoded_vector_array, "decoded_output.txt")

# sys.exit()
