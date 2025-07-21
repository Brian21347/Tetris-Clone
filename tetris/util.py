"""
A collection of helper functions.
"""

from constants import Pii


def add_pii(*args: Pii) -> Pii:
    sum_vec = (0, 0)
    for vec in args:
        sum_vec = sum_vec[0] + vec[0], sum_vec[1] + vec[1]
    return sum_vec


def scale_pii(vector: Pii, scale_factor) -> Pii:
    return tuple(val * scale_factor for val in vector)
