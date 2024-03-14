#!/usr/bin/env python3
""" Complex types - mixed list """

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Return the sum of ints and floats in the given list
    """
    return sum(mxd_lst)
