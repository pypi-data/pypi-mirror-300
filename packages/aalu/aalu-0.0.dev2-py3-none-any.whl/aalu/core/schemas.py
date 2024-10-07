"""
Defines generic schemas and models
"""

import uuid
import json
from dataclasses import dataclass, field

from jsonalias import Json
from flatten_json import flatten


@dataclass
class PersistModel:
    """
    Schema of the object to persist
    """

    # pylint: disable=invalid-name

    id: str
    name: str
    timestamp: int
    duration: int
    debug: bool = False
    kind: str | None = None
    traceId: str | None = None
    tags: dict[
        str, str | bool | float | int | list[str] | list[bool] | list[float] | list[int]
    ] = field(default_factory=dict)
    localEndpoint: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if self.traceId is not None:
            assert (
                self.traceId == uuid.UUID(self.traceId, version=4).hex
            ), "Invalid TraceID"


@dataclass
class Metadata:
    """
    Defines the schema of static metadata to be persisted
    """

    namespace: str
    interface: str
    func_name: str
    tags: list[str]
    func_lineage: str
    object_dump: Json | None

    def to_persistmodel(
        self,
        span_id: str,
        timestamp: int,
        duration: int,
        input_message: Json,
        output_message: Json,
        debug: bool = False,
        kind: str | None = None,
        trace_id: str | None = None,
        local_endpoint: dict[str, str] | None = None,
        **kwargs,
    ):
        """
        Converts metadata to PersistModel
        """
        return PersistModel(
            traceId=trace_id,
            id=span_id,
            name=self.func_lineage,
            timestamp=timestamp,
            duration=duration,
            debug=debug,
            kind=kind,
            tags={
                "metadata.namespace": self.namespace,
                "metadata.interface": self.interface,
                "metadata.func_name": self.func_name,
                "metadata.tags": self.tags,
                "metadata.func_lineage": self.func_lineage,
                **{
                    k: (
                        v
                        if isinstance(v, str)
                        else json.dumps(v, ensure_ascii=False, default=str)
                    )
                    for k1, v1 in (
                        ("metadata.object_dump", self.object_dump),
                        ("input", input_message),
                        ("output", output_message),
                    )
                    for k, v in flatten({k1: v1}, ".").items()
                },
                **kwargs,
            },
            localEndpoint=(local_endpoint or {}),
        )
