import numpy as np
from matplotlib import pyplot

import task4.functions as func

if __name__ == '__main__':
    T = 10000
    queue_capacity = 10

    start, end, step = 0.1, 1.1, 0.1
    array_lambda = np.arange(start, end, step)

    n = []
    delay = []
    n_th = []
    delay_th = []
    for i in array_lambda:
        experimental_n, experimental_delay = func.get_experimental_values(i, T, queue_capacity)
        theoretical_n, theoretical_delay = func.get_theoretical_values(i, queue_capacity)
        n.append(experimental_n)
        delay.append(experimental_delay)

        n_th.append(theoretical_n)
        delay_th.append(theoretical_delay)

    pyplot.plot(array_lambda, n, label="experimental")
    pyplot.plot(array_lambda, n_th, label="theoretical")
    pyplot.legend()
    pyplot.savefig("result_queue_size.png")

    pyplot.clf()

    pyplot.plot(array_lambda, delay, label="experimental")
    pyplot.plot(array_lambda, delay_th, label="theoretical")
    pyplot.legend()
    pyplot.savefig("result_delay.png")
