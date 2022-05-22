from dataclasses import dataclass
import numpy as np


@dataclass
class TableFunction:
    n: int
    x_arr: list[float]
    y_arr: list[float]


function_types_arr = [
    'f(x) = sqrt(x)',
    'f(x) = sin(x)',
    'f(x) = x^3'
]


def get_function_result(func_type: int, x: float):
    try:
        if func_type == 0:
            if x < 0:
                raise ValueError
            return np.sqrt(x)
        elif func_type == 1:
            return np.sin(x)
        elif func_type == 2:
            return x**3
    except ValueError:
        return None
