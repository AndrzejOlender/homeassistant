"""QueueManager::decorator."""
import asyncio
from functools import wraps
from queueman.helper import iscoroutine


def concurrent(concurrenttasks=15, sleepafter=0):
    """Return a modified function."""

    max_concurrent = asyncio.Semaphore(concurrenttasks)

    def inner_function(function):
        if not iscoroutine(function):
            print("Is not a coroutine")
            return function

        @wraps(function)
        async def wrapper(*args):

            async with max_concurrent:
                await function(*args)
                await asyncio.sleep(sleepafter)

        return wrapper

    return inner_function
