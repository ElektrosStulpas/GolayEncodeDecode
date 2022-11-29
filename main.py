import argparse
from IO import *
from encode import *
from distortion import *
from decode import *

# command line arguments definition and parsing.
parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str,
                    help="Input file path. File containing binary vector of 12 multitude length, text, or a picture in bmp format.")
parser.add_argument(
    'mode', choices=["BFT", "TFT", "IFB"], help="BFT = BinaryFromTxt: mode processes binary vector of 12 multitude length from txt file. TFT = TextFromTxt: mode processes some text from txt file. IFB = ImageFromBmp mode processes a bmp format image.")
parser.add_argument("distortion_p", type=float,
                    help="Chance to distort a bit at every position in the vector in percents (should be provided as a number 0.00-100.00).")
parser.add_argument("-out", "--outputPath", type=str, default="",
                    help="Path where output files will be created. If none, output file will be created in the same directory as the script is ran")
args = parser.parse_args()

inputFile = args.inputFile
mode = args.mode
p = args.distortion_p
outputPath = args.outputPath


# read input based on mode used (binaryFromTxt outputs more details to console)
if mode == 'BFT':
    input_vector_array = read_from_file_VECTOR(inputFile, 12)
    print("Input vectors:")
    print_ndarray(input_vector_array)

elif mode == 'TFT':
    input_vector_array, char_mask = read_from_file_TEXT(inputFile)

    # distortion first without encoding
    distorted_vector_array, _ = distort_vector_array(
        input_vector_array, p)

    # pass the distorted vector to be converted to text and written to file
    write_ndarray_to_file_TEXT(
        distorted_vector_array, char_mask, outputPath + "distorted_output_text.txt")

elif mode == 'IFB':
    input_vector_array, len_mask, img_shape = read_from_file_IMAGE(inputFile)

    # distortion first without encoding
    distorted_vector_array, _ = distort_vector_array(
        input_vector_array, p)

    # pass the distorted vector to be converted to image and show it
    show_ndarray_as_IMAGE(distorted_vector_array, len_mask, img_shape, False)


# encode all vectors read from input file
print("Encoding..")
encoded_vector_array = encode_vector_array(input_vector_array)
print("Encoding complete..")
if mode == 'BFT':
    print("Encoded vectors:")
    print_ndarray(encoded_vector_array)


# send encoded data through distortion channel
print("Sending through distortion channel..")
distorted_vector_array, error_info = distort_vector_array(
    encoded_vector_array, p)
print("Distortion complete..")


if mode == 'BFT':
    # for binary text we output info to console
    print("Distorted vectors:")
    print_ndarray(distorted_vector_array)
    print("Number of errors and indexes where it happened for each array:")
    print(error_info)
    # we also write the distorted vectors to file in case we want to edit it before decoding
    write_ndarray_to_file_VECTOR(
        distorted_vector_array, outputPath + "distorted_output_vector.txt")


# if binaryFromTxt mode, then give a checkpoint to edit distorted output and read the edited distorted output
if mode == 'BFT':
    input(
        'Please hit enter when the "distorted_output_vector.txt" file is reviewed: ')
    distorted_vector_array = read_from_file_VECTOR(
        outputPath + "distorted_output_vector.txt", 23)


# decode vectors
print("Decoding..")
decoded_vector_array = decode_vector_array(distorted_vector_array)
print("Decoding complete..")


# depending on mode final print outs to console/writing to file/showing the final picture result
if mode == 'BFT':
    print("Decoded vectors:")
    print_ndarray(decoded_vector_array)
    write_ndarray_to_file_VECTOR(
        decoded_vector_array, outputPath + "decoded_output_vector.txt")
elif mode == 'TFT':
    write_ndarray_to_file_TEXT(
        decoded_vector_array, char_mask, outputPath + "decoded_output_text.txt")
elif mode == 'IFB':
    show_ndarray_as_IMAGE(decoded_vector_array, len_mask, img_shape, True)
