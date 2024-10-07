"""
Provides the default backend
"""

from aalu.backends.file import FileBackend
from aalu.backends.rest import RestBackend
from aalu.backends.otel import OtelBackend

DEFAULT_BACKEND = (
    OtelBackend.default_instance()
    or RestBackend.default_instance()
    or FileBackend.default_instance()
)
