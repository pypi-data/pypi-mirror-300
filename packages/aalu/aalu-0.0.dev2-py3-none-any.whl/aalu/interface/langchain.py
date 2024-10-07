"""
Implements a Langchain Runnable wrapper
"""

import typing
from functools import wraps

from loguru import logger
from jsonalias import Json
from langchain_core.load import dumpd
from langchain_core.runnables import Runnable, RunnableSequence

from aalu.core import DEFAULT_NAMESPACE
from aalu.core.schemas import Metadata
from aalu.backends import DEFAULT_BACKEND
from aalu.backends.base import BaseBackend
from aalu.interface.base import auto_wrapper, SerializerSourceType


function_targets = [
    "batch",
    "stream",
    "invoke",
    "abatch",
    "astream",
    "ainvoke",
    "astream_log",
    "astream_events",
]


def serializer(source: SerializerSourceType, funcname: str, arg: typing.Any) -> Json:
    """
    Makes LLM interactions Serializable
    """
    return dumpd(arg)


T = typing.TypeVar("T", Runnable, RunnableSequence)


def wrap(
    runnable: T,
    namespace: str = DEFAULT_NAMESPACE,
    backends: BaseBackend | list[BaseBackend] | None = DEFAULT_BACKEND,
    tags: set[str] | None = None,
) -> T:
    """
    Wraps a given Runnable/RunnableSequence Object and attaches it to given backends
    """

    logger.info(f"Using namespace {namespace}")

    if backends is None:
        backends = []
    elif isinstance(backends, BaseBackend):
        backends = [backends]

    if tags is None:
        tags = set()

    if isinstance(runnable, RunnableSequence):
        first = (
            wrap(runnable.first, f"{namespace}.0", backends, tags)
            if (
                isinstance(runnable.first, Runnable)
                or isinstance(runnable.first, RunnableSequence)
            )
            else runnable.first
        )
        middle = [
            wrap(r, f"{namespace}.{e+1}", backends, tags)
            if (isinstance(r, Runnable) or isinstance(r, RunnableSequence))
            else r
            for e, r in enumerate(runnable.middle)
        ]

        last = (
            wrap(runnable.last, f"{namespace}.{1+len(middle)}", backends, tags)
            if (
                isinstance(runnable.last, Runnable)
                or isinstance(runnable.last, RunnableSequence)
            )
            else runnable.last
        )

        runnable = RunnableSequence(first=first, middle=middle, last=last)

    if backends:
        runnable_dump = dumpd(runnable)

        for target_name in function_targets:
            target_func = getattr(runnable, target_name)
            metadata = Metadata(
                func_lineage=f"{target_func.__module__}.{target_func.__qualname__}",
                namespace=namespace,
                interface="langchain",
                func_name=target_name,
                tags=list(tags),
                object_dump=runnable_dump,
            )

            object.__setattr__(
                runnable,
                target_name,
                wraps(target_func)(
                    auto_wrapper(metadata, serializer, backends, target_func)
                ),
            )

    return runnable
