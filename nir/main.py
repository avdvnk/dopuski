import numpy as np
from matplotlib import pyplot

import nir.functions as func

if __name__ == '__main__':
    FRAME_COUNT = 10000
    SLOTS_COUNT = 200
    my_lambda = 0.8
    BUFFER_SIZE = 10
    g_value = np.arange(0.05, 1.05, 0.05)

    result = {}
    failed_packages = {}
    for current_g in g_value:
        for i in range(FRAME_COUNT):
            subs_count = int(current_g * SLOTS_COUNT)
            slots = func.gen_subscriber_messages(subs_count, SLOTS_COUNT)
            decoded_messages = func.decode_messages(slots, BUFFER_SIZE, SLOTS_COUNT)
            result[current_g] = result.get(current_g, 0) + decoded_messages / subs_count
            failed_packages[current_g] = failed_packages.get(current_g, 0) + \
                                         (subs_count - decoded_messages) / subs_count
    mean_decoded_messages = np.fromiter(result.values(), dtype=float) / FRAME_COUNT
    mean_lost_messages = np.fromiter(failed_packages.values(), dtype=float) / FRAME_COUNT
    pyplot.plot(g_value, mean_lost_messages)
    pyplot.savefig("result.png")
