import argparse
from IO import *
from encode import *
from distortion import *
from decode import *

# command line arguments definition and parsing.
parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str,
                    help="Input file path. containing either binary vector of 12 multitude length.")
parser.add_argument(
    'mode', choices=["BFT", "TFT", "IFB"], help="BFT = BinaryFromTxt: mode processes binary vector from txt file. inputFile has to contain a binary vector of 12 multitude length.\nTFT = TextFromTxt: mode processes some text from txt file. inputFile has to contain some text.\nIFB = ImageFromBmp mode processes a bmp format image. inputFile has to be a bmp file image.")
parser.add_argument("distortion_p", type=int,
                    help="Chance to distort a bit at every position in the vector in percents (should be provided as a number 0-100).")
parser.add_argument("-encode", "--useEncoding",
                    action="store_true", help="Flag to turn on encoding and decoding usage when sending. When not specified, encoding and decoding are not used.")
args = parser.parse_args()

inputPath = args.inputFile
mode = args.mode
p = args.distortion_p
useEncoding = args.useEncoding


# read input based on mode used (binaryFromTxt outputs more details to console)
if mode == 'BFT':
    input_vector_array = read_from_file_VECTOR(inputPath, 12)
    print("Input vectors:")
    print_ndarray(input_vector_array)
elif mode == 'TFT':
    input_vector_array, char_mask = read_from_file_TEXT(inputPath)
elif mode == 'IFB':
    input_vector_array, len_mask, img_shape = read_from_file_IMAGE(inputPath)


# encode all vectors read from input file
encoded_vector_array = []
if useEncoding:
    print("Encoding..")
    encoded_vector_array = encode_vector_array(input_vector_array)
    print("Encoding complete..")
    if mode == 'binaryFromTxt':
        print("Encoded vectors:")
        print_ndarray(encoded_vector_array)


# send through distortion channel and output to file
print("Sending through distortion channel..")
if len(encoded_vector_array) > 0:
    # if encoding was used, we use encoded vectors
    distorted_vector_array, error_info = distort_vector_array(
        encoded_vector_array, p)
else:
    # if no encoding, we use raw input vectors
    distorted_vector_array, error_info = distort_vector_array(
        input_vector_array, p)
print("Distortion complete..")


# depending on mode IO operations after distortion
if mode == 'BFT':
    # for binary text we output info to console
    print("Distorted vectors:")
    print_ndarray(distorted_vector_array)
    print("Number of errors and indexes where it happened for each array:")
    print(error_info)
    # we also write the distorted vectors to file in case we want to edit it before decoding
    write_ndarray_to_file_VECTOR(
        distorted_vector_array, "distorted_output.txt")
elif mode == 'TFT' and not useEncoding:
    # pass the distorted vector to be converted to text and written to file
    write_ndarray_to_file_TEXT(
        distorted_vector_array, char_mask, "distorted_output.txt")
elif mode == 'IFB' and not useEncoding:
    # pass the distorted vector to be converted to image and show it
    show_ndarray_as_IMAGE(distorted_vector_array, len_mask, img_shape)


# decode vectors and present results after decoding
if useEncoding:
    # if binaryFromTxt mode, then give a checkpoint to edit distorted output and read the edited distorted output
    if mode == 'BFT':
        input(
            'Please hit enter when the "distorted_output.txt" file is reviewed: ')
        distorted_vector_array = read_from_file_VECTOR(
            "distorted_output.txt", 23)

    print("Decoding..")
    decoded_vector_array = decode_vector_array(distorted_vector_array)
    print("Decoding complete..")

    # depending on mode final print outs to console/writing to file/showing the final picture result
    if mode == 'BFT':
        print("Decoded vectors:")
        print_ndarray(decoded_vector_array)
        write_ndarray_to_file_VECTOR(
            decoded_vector_array, "decoded_output.txt")
    elif mode == 'TFT':
        write_ndarray_to_file_TEXT(
            decoded_vector_array, char_mask, "decoded_output.txt")
    elif mode == 'IFB':
        show_ndarray_as_IMAGE(decoded_vector_array, len_mask, img_shape)
