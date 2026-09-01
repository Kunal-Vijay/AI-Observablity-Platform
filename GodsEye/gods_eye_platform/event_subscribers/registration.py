"""Register Platform persistence consumers on an execution stream."""

from gods_eye.execution_stream import (
    ExecutionCancelled,
    ExecutionCompleted,
    ExecutionEventSubscriber,
    ExecutionFailed,
    ExecutionStarted,
    ExecutionStream,
    TraceCompleted,
)
from gods_eye_platform.event_subscribers.execution import (
    ExecutionCancelledSubscriber,
    ExecutionCompletedSubscriber,
    ExecutionFailedSubscriber,
    ExecutionStartedSubscriber,
)
from gods_eye_platform.event_subscribers.trace import TraceCompletedSubscriber
from gods_eye_platform.execution_store import TracePersister
from gods_eye_platform.repositories.execution import (
    ExecutionLifecycleRepository,
    ExecutionSnapshotRepository,
)


def register_persistence_subscribers(
    stream: ExecutionStream,
    *,
    executions: ExecutionLifecycleRepository,
    snapshots: ExecutionSnapshotRepository,
    trace_persister: TracePersister,
) -> tuple[ExecutionEventSubscriber, ...]:
    """Attach the current Platform persistence projections to a stream."""
    subscribers: tuple[ExecutionEventSubscriber, ...] = (
        ExecutionStartedSubscriber(executions),
        ExecutionCompletedSubscriber(executions, snapshots),
        ExecutionFailedSubscriber(executions, snapshots),
        ExecutionCancelledSubscriber(executions, snapshots),
        TraceCompletedSubscriber(trace_persister),
    )
    stream.subscribe(ExecutionStarted, subscribers[0])
    stream.subscribe(ExecutionCompleted, subscribers[1])
    stream.subscribe(ExecutionFailed, subscribers[2])
    stream.subscribe(ExecutionCancelled, subscribers[3])
    stream.subscribe(TraceCompleted, subscribers[4])
    return subscribers
