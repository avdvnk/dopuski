import numpy as np

import nir.constants as const
import nir.functions as func
import nir.plot_functions as plot

if __name__ == '__main__':
    FRAME_COUNT = 20000
    SLOTS_COUNT = 200
    BUFFER_SIZE = SLOTS_COUNT
    g_value = np.arange(0.05, 1.05, 0.05)

    plr = {}
    plr_approximation = {}
    throughput = {}
    throughput_approximation = {}

    for polynom_name, polynom_value in const.polynoms.items():
        result = {}
        failed_result = {}
        g_max = const.g_max_values.get(polynom_name)
        a_0 = const.a_0_values.get(polynom_name)
        b_0 = const.b_0_values.get(polynom_name)
        gamma = const.gamma_values.get(polynom_name)
        current_throughput = []
        current_throughput_approximation = []
        current_plr_approximation = []
        for current_g in g_value:
            decoded_messages = 0
            for i in range(FRAME_COUNT):
                # subs_count = int(current_g * SLOTS_COUNT)  # for fixed m subscribers
                subs_count = np.random.poisson(current_g * SLOTS_COUNT)  # for Poisson m subscribers
                if subs_count < 1:
                    subs_count = 1
                slots = func.gen_subscriber_messages(polynom_value, subs_count, SLOTS_COUNT)
                decoded_messages = func.decode_messages(slots, BUFFER_SIZE, SLOTS_COUNT)
                failed_messages = subs_count - decoded_messages
                result[current_g] = result.get(current_g, 0) + decoded_messages / subs_count
                failed_result[current_g] = failed_result.get(current_g, 0) + failed_messages / subs_count
            current_throughput.append(current_g * result.get(current_g, 0))
            current_plr_approximation.append(func.get_approximation_plr(SLOTS_COUNT, current_g, g_max, a_0, b_0, gamma))
            current_throughput_approximation.append(current_g * (1 - current_plr_approximation[-1]))
            print("Polynom: {}, g: {} was finished".format(polynom_name, current_g))
        mean_decoded_messages = np.fromiter(result.values(), dtype=float) / FRAME_COUNT
        current_plr = np.fromiter(failed_result.values(), dtype=float) / FRAME_COUNT
        current_throughput = np.array(mean_decoded_messages * g_value)
        plr[polynom_name] = current_plr
        plr_approximation[polynom_name] = current_plr_approximation
        throughput[polynom_name] = current_throughput
        throughput_approximation[polynom_name] = current_throughput_approximation
        print("{} is finished".format(polynom_name))

    plot.plot_plr(plr, plr_approximation, g_value)
    plot.plot_throughput(throughput, throughput_approximation, g_value)
