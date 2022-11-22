import argparse
from IO import *
from encode import *
from distortion import *
from decode import *

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str,
                    help="Input file containing binary vector of 12 multitude length")
parser.add_argument(
    'mode', choices=['binaryFromTxt', 'textFromTxt', 'imageFromBmp'])
parser.add_argument("p", type=int,
                    help="Chance to distort number at every position in percents (should be provided as a number 0-100)")
parser.add_argument('-encode', '--useEncoding',
                    action='store_true')
parser.add_argument("-out", "--outputFile", type=str,
                    help="Path where output file will be created. If none, output file will be created in the same directory as the script")
args = parser.parse_args()

inputPath = args.inputFile
mode = args.mode
p = args.p
useEncoding = args.useEncoding
outputPath = args.outputFile


# read input based on mode
if mode == 'binaryFromTxt':
    input_vector_array = read_from_file_VECTOR(inputPath, 12)
    print("Input vectors:")
    print_ndarray(input_vector_array)
elif mode == 'textFromTxt':
    input_vector_array, char_mask = read_from_file_TEXT(inputPath)
elif mode == 'imageFromBmp':
    print("placeholder")


# encode and show all vectors read from input file
encoded_vector_array = []
if useEncoding:
    print("Encoding..")
    encoded_vector_array = encode_vector_array(input_vector_array)
    print("Encoded vectors:")
    print_ndarray(encoded_vector_array)


# send through channel and output to file
print("Sending through distortion channel..")
if len(encoded_vector_array) > 0:
    distorted_vector_array, error_info = distort_vector_array(
        encoded_vector_array, p)
else:
    distorted_vector_array, error_info = distort_vector_array(
        input_vector_array, p)

print("Distorted vectors:")
print_ndarray(distorted_vector_array)


if mode == 'binaryFromTxt':
    print("Number of errors and indexes where it happened for each array:")
    print(error_info)
    write_ndarray_to_file_VECTOR(
        distorted_vector_array, "distorted_output.txt")
elif mode == 'textFromTxt':
    write_ndarray_to_file_TEXT(
        distorted_vector_array, char_mask, "distorted_output.txt")
elif mode == 'imageFromBmp':
    print("placeholder")


# decode vector and output to file
if useEncoding:

    if mode == 'binaryFromTxt':
        input(
            'Please hit enter when the "distorted_output.txt" file is reviewed: ')
        distorted_vector_array = read_from_file_VECTOR(
            "distorted_output.txt", 23)

    print("Decoding..")
    decoded_vector_array = decode_vector_array(distorted_vector_array)
    print("Decoded vectors:")
    print_ndarray(decoded_vector_array)

    if mode == 'binaryFromTxt':
        write_ndarray_to_file_VECTOR(
            decoded_vector_array, "decoded_output.txt")
    elif mode == 'textFromTxt':
        write_ndarray_to_file_TEXT(
            decoded_vector_array, char_mask, "decoded_output.txt")
    elif mode == 'imageFromBmp':
        print("placeholder")
