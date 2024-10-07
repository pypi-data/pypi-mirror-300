"""
Implements a backend that saves the interactions to a file
"""

import os
import json
import typing
import tempfile
from uuid import uuid4
from dataclasses import asdict

from loguru import logger
from jsonalias import Json
from smart_open import parse_uri, open as smart_open

from aalu.core.schemas import Metadata
from aalu.backends.base import BaseBindBackend


class FileBackend(BaseBindBackend):
    """
    Implements a backend to store interactions to a file
    """

    path: str
    transport_params: dict[str, typing.Any] | None = None

    @classmethod
    def default_instance(cls) -> typing.Self:
        return cls(
            path=tempfile.TemporaryDirectory().name, tags={"DEFAULT_LOCAL_FILE_BACKEND"}
        )

    def model_post_init(self, __context: typing.Any) -> None:
        logger.info(f"Storing interactions to {self.path}")
        return super().model_post_init(__context)

    def persist(
        self,
        input_message: Json,
        output_message: Json,
        timestamp: int,
        duration: int,
        metadata: Metadata,
    ) -> None:
        span_id = uuid4().hex
        persist_path = os.path.join(self.path, metadata.namespace)
        persist_file = os.path.join(persist_path, f"{span_id}.json")

        if parse_uri(persist_path).scheme == "file":
            os.makedirs(persist_path, exist_ok=True)
        with smart_open(
            persist_file, "w", transport_params=self.transport_params
        ) as fout:
            fout.write(
                json.dumps(
                    [
                        asdict(
                            metadata.to_persistmodel(
                                span_id=span_id,
                                timestamp=timestamp,
                                duration=duration,
                                input_message=input_message,
                                output_message=output_message,
                            )
                        )
                    ]
                )
            )
