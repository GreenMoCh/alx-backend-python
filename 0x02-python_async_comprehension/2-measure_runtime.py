#!/usr/bin/env python3
""" Run time for four parallel comprehensions """

import asyncio
import time
from typing import List
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Measures and returns the total runtime of executing async_comprehension
    """
    start_time = time.time()
    tasks: List[asyncio.Task] = [async_comprehension() for _ in range(4)]
    await asyncio.gather(*tasks)
    end_time = time.time()
    total_runtime = end_time - start_time

    return total_runtime
    