"""Deprecated compatibility imports.

Import shared DTOs from :mod:`gods_eye.contracts` instead.
"""

from gods_eye.contracts.execution import (
    CURRENT_REPOSITORY_VERSION,
    ExecutionRecord,
    ExecutionSnapshot,
    ExecutionStatus,
    ExecutionSummary,
    ModelInfo,
    PromptReference,
    SnapshotCreationMetrics,
    TerminalExecutionStatus,
)

__all__ = [
    "CURRENT_REPOSITORY_VERSION",
    "ExecutionRecord",
    "ExecutionSnapshot",
    "ExecutionStatus",
    "ExecutionSummary",
    "ModelInfo",
    "PromptReference",
    "SnapshotCreationMetrics",
    "TerminalExecutionStatus",
]
