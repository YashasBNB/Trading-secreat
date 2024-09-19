import numpy as np

def find_support_resistance(data):
    data['high_shift'] = data['high'].shift(1)
    data['low_shift'] = data['low'].shift(1)

    resistance = np.max(data['high_shift'][-20:])
    support = np.min(data['low_shift'][-20:])

    return support, resistance
