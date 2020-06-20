from collections import OrderedDict

import numpy as np
from scipy import stats


def generate_message(input_lambda, frame_size, count):
    current_time = 0
    result = set()
    while len(result) != count:
        current_time += np.random.poisson(input_lambda * frame_size)
        result.add(int(current_time) % frame_size)
    return result


def generate_message_set_random(start, frame_size, count):
    result_set = set()
    while len(result_set) != count:
        result_set.add(np.random.randint(low=start, high=frame_size))
    return result_set


def get_message_slots(polynom, frame_size):
    current_prob = 0
    copy_count = 0
    random_value = np.random.rand()
    for prob, count in polynom:
        current_prob += prob
        if random_value < current_prob:
            copy_count = count
            break
    message_slots = generate_message_set_random(0, frame_size, copy_count)
    return message_slots


def gen_subscriber_messages(polynom, subscriber_count, frame_size):
    slots = {}
    for i in range(subscriber_count):
        current_sub_messages = get_message_slots(polynom, frame_size)
        for j in current_sub_messages:
            current_slot = slots.get(j, None)
            if not current_slot:
                slots[j] = [i]
            else:
                slots[j].append(i)
    return OrderedDict(sorted(item for item in slots.items()))


def interference_cancellation(input_slots_state, buffer_size, frame_size, slot_number, subscriber_id):
    recovered_messages = 0
    for current_slot, current_messages in input_slots_state.items():
        if subscriber_id in current_messages:
            current_messages.remove(subscriber_id)
    for current_slot, current_messages in input_slots_state.items():
        if current_slot > slot_number:
            break
        if len(current_messages) == 1:
            recovered_sub_id = current_messages[0]
            recovered_messages += 1 + interference_cancellation(input_slots_state, buffer_size, frame_size,
                                                                slot_number, recovered_sub_id)
    return recovered_messages


def decode_messages(input_slots_state, buffer_size, frame_size):
    decoded_messages = 0
    for current_slot, current_messages in input_slots_state.items():
        if len(current_messages) == 1:
            current_sub_id = current_messages[0]
            decoded_messages += 1 + interference_cancellation(input_slots_state,
                                                              buffer_size, frame_size, current_slot, current_sub_id)
    return decoded_messages


def get_input_q_func(frame_size, g_value, g_max, alpha, betta):
    a_g0 = np.sqrt(np.power(alpha, 2) + g_value)
    return (np.sqrt(frame_size) * (g_max - betta * np.power(frame_size, -2 / 3) - g_value)) / a_g0


def get_approximation_plr(frame_size, g_value, g_max, alpha, betta, gamma):
    q_input = get_input_q_func(frame_size, g_value, g_max, alpha, betta)
    q_func = stats.norm.sf(q_input)
    return gamma * q_func
