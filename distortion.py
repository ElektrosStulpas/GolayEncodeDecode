from IO import *
import random


def distort_array(array, p):
    error_count = 0
    error_buff = []
    for idx in range(len(array)):
        random.randint(0, 100)

        if random.randint(0, 100) < p:
            array[idx] = (array[idx] + 1) % 2
            error_count += 1
            error_buff.append(idx)

    return array, error_count, error_buff


def distort_vector_array(sent_vector_array, p):
    vectors_error_info = []
    for array_idx in range(len(sent_vector_array)):
        sent_vector_array[array_idx], error_count, error_buff = distort_array(
            sent_vector_array[array_idx], p)
        vectors_error_info.append((error_count, error_buff))

    return sent_vector_array, vectors_error_info
