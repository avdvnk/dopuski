import numpy as np
import random
from matplotlib import pyplot


def get_states(p_matrix, start_state, count_t):
    result = np.zeros(3)
    history = []
    current_state = start_state
    for i in range(count_t):
        result[current_state] += 1
        history.append(current_state)
        pr_next_state = random.random()
        if pr_next_state < p_matrix[current_state][0]:
            current_state = 0
        elif pr_next_state < p_matrix[current_state][0] + p_matrix[current_state][1]:
            current_state = 1
        else:
            current_state = 2
    result /= count_t
    return result, history


def get_theoretical_distribution(p_matrix):
    p_transpose = p_matrix.transpose()
    b_matrix = [0, 0, 1]
    a_matrix = p_transpose - np.identity(3)
    a_matrix[-1] = np.ones(3)
    if round(np.linalg.det(a_matrix), 5) == 0:
        raise AssertionError("The matrix determinant is equal 0!")
    return np.linalg.inv(a_matrix).dot(b_matrix)


if __name__ == '__main__':
    P = np.array([[0.9, 0.05, 0.05],
                  [0.8, 0.1, 0.1],
                  [0.7, 0.1, 0.2]])
    T = 200000
    my_start_state = 0

    states = get_states(P, my_start_state, T)
    prob_states = states[0]
    print("Experimental value: {}".format(prob_states))
    print("Theoretical value: {} (big matrix power)".format(np.linalg.matrix_power(P, 100)[0]))
    print("Theoretical value: {} (linear equation system)".format(get_theoretical_distribution(P)))

    states_history = states[1]
    pyplot.plot(range(T), states_history, 'b.')
    pyplot.savefig("result.png")
