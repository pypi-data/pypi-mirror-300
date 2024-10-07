"""
Implements decorators
"""

import typing
import inspect
import functools
from contextlib import ExitStack
from datetime import datetime, UTC

from jsonalias import Json

from aalu.core.worker import schedule_task
from aalu.backends.base import (
    Metadata,
    BaseBackend,
    BaseBindBackend,
    BaseDecorateBackend,
)


def get_default_dict(func: typing.Callable) -> dict:
    """
    Returns the default args of a function
    """

    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_args_dict(func: typing.Callable, *args) -> dict:
    """
    Returns the default args of a function
    """

    return dict(zip(func.__code__.co_varnames, args))


def get_input_dict(func, *args, **kwargs) -> dict[str, typing.Any]:
    """
    Creates and returns a dictionary with all of the provided args
    and kwargs combined with any unspecified default parameters.
    """
    return {
        **get_default_dict(func),
        **get_args_dict(func, args),
        **kwargs,
    }


SerializerSourceType = typing.Literal["input", "output", "metadata"]

T = typing.TypeVar("T")
P = typing.ParamSpec("P")


@typing.overload
def auto_wrapper(
    metadata: Metadata,
    serializer: typing.Callable[[SerializerSourceType, str, typing.Any], Json],
    backends: list[BaseBackend],
    target_function: typing.Callable[P, typing.Awaitable[T]],
) -> typing.Callable[P, typing.Awaitable[T]]: ...


@typing.overload
def auto_wrapper(
    metadata: Metadata,
    serializer: typing.Callable[[SerializerSourceType, str, typing.Any], Json],
    backends: list[BaseBackend],
    target_function: typing.Callable[P, typing.Generator[T, typing.Any, typing.Any]],
) -> typing.Callable[P, typing.Generator[T, typing.Any, typing.Any]]: ...


@typing.overload
def auto_wrapper(
    metadata: Metadata,
    serializer: typing.Callable[[SerializerSourceType, str, typing.Any], Json],
    backends: list[BaseBackend],
    target_function: typing.Callable[P, T],
) -> typing.Callable[P, T]: ...


def auto_wrapper(
    metadata: Metadata,
    serializer: typing.Callable[[SerializerSourceType, str, typing.Any], Json],
    backends: list[BaseBackend],
    target_function: typing.Callable[P, T],
) -> (
    typing.Callable[P, T]
    | typing.Callable[P, typing.Awaitable[T]]
    | typing.Callable[P, typing.Generator[T, typing.Any, typing.Any]]
):
    """
    Dynamically wraps the given function
    """

    is_async = inspect.iscoroutinefunction(target_function)
    is_gener = inspect.isgeneratorfunction(target_function)

    persist_functions = [b for b in backends if isinstance(b, BaseBindBackend)]
    persist_decorators = [b for b in backends if isinstance(b, BaseDecorateBackend)]

    def persist_handler(input_message, output_message, timestamp, duration, metadata):
        """
        Queues all backend persist functions
        """
        for pf in persist_functions:
            schedule_task(
                pf.persist,
                (input_message, output_message, timestamp, duration, metadata),
            )

    if is_async:
        if is_gener:

            @functools.wraps(target_function)
            async def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                output_message = []
                input_message = serializer(
                    "input",
                    metadata.func_lineage,
                    get_input_dict(target_function, *args, **kwargs),
                )

                with ExitStack() as stack:
                    cms = [
                        (
                            stack.enter_context(d.get_context_manager(metadata)()),
                            d.persist,
                        )
                        for d in persist_decorators
                    ]
                    timestamp = int(datetime.now(UTC).timestamp() * (10**6))
                    target_result = await typing.cast(
                        typing.Awaitable, target_function(*args, **kwargs)
                    )
                    duration = int(datetime.now(UTC).timestamp() * (10**6)) - timestamp
                    async for result in target_result:
                        output_message.append(result)
                        yield result

                    for context_manager, persist_func in cms:
                        persist_func(
                            context_manager,
                            input_message=input_message,
                            output_message=serializer(
                                "output", metadata.func_lineage, output_message
                            ),
                            timestamp=timestamp,
                            duration=duration,
                            metadata=metadata,
                        )

                persist_handler(
                    input_message, output_message, timestamp, duration, metadata
                )

            return wrapped_func

        else:

            @functools.wraps(target_function)
            async def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                input_message = serializer(
                    "input",
                    metadata.func_lineage,
                    get_input_dict(target_function, *args, **kwargs),
                )

                with ExitStack() as stack:
                    cms = [
                        (
                            stack.enter_context(d.get_context_manager(metadata)()),
                            d.persist,
                        )
                        for d in persist_decorators
                    ]
                    timestamp = int(datetime.now(UTC).timestamp() * (10**6))

                    output_message = await typing.cast(
                        typing.Awaitable, target_function(*args, **kwargs)
                    )
                    duration = int(datetime.now(UTC).timestamp() * (10**6)) - timestamp

                    for context_manager, persist_func in cms:
                        persist_func(
                            context_manager,
                            input_message=input_message,
                            output_message=serializer(
                                "output", metadata.func_lineage, [output_message]
                            ),
                            timestamp=timestamp,
                            duration=duration,
                            metadata=metadata,
                        )

                persist_handler(
                    input_message, [output_message], timestamp, duration, metadata
                )

                return output_message

            return wrapped_func

    else:
        if is_gener:

            @functools.wraps(target_function)
            def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                output_message = []
                input_message = serializer(
                    "input",
                    metadata.func_lineage,
                    get_input_dict(target_function, *args, **kwargs),
                )

                with ExitStack() as stack:
                    cms = [
                        (
                            stack.enter_context(d.get_context_manager(metadata)()),
                            d.persist,
                        )
                        for d in persist_decorators
                    ]
                    timestamp = int(datetime.now(UTC).timestamp() * (10**6))

                    target_result = typing.cast(
                        typing.Generator, target_function(*args, **kwargs)
                    )
                    duration = int(datetime.now(UTC).timestamp() * (10**6)) - timestamp

                    for result in target_result:
                        output_message.append(result)
                        yield result

                    for context_manager, persist_func in cms:
                        persist_func(
                            context_manager,
                            input_message=input_message,
                            output_message=serializer(
                                "output", metadata.func_lineage, output_message
                            ),
                            timestamp=timestamp,
                            duration=duration,
                            metadata=metadata,
                        )

                persist_handler(
                    input_message, output_message, timestamp, duration, metadata
                )

            return wrapped_func

        else:

            @functools.wraps(target_function)
            def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                input_message = serializer(
                    "input",
                    metadata.func_lineage,
                    get_input_dict(target_function, *args, **kwargs),
                )
                with ExitStack() as stack:
                    cms = [
                        (
                            stack.enter_context(d.get_context_manager(metadata)()),
                            d.persist,
                        )
                        for d in persist_decorators
                    ]
                    timestamp = int(datetime.now(UTC).timestamp() * (10**6))
                    output_message = target_function(*args, **kwargs)
                    duration = int(datetime.now(UTC).timestamp() * (10**6)) - timestamp

                    for context_manager, persist_func in cms:
                        persist_func(
                            context_manager,
                            input_message=input_message,
                            output_message=serializer(
                                "output", metadata.func_lineage, [output_message]
                            ),
                            timestamp=timestamp,
                            duration=duration,
                            metadata=metadata,
                        )
                persist_handler(
                    input_message, [output_message], timestamp, duration, metadata
                )

                return output_message

            return wrapped_func
