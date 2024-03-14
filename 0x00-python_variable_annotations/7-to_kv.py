#!/usr/bin/python3
""" Complex types - string and int/float to tuple """

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Return a tuple contaning the str k and the square of the int or float v
    """
    return k, float(v ** 2)
    