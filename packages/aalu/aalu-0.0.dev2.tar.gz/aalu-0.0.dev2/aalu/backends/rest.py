"""
Implements a backend that sends the interactions to a REST endpoint
"""

import os
import json
import typing
import warnings
from uuid import uuid4
from dataclasses import asdict

import requests
from loguru import logger
from jsonalias import Json

from aalu.core.schemas import Metadata
from aalu.backends.base import BaseBindBackend


class RestBackend(BaseBindBackend):
    """
    Implements a backend to send interactions to a REST endpoint
    """

    endpoint: str
    headers: dict[str, str]

    @classmethod
    def default_instance(cls) -> typing.Self | None:
        return (
            cls(
                endpoint=os.environ["AALU_API_ENDPOINT"],
                headers={"Authorization": f"Bearer {os.environ['AALU_API_KEY']}"},
                tags={"AALU_REST_BACKEND"},
            )
            if (os.getenv("AALU_API_ENDPOINT") and os.getenv("AALU_API_KEY"))
            else None
        )

    def model_post_init(self, __context: typing.Any) -> None:
        logger.info(f"Sending interactions to {self.endpoint}")
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
        try:
            response = requests.post(
                self.endpoint,
                headers={
                    **self.headers,
                    "Content-Type": "application/json",
                },
                data=json.dumps(
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
                ),
                timeout=10,
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            print(
                {
                    "input": input_message,
                    "output": output_message,
                    "metadata": metadata,
                    "backend_tags": list(self.tags),
                }
            )
            warnings.warn(str(e))
        else:
            if response.status_code != 200:
                warnings.warn(
                    f"Unable to send data to the endpoint : {response.status_code}"
                )
