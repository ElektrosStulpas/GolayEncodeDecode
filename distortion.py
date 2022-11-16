import argparse
from IO import *
import random


def distort_array(array, p):
    for idx in range(len(array)):
        random.randint(0, 100)

        if random.randint(0, 100) <= p:
            distorted_value = array[idx] + 1
            array[idx] = distorted_value % 2

    return array


parser = argparse.ArgumentParser()

parser.add_argument("inputFile", type=str,
                    help="Input txt file containing encoded vector of 23 multitude length")
parser.add_argument("p", type=int,
                    help="Chance to distort number at every position in percents (should be provided as a number 0-100)")
parser.add_argument("-out", "--outputFile", type=str,
                    help="Path where output file with distorted encoded vector will be created. If none, distorted_encoded_output.txt will be created in the same directory as the script")

args = parser.parse_args()

p = args.p

sent_vector_array = read_vector_from_file(args.inputFile, 23)


for array_idx in range(len(sent_vector_array)):
    sent_vector_array[array_idx] = distort_array(
        sent_vector_array[array_idx], p)


if args.outputFile:
    write_ndarray_to_file(sent_vector_array, args.outputFile)
else:
    write_ndarray_to_file(sent_vector_array, "distorted_encoded_output.txt")

sys.exit()
