"""QueueManager::helper."""
import asyncio


def iscoroutine(function):
    """Return a bool if a function is a coroutine."""
    return asyncio.iscoroutinefunction(function)
