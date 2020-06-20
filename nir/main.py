import numpy as np
from matplotlib import pyplot

import nir.functions as func

if __name__ == '__main__':
    FRAME_COUNT = 20000
    SLOTS_COUNT = 200
    BUFFER_SIZE = SLOTS_COUNT
    g_value = np.arange(0.05, 1.05, 0.05)

    # polynom = [(0.5, 2), (0.28, 3), (0.22, 8)]
    polynom = [(1, 3)]
    g_max = 0.818469
    a_0 = 0.404986
    b_0 = 0.849037
    gamma = 0.982040

    result = {}
    failed_result = {}
    throughput = []
    plr_approximation = []
    throughput_approximation = []
    for current_g in g_value:
        decoded_messages = 0
        for i in range(FRAME_COUNT):
            # subs_count = int(current_g * SLOTS_COUNT)  # for fixed m subscribers
            subs_count = np.random.poisson(current_g * SLOTS_COUNT)  # for Poisson m subscribers
            if subs_count < 1:
                subs_count = 1
            slots = func.gen_subscriber_messages(polynom, subs_count, SLOTS_COUNT)
            decoded_messages = func.decode_messages(slots, BUFFER_SIZE, SLOTS_COUNT)
            failed_messages = subs_count - decoded_messages
            result[current_g] = result.get(current_g, 0) + decoded_messages / subs_count
            failed_result[current_g] = failed_result.get(current_g, 0) + failed_messages / subs_count
        throughput.append(current_g * result.get(current_g, 0))
        plr_approximation.append(func.get_approximation_plr(SLOTS_COUNT, current_g, g_max, a_0, b_0, gamma))
        throughput_approximation.append(current_g * (1 - plr_approximation[-1]))
        print("{} is finished".format(current_g))
    mean_decoded_messages = np.fromiter(result.values(), dtype=float) / FRAME_COUNT
    mean_lost_messages = np.fromiter(failed_result.values(), dtype=float) / FRAME_COUNT
    throughput = np.array(mean_decoded_messages * g_value)

    pyplot.ylim(10 ** -7, 10 ** 0)
    pyplot.xticks(np.arange(0, 1.1, 0.1))
    pyplot.xlabel("G")
    pyplot.ylabel("Package Loss Rate (PLR)")
    pyplot.semilogy(g_value, mean_lost_messages)
    pyplot.semilogy(g_value, plr_approximation, "--r")
    pyplot.savefig("plr.png")

    pyplot.clf()

    pyplot.ylim(0, 1)
    pyplot.xticks(np.arange(0, 1.1, 0.1))
    pyplot.xlabel("G")
    pyplot.ylabel("Throughput")
    pyplot.plot(g_value, throughput)
    pyplot.plot(g_value, throughput_approximation, "--r")
    pyplot.savefig("throughput.png")
