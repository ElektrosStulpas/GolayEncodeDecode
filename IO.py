import sys
import numpy as np


def print_ndarray(ndarray):
    for array in ndarray:
        print(array.astype(int))


def str_vec_to_int_array(vec):
    line_data = []
    for idx in range(len(vec)):
        line_data.append(int(vec[idx]))

    return np.array(line_data)


def int_array_to_char(array):
    dec_num = 0
    for j in range(len(array)):
        dec_num += array[-(j+1)] * 2**j

    return chr(int(dec_num))


def read_from_file_TEXT(filepath):
    text_buff = []

    with open(filepath) as f:
        text_buff = f.read()
        f.close()

    # convert all chars in text_buff to binary
    buff = [bin(ord(x))[2:] for x in text_buff]
    # save lengths of all binary chars to later know what to decode
    len_mask = [len(x) for x in buff]
    # convert all binary chars to one binary string
    buff = "".join(buff)

    buff = str_vec_to_int_array(buff)
    pad_size = 0
    if len(buff) % 12 != 0:
        pad_size = 12 - len(buff) % 12
        buff = np.concatenate((buff, np.zeros(pad_size)))

    buff = np.reshape(buff, (-1, 12))
    # returning buff as int to remain uniform with reading vector from file
    return buff.astype(int), len_mask


def read_from_file_VECTOR(filepath, vector_length):
    data_array = []

    with open(filepath) as f:
        full_vector_len = 0
        while True:
            line = str(f.read(vector_length))
            if not line:
                break

            line_len = len(line)
            full_vector_len += line_len

            if (line_len % vector_length) != 0:
                print(
                    f"Binary vector is not a multiple of {vector_length}, full vector len was {full_vector_len}, exiting")
                sys.exit()

            line_data = str_vec_to_int_array(line)
            data_array.append(line_data)

        f.close()

    return np.array(data_array)


def write_ndarray_to_file_VECTOR(ndarray, filepath):
    with open(filepath, "w") as f:
        for array_idx in range(len(ndarray)):
            array = ndarray[array_idx].astype(int).astype(str)
            f.write("".join(array))
        f.close()


def write_ndarray_to_file_TEXT(ndarray, char_mask, filepath=""):
    ndarray = np.reshape(ndarray, (1, -1))[0]

    bin_char_array = []
    len_cursor = 0
    for num_len in char_mask:
        current_num = ndarray[len_cursor:len_cursor+num_len]
        bin_char_array.append(current_num)
        len_cursor += num_len

    text_buff = []
    for array in bin_char_array:
        char = int_array_to_char(array)
        text_buff.append(char)

    with open(filepath, "w") as f:
        f.write("".join(text_buff))
        f.close()
