"""
A collection of helper functions.
"""
from constants import Pii


def add_vectors(*args: tuple[Pii, ...]) -> Pii:
    sum_vec = [0] * len(args[0])
    for vec in args:
        sum_vec = [val1 + val2 for val1, val2 in zip(vec, sum_vec, strict=True)]
    return sum_vec


def scale_vector(vector: Pii, scale_factor) -> Pii:
    return [val * scale_factor for val in vector]
