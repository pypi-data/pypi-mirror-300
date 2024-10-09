import numpy as np

def round_up(value):
    rounded_value = np.round(value)
    if (value - np.floor(value)) == 0.5:
        rounded_value = np.ceil(value)
    return rounded_value