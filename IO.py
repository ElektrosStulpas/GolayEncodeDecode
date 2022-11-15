import sys
import numpy as np


def read_vector_from_file(filepath):
    with open(filepath) as f:
        line = str(f.readline())
        f.close()

    if (len(line) % 12) != 0:
        print("Binary vector is not a multiple of 12, exiting")
        sys.exit()

    data_array = []
    for idx in range(len(line)):
        data_array.append(int(line[idx]))

    return np.array(data_array)


def write_ndarray_to_file(ndarray, filepath):
    with open(filepath, "w") as f:
        ndarray = ndarray.astype(int).astype(str)
        f.write("".join(ndarray))
        f.close()
