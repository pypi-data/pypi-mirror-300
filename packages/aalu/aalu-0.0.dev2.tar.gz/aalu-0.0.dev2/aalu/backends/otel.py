"""
Implements a backend that sends the interactions to Open Telemtry
"""

import os
import typing
from uuid import uuid4
from functools import partial
from dataclasses import asdict

import requests
from loguru import logger
from jsonalias import Json
from pydantic import ConfigDict
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.zipkin.json import ZipkinExporter

from aalu.core.schemas import Metadata
from aalu.backends.base import BaseDecorateBackend


class OtelBackend(BaseDecorateBackend):
    """
    Implements a backend to send interactions to Open Telemtry
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    span_processors: list[SpanProcessor] = []

    @classmethod
    def default_instance(cls) -> typing.Self | None:
        return (
            cls.with_zipkin_processor(
                endpoint=os.environ["AALU_API_ENDPOINT"],
                headers={"X-Api-Key": os.environ["AALU_API_KEY"]},
                tags={"AALU_REST_BACKEND"},
            )
            if (os.getenv("AALU_API_ENDPOINT") and os.getenv("AALU_API_KEY"))
            else None
        )

    def model_post_init(self, __context: typing.Any) -> None:
        logger.info(
            f"Sending interactions to {len(self.span_processors)} OTel Processors"
        )

        tracer_provider = TracerProvider()
        for span_processor in self.span_processors:
            tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        return super().model_post_init(__context)

    @classmethod
    def with_zipkin_processor(
        cls, endpoint: str, headers: dict[str, str], tags: set[str]
    ):
        """
        Creattes an OTelBackend with a Zipkin Span processor
        """

        s = requests.session()
        s.headers.update(
            {
                **headers,
                "Content-Type": "application/json",
            }
        )
        return cls(
            span_processors=[
                BatchSpanProcessor(
                    ZipkinExporter(
                        endpoint=endpoint,
                        session=s,
                    )
                )
            ],
            tags=tags,
        )

    def get_context_manager(
        self,
        metadata: Metadata,
    ):
        """
        Returns the context manager for the target function
        """
        tracer = trace.get_tracer(metadata.namespace)
        return partial(tracer.start_as_current_span, name=metadata.func_lineage)

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
        tags = asdict(
            metadata.to_persistmodel(
                span_id=uuid4().hex,
                timestamp=timestamp,
                duration=duration,
                input_message=input_message,
                output_message=output_message,
            )
        )["tags"]
        for tagname, tagval in tags.items():
            context_manager.set_attribute(tagname, tagval)
