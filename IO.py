import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# prints an ndarray with all elements as ints
def print_ndarray(ndarray):
    for array in ndarray:
        print(array.astype(int))


# opens/creates a file at filepath and writes the provided string
def write_string_to_file(filepath, string):
    with open(filepath, "w") as f:
        f.write(string)
        f.close()


# opens a file at filepath and reads it's contents to a single string
def read_string_from_file(filepath):
    string = ""
    with open(filepath, "r") as f:
        string = f.read()
        f.close()
    return string


# shows the provided image
def show_image(img):
    plt.imshow(img)
    plt.show()


# given an array, applies a length mask to separate array elems by length
# "0011010100110101", [3, 6, 4, 3] -> ["001", "101010", "0110", "101"]
def separate_array_by_mask(array, mask):
    separated_array = []
    len_cursor = 0
    for num_len in mask:
        current_num = array[len_cursor:len_cursor+num_len]
        separated_array.append(current_num)
        len_cursor += num_len
    return separated_array


# given any dimension vector array flattens it into a 1D array
def flatten_vector_array(vector_array):
    return np.reshape(vector_array, (1, -1))[0]


# pad array with 0s to be length of 12 multiple
# "001101010" -> "001101010000"
def pad_array_to_12(array):
    if len(array) % 12 != 0:
        pad_size = 12 - len(array) % 12
        return np.concatenate((array, np.zeros(pad_size)))
    else:
        return array


# concats all strings/char in array into a single string
# ["0", "1", "0"] -> "010"
# ["00", "01", "10", "11"] -> "00011011"
def char_array_to_string(array):
    return "".join(array)


# converts string into int array
# "00011011" -> [0, 0, 0, 1, 1, 0, 1, 1]
def string_to_int_array(vec):
    line_data = []
    for idx in range(len(vec)):
        line_data.append(int(vec[idx]))

    return np.array(line_data)


# convert bin array to a single char
# "1001110" -> 'N'
def bin_array_to_char(array):
    dec_num = 0
    for j in range(len(array)):
        dec_num += array[-(j+1)] * 2**j

    return chr(int(dec_num))


# convert bin array to a single decimal number (int)
# "10101" -> 21
def bin_array_to_int(array):
    dec_num = 0
    for j in range(len(array)):
        dec_num += array[-(j+1)] * 2**j

    return int(dec_num)


# MODE IFB read and write

# reads from a bmp format image, converts it to binary int vector array
# additionally returns length mask to separate binary values and img_shape to know into what reshape when converting back to an image
def read_from_file_IMAGE(filepath):
    img = Image.open(filepath).convert("RGB")

    show_image(img)

    img = np.array(img)
    img_shape = img.shape
    img = flatten_vector_array(img)

    # converts the 1D int array to to a 1D binary array representing same values
    buff = [bin(x)[2:] for x in img]
    # creates length mask for the binary decimal representations
    len_mask = [len(x) for x in buff]

    # concat all binary elements to a single string and cast it to int vector
    buff = char_array_to_string(buff)
    buff = string_to_int_array(buff)
    # pad the vector to make sure it's length is a multiple of 12
    buff = pad_array_to_12(buff)

    # reshape the 1D vector into Nx12 vector_array
    buff = np.reshape(buff, (-1, 12))

    return buff.astype(int), len_mask, img_shape


# given a vector array, binary mask, and original img shape converts vector array back to an image representation
def show_ndarray_as_IMAGE(ndarray, len_mask, img_shape):
    # flatten Nx12 array into 1D
    ndarray = flatten_vector_array(ndarray)

    # separate binary representations by applying mask
    bin_int_array = separate_array_by_mask(ndarray, len_mask)

    # convert binary representations back to ints
    val_buff = []
    for array in bin_int_array:
        val = bin_array_to_int(array)
        val_buff.append(val)

    # reshape into image data structure
    img = np.reshape(val_buff, img_shape)

    show_image(img)


# MODE TFT read and write

# given a filepath read all contents as string returns a binary int vector array together with a binary len mask
def read_from_file_TEXT(filepath):
    text_buff = read_string_from_file(filepath)

    # converts the string to a 1D binary array representing same char values
    buff = [bin(ord(x))[2:] for x in text_buff]
    # creates length mask for the binary decimal representations
    char_mask = [len(x) for x in buff]
    # concat all binary elements to a single string and cast it to int vector
    buff = char_array_to_string(buff)
    buff = string_to_int_array(buff)
    # pad the vector to make sure it's length is a multiple of 12
    buff = pad_array_to_12(buff)

    # reshape the 1D vector into Nx12 vector_array
    buff = np.reshape(buff, (-1, 12))
    # returning buff as int to remain uniform with reading vector from file
    return buff.astype(int), char_mask


# given vector array, char mask and filepath
# converts the vector array into a text representation and writes it to a given filepath
def write_ndarray_to_file_TEXT(ndarray, char_mask, filepath):
    # flatten Nx12 array into 1D
    ndarray = flatten_vector_array(ndarray)

    # separate binary representations by applying mask
    bin_char_array = separate_array_by_mask(ndarray, char_mask)

    # convert binary representations back to chars
    text_buff = []
    for array in bin_char_array:
        char = bin_array_to_char(array)
        text_buff.append(char)

    # concat to a string and write to file
    text_buff = char_array_to_string(text_buff)
    write_string_to_file(filepath, text_buff)


# MODE BFT read and write

# reads a vector from file and returns it in Nx12 representation
def read_from_file_VECTOR(filepath, vector_length):
    vector_buff = read_string_from_file(filepath)
    whole_vector_len = len(vector_buff)

    # if the read amount is not the same as vector_length, we complain about incorrect format and exit
    if (whole_vector_len % vector_length) != 0:
        print(
            f"Binary vector is not a multiple of {vector_length}, full vector len was {whole_vector_len}, exiting")
        sys.exit()

    # cast char 1s and 0s to ints and reshape to vectors of length 12
    vector_buff = string_to_int_array(vector_buff)
    vector_buff = np.reshape(vector_buff, (-1, 12))

    return vector_buff


# given a vector array and filepath writes the vector array as a single vector to filepath
def write_ndarray_to_file_VECTOR(ndarray, filepath):
    ndarray = flatten_vector_array(ndarray)
    arraystring = char_array_to_string(ndarray.astype(str))

    write_string_to_file(filepath, arraystring)
