import random
from matplotlib import pyplot
import numpy as np


def recursive_probably(p_matrix, previous_probably, count_t):
    if count_t == 0:
        return previous_probably
    current_probably = recursive_probably(p_matrix, previous_probably, count_t - 1).dot(p_matrix)
    return current_probably


def get_p_t_recursive(p_matrix, start_state, count_t):
    result = np.zeros(count_t)
    states = np.zeros(2)
    states[start_state] = 1
    for i in range(count_t):
        result[i] = recursive_probably(p_matrix, states, i)[start_state]
    return result


def get_p_t_th(p_matrix, start_state, count_t):
    result = np.zeros(count_t)
    states = np.zeros(2)
    states[start_state] = 1
    for i in range(count_t):
        pow_matrix = np.linalg.matrix_power(p_matrix, i)
        result[i] = states.dot(pow_matrix[start_state])
    return result


def get_p_t(p_matrix, start_state, count_n, count_t):
    result = np.zeros(count_t)
    for n in range(count_n):
        state = start_state
        for i in range(count_t):
            if state == start_state:
                result[i] += 1
            next_state_prob = random.random()
            if next_state_prob < p_matrix[state][start_state]:
                state = start_state
            else:
                state = (start_state + 1) % 2
    for i in range(T):
        result[i] /= N
    return result


if __name__ == '__main__':
    P = np.array([[0.8, 0.2],
                  [0.6, 0.4]])
    my_start_state = 1
    N = 100000
    T = 20

    p_t = get_p_t(P, my_start_state, N, T)
    p_t_th = get_p_t_th(P, my_start_state, T)
    p_t_rec = get_p_t_recursive(P, my_start_state, T)

    pyplot.plot(range(T), p_t)
    pyplot.plot(range(T), p_t_th)
    pyplot.savefig("result.png")

    pyplot.clf()

    pyplot.plot(range(T), p_t)
    pyplot.plot(range(T), p_t_rec, "r")
    pyplot.savefig("result_rec.png")
