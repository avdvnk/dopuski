import numpy as np


def generate_messages(input_lambda, time):
    buffer_time = 0
    current_time = 0
    result = np.zeros(time, dtype=int)
    while True:
        tao = -1 / input_lambda * np.log(np.random.rand())
        buffer_time += tao
        if buffer_time <= 1:
            result[current_time] += 1
        else:
            new_message_time = int(np.floor(buffer_time))
            if current_time + new_message_time >= time:
                break
            current_time += new_message_time
            result[current_time] += 1
            buffer_time -= new_message_time
    return result


def get_experimental_values(input_lambda, time, queue_capacity):
    queue = []
    messages = generate_messages(input_lambda, time)
    total_queue_size = 0
    total_delay = 0
    total_queue_messages = 0
    total_success_messages = 0
    for i in range(len(messages)):
        total_queue_size += len(queue)
        if len(queue) > 0:
            processing_message = queue.pop(0)
            total_success_messages += 1
            delay = i - processing_message
            total_delay += delay
        if messages[i] > 0:
            for j in range(int(messages[i])):
                if len(queue) + 1 < queue_capacity:
                    queue.append(i)
                else:
                    break
            total_queue_messages += messages[i]
    mean_queue_size = total_queue_size / time
    mean_delay = total_delay / total_success_messages
    lambda_output = total_success_messages / time
    return mean_queue_size, mean_delay, lambda_output


def get_probably(degree, input_lambda):
    return np.math.pow(input_lambda, degree) * np.exp(-input_lambda) / np.math.factorial(degree)


def generate_matrix(input_lambda, b):
    states_num = b + 1
    p_matrix = np.zeros((states_num, states_num), dtype=float)
    for i in range(0, states_num - 1):
        p_matrix[0, i] = p_matrix[1, i] = get_probably(i, input_lambda)
    p_matrix[0, states_num - 1] = 1 - sum(p_matrix[0])
    p_matrix[1, states_num - 2] = 0
    for i in range(2, states_num - 1):
        deg = 0
        for j in range(i - 1, states_num - 2):
            p_matrix[i, j] = get_probably(deg, input_lambda)
            deg += 1
    for i in range(1, states_num - 1):
        p_matrix[i, states_num - 2] = 1 - sum(p_matrix[i])
    p_matrix[states_num - 1, states_num - 2] = 1
    for i in range(0, states_num):
        p_matrix[i, i] -= 1
    p_matrix = np.transpose(p_matrix)
    p_matrix[states_num - 1] = np.array([1] * states_num)
    return p_matrix


def get_theoretical_values(input_lambda, queue_capacity):
    p_matrix = generate_matrix(input_lambda, queue_capacity)
    vector = np.zeros(queue_capacity + 1)
    vector[-1] = 1
    p_i = np.linalg.solve(p_matrix, vector)
    mean_queue_size_th = 0
    for j in range(len(p_i)):
        mean_queue_size_th += j * p_i[j]
    output_lambda = 1 - p_i[0]
    mean_delay_th = mean_queue_size_th / output_lambda
    return mean_queue_size_th, mean_delay_th, output_lambda
