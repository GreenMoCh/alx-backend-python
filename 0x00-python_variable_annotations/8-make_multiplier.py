#!/usr/bin/python3
""" Complex types - functions """

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Return a function that multiplies a float by a given number
    """
    def multiplier_func(x: float) -> float:
        """
        Multiply a float by the given number
        """
        return x * multiplier

    return multiplier_func
    