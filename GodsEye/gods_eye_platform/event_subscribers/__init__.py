"""Platform consumers that project execution facts into persistence."""

from gods_eye_platform.event_subscribers.execution import (
    ExecutionCancelledSubscriber,
    ExecutionCompletedSubscriber,
    ExecutionFailedSubscriber,
    ExecutionStartedSubscriber,
)
from gods_eye_platform.event_subscribers.registration import (
    register_persistence_subscribers,
)
from gods_eye_platform.event_subscribers.trace import TraceCompletedSubscriber

__all__ = [
    "ExecutionCancelledSubscriber",
    "ExecutionCompletedSubscriber",
    "ExecutionFailedSubscriber",
    "ExecutionStartedSubscriber",
    "TraceCompletedSubscriber",
    "register_persistence_subscribers",
]
