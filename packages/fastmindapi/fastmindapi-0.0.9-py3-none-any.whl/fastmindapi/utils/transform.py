import numpy as np
import math

def convert_numpy_float32_to_float(d):
    if isinstance(d, dict):
        return {k: convert_numpy_float32_to_float(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_numpy_float32_to_float(item) for item in d]
    elif isinstance(d, np.float32):
        return float(d)
    else:
        return d
    
def clean_dict_null_value(d):
    # return { k:d[k] for k in d if d[k] }
    new_d = {}
    for k in d:
        if not d[k]:
            continue
        if type(d[k]) == float and math.isnan(d[k]):
            continue
        new_d[k] = d[k]
    return new_d
