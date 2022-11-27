import random
import numpy as np


# distorts every element in the vector with p (0-100) probability
def distort_array(vector, p):
    distorted_vector = []
    error_count = 0
    error_buff = []
    for idx in range(len(vector)):
        current_val = vector[idx]

        if random.randint(1, 100) <= p:
            new_val = (current_val + 1) % 2
            error_count += 1
            error_buff.append(idx)
            distorted_vector.append(new_val)
        else:
            distorted_vector.append(current_val)

    # returns distorted vector, the count of how many errors were made(error_count) and the positions at which the errors are(error_buff)
    return distorted_vector, error_count, error_buff


# takes in a vector array and the probability to distort every element in vectors
def distort_vector_array(sent_vector_array, p):
    distorted_sent_vector_array = []
    vectors_error_info = []
    for vector in sent_vector_array:
        # distort every sent vector
        distorted_sent_vector, error_count, error_buff = distort_array(
            vector, p)
        # save vector error info in separate array
        distorted_sent_vector_array.append(distorted_sent_vector)
        vectors_error_info.append((error_count, error_buff))

    # return the distorted vector and an error info vector
    return np.array(distorted_sent_vector_array), vectors_error_info
