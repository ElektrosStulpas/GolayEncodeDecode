import random


# distorts every element in the array with p (0-100) probability
def distort_array(array, p):
    error_count = 0
    error_buff = []
    for idx in range(len(array)):
        random.randint(0, 100)

        if random.randint(0, 100) < p:
            array[idx] = (array[idx] + 1) % 2
            error_count += 1
            error_buff.append(idx)

    # returns distorted array, the count of how many errors were made(error_count) and the positions at which the errors are(error_buff)
    return array, error_count, error_buff


# takes in a vector array and the probability to distort every element in vectors
def distort_vector_array(sent_vector_array, p):
    vectors_error_info = []
    for array_idx in range(len(sent_vector_array)):
        # distort every sent vector
        sent_vector_array[array_idx], error_count, error_buff = distort_array(
            sent_vector_array[array_idx], p)
        # save vector error info in separate array
        vectors_error_info.append((error_count, error_buff))

    # return the distorted vector and an error info vector
    return sent_vector_array, vectors_error_info
