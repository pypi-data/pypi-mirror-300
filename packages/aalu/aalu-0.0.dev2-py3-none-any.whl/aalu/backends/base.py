"""
Implements all base classes for backends
"""

from typing import Self
from abc import ABC, abstractmethod

from jsonalias import Json
from pydantic import BaseModel

from aalu.core.schemas import Metadata


class BaseBackend(ABC, BaseModel):
    """
    Base Class for all backends
    """

    tags: set[str]

    @classmethod
    @abstractmethod
    def default_instance(cls) -> Self | None:
        """
        Provides the default backend implementation
        """


class BaseBindBackend(BaseBackend, ABC):
    """
    Base Class for backends that implement a `persist_pair`
    function that binds to the functions to be traced.
    """

    @abstractmethod
    def persist(
        self,
        input_message: Json,
        output_message: Json,
        timestamp: int,
        duration: int,
        metadata: Metadata,
    ) -> None:
        """
        Implements signature to persist interaction
        """


class BaseDecorateBackend(BaseBackend, ABC):
    """
    Base Class for backends that implement a `persist`
    decorator to wrap functions to be traced.
    """

    @abstractmethod
    def persist(
        self,
        context_manager,
        input_message: Json,
        output_message: Json,
        timestamp: int,
        duration: int,
        metadata: Metadata,
    ) -> None:
        """
        Implements signature to persist interaction
        """

    @abstractmethod
    def get_context_manager(
        self,
        metadata: Metadata,
    ):
        """
        Returns the context manager for the target function
        """
