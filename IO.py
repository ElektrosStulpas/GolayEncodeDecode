import sys
import numpy as np


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

            line_data = []
            for idx in range(line_len):
                line_data.append(int(line[idx]))
            data_array.append(line_data)

        f.close()

    return np.array(data_array)


def write_ndarray_to_file(ndarray, filepath):
    with open(filepath, "w") as f:
        for array_idx in range(len(ndarray)):
            array = ndarray[array_idx].astype(int).astype(str)
            f.write("".join(array))
        f.close()
