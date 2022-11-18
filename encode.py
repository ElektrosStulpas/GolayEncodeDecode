import sys
import argparse
from matrices import Matrices
from IO import *
from operations import vm_dot_mod_2

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str,
                    help="Input txt file containing binary vector of 12 multitude length")
parser.add_argument("-out", "--outputFile", type=str,
                    help="Path where output file with encoded vector will be created. If none, encoded_output.txt will be created in the same directory as the script")
args = parser.parse_args()


input_vector_array = read_vector_from_file(args.inputFile, 12)

matrices = Matrices(full_B=False)
gen_matrix = matrices.get_G()

encoded_vector_array = []
for input_vector_idx in range(len(input_vector_array)):
    encoded_vector = vm_dot_mod_2(
        input_vector_array[input_vector_idx], gen_matrix, 12, 23)
    encoded_vector_array.append(encoded_vector)

if args.outputFile:
    write_ndarray_to_file(encoded_vector_array, args.outputFile)
else:
    write_ndarray_to_file(encoded_vector_array, "encoded_output.txt")

sys.exit()
