#!/usr/bin/env python3
""" Let's duck type an iterable object """

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Calculate the length of elements in the given list
    """
    return [(i, len(i)) for i in lst]
