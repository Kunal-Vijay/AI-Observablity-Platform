"""Deprecated compatibility imports.

Import shared DTOs from :mod:`gods_eye.contracts` instead.
"""

from gods_eye.contracts.tracing import (
    Span,
    SpanRecord,
    SpanStatus,
    Trace,
    TraceRecord,
)

__all__ = [
    "Span",
    "SpanRecord",
    "SpanStatus",
    "Trace",
    "TraceRecord",
]
