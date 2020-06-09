from collections import OrderedDict

import numpy as np


def get_message_slots(frame_size):
    polynom = [(0.5, 2), (0.28, 3), (0.22, 8)]
    random_value = np.random.rand()
    message_slots = set()
    if random_value < polynom[0][0]:
        copy_count = 2
    elif random_value < polynom[0][0] + polynom[1][0]:
        copy_count = 3
    else:
        copy_count = 4
    while len(message_slots) != copy_count:
        message_slots.add(np.random.randint(0, frame_size))
    return sorted(message_slots)


def gen_subscriber_messages(subscriber_count, frame_size):
    slots = {}
    for i in range(subscriber_count):
        current_sub_messages = get_message_slots(frame_size)
        for j in current_sub_messages:
            current_slot = slots.get(j, None)
            if not current_slot:
                slots[j] = [i]
            else:
                slots[j].append(i)
    return OrderedDict(sorted(item for item in slots.items()))


def interference_cancellation(input_slots_state, buffer_size, frame_size, slot_number, subscriber_id):
    recovered_messages = 0
    for i in range(slot_number, frame_size):
        if subscriber_id in input_slots_state.get(i, []):
            input_slots_state[i].remove(subscriber_id)
    for i in range(slot_number, slot_number - buffer_size, -1):
        if len(input_slots_state.get(i, [])) == 1:
            recovered_messages += 1
            recovered_sub_id = input_slots_state.get(i)[0]
            interference_cancellation(input_slots_state, buffer_size, frame_size, i, recovered_sub_id)
        if slot_number - buffer_size < 0:
            break
    return recovered_messages


def decode_messages(input_slots_state, buffer_size, frame_size):
    decoded_messages = 0
    for current_slot, current_messages in input_slots_state.items():
        if len(current_messages) == 1:
            current_sub_id = current_messages[0]
            decoded_messages += 1 + interference_cancellation(input_slots_state,
                                                              buffer_size, frame_size, current_slot, current_sub_id)
    return decoded_messages
