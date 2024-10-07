"""
Implements a generic worker to be used for all LROs
"""

import typing
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult


from aalu import LOCAL_WORKERS

WORKERPOOL = Pool(LOCAL_WORKERS)
SCHEDULED_TASKS: list[AsyncResult] = []


def schedule_task(func: typing.Callable, args: tuple[typing.Any, ...]) -> None:
    """
    Schedules the given task on the global worker and stores the future
    """
    SCHEDULED_TASKS.append(WORKERPOOL.apply_async(func, args))


def safe_exit():
    """
    Waits for all pending tasks to complete
    """
    _ = [task.get() for task in SCHEDULED_TASKS]
