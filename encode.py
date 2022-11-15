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

input_vector = read_vector_from_file(args.inputFile)

matrices = Matrices(full_B=True)
gen_matrix = matrices.get_G()

encoded_vector = vm_dot_mod_2(input_vector, gen_matrix, 12, 24)

if args.outputFile:
    write_ndarray_to_file(encoded_vector, args.outputFile)
else:
    write_ndarray_to_file(encoded_vector, "encoded_output.txt")

sys.exit()
