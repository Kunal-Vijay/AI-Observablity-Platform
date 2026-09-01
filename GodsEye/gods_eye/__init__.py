"""God's Eye instrumentation SDK."""

from gods_eye.contracts import ExecutionSnapshot, ModelInfo, PromptReference
from gods_eye.execution.active import get_active_execution, record_metadata
from gods_eye.execution.context import ExecutionContext, prompt_reference
from gods_eye.execution_stream import ExecutionStream, InMemoryExecutionStream
from gods_eye.plugins import Plugin
from gods_eye.repositories.execution_repository import ExecutionRepository
from gods_eye.repositories.trace_repository import TraceRepository
from gods_eye.sdk.configure import (
    InstrumentationSettings,
    configure,
    get_settings,
    reset_configuration,
)
from gods_eye.sdk.correlation import (
    get_current_execution_id,
    get_current_execution_latency_ms,
    get_current_trace_id,
)
from gods_eye.sdk.instrumentation import GodsEye, execution, span
from gods_eye.sdk.metadata import ExecutionMetadata, ObservedResult
from gods_eye.sdk.observe_execution import observe_execution
from gods_eye.tracing.observe import observe

from . import contracts as Contracts

# Source-compatible names from the pre-freeze API. They are intentionally
# omitted from __all__ and from customer documentation.
_COMPATIBILITY_EXPORTS = (
    ExecutionContext,
    ExecutionMetadata,
    ExecutionRepository,
    ExecutionSnapshot,
    InMemoryExecutionStream,
    InstrumentationSettings,
    ModelInfo,
    ObservedResult,
    PromptReference,
    TraceRepository,
    get_active_execution,
    get_settings,
    observe,
    observe_execution,
    prompt_reference,
    record_metadata,
    reset_configuration,
)

__all__ = [
    "Contracts",
    "ExecutionStream",
    "Plugin",
    "GodsEye",
    "configure",
    "execution",
    "get_current_execution_id",
    "get_current_execution_latency_ms",
    "get_current_trace_id",
    "span",
]

__version__ = "2.0.0"
