import sys
import numpy as np


def str_vec_to_int_array(vec):
    line_data = []
    for idx in range(len(vec)):
        line_data.append(int(vec[idx]))

    return np.array(line_data)


def read_text_from_file(filepath):
    text_buff = []

    with open(filepath) as f:
        text_buff = f.read()
        f.close()

    # convert all chars in text_buff to binary
    buff = [bin(ord(x))[2:] for x in text_buff]
    # convert all binary chars to one binary string
    buff = "".join(buff)

    buff = str_vec_to_int_array(buff)
    if len(buff) % 12 != 0:
        pad_size = 12 - len(buff) % 12
        buff = np.concatenate((buff, np.zeros(pad_size)))

    buff = np.reshape(buff, (-1, 12))
    return buff


def read_vector_from_file(filepath, vector_length):
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


def write_ndarray_to_file(ndarray, filepath):
    with open(filepath, "w") as f:
        for array_idx in range(len(ndarray)):
            array = ndarray[array_idx].astype(int).astype(str)
            f.write("".join(array))
        f.close()


def print_ndarray(ndarray):
    for array in ndarray:
        print(array.astype(int))
