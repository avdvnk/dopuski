import random
import numpy as np


def average_system_life(p_matrix, start_state, count_n):
    total_count = 0
    for i in range(count_n):
        current_state = start_state
        count = 0
        while current_state != 2:
            pr_next_state = random.random()
            if pr_next_state < p_matrix[current_state][0]:
                current_state = 0
            elif pr_next_state < p_matrix[current_state][0] + p_matrix[current_state][1]:
                current_state = 1
            else:
                current_state = 2
            count += 1
        total_count += count
    return total_count / count_n


def theoretical_average_life_system(p_matrix, start_state):
    matrix_a = np.array([[1 - p_matrix[0][0], p_matrix[0][1] * -1],
                         [p_matrix[1][0] * -1, 1 - p_matrix[1][1]]])
    matrix_b = np.ones(2)
    return np.linalg.solve(matrix_a, matrix_b)[start_state]


if __name__ == '__main__':
    P = np.array([[0.9, 0.05, 0.05],
                  [0.8, 0.1, 0.1],
                  [1, 0, 0]])
    N = 200000
    my_start_state = 1
    print("Experimental value: {}".format(average_system_life(P, my_start_state, N)))
    print("Theoretical value: {}".format(theoretical_average_life_system(P, my_start_state)))
