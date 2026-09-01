from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, InterfaceError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sentinelai_platform.persistence.postgres.models_span import SpanModel
from sentinelai_platform.persistence.postgres.models_trace import TraceModel
from sentinelai_platform.projections import SpanRecord, TraceRecord
from sentinelai_platform.repositories.trace import TraceRepository

_STALE_CONNECTION_MARKERS = (
    "connection was closed",
    "connectiondoesnotexist",
    "server closed the connection",
    "the connection is closed",
)


def _is_stale_connection(exc: BaseException) -> bool:
    message = str(exc).lower()
    return any(marker in message for marker in _STALE_CONNECTION_MARKERS)


class PostgresTraceRepository(TraceRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(
        self,
        trace: TraceRecord,
        spans: list[SpanRecord],
    ) -> TraceRecord:
        last_error: BaseException | None = None
        for attempt in range(2):
            try:
                async with self._session_factory() as session:
                    trace_row = TraceModel(
                        trace_id=trace.trace_id,
                        execution_id=trace.execution_id,
                        status=trace.status,
                        span_count=trace.span_count,
                        latency_ms=trace.latency_ms,
                        storage_path=trace.storage_path,
                        created_at=trace.created_at,
                    )
                    session.add(trace_row)
                    # TraceModel has no ORM relationship to SpanModel, so force the
                    # parent row to exist before inserting children with a trace FK.
                    await session.flush()
                    for span in spans:
                        session.add(
                            SpanModel(
                                span_id=span.span_id,
                                trace_id=span.trace_id,
                                parent_span_id=span.parent_span_id,
                                span_type=span.span_type,
                                latency_ms=span.latency_ms,
                                model=span.model,
                                tokens_input=span.tokens_input,
                                tokens_output=span.tokens_output,
                                status=span.status,
                                error=span.error,
                                started_at=span.started_at,
                                ended_at=span.ended_at,
                            )
                        )
                    await session.commit()
                    return trace
            except (DBAPIError, OperationalError, InterfaceError, OSError) as exc:
                last_error = exc
                if attempt == 0 and _is_stale_connection(exc):
                    continue
                raise
        raise last_error  # pragma: no cover

    async def get(self, trace_id: UUID) -> TraceRecord | None:
        async with self._session_factory() as session:
            row = await session.get(TraceModel, trace_id)
            if row is None:
                return None
            return TraceRecord(
                trace_id=row.trace_id,
                execution_id=row.execution_id,
                status=row.status,
                span_count=row.span_count,
                latency_ms=row.latency_ms,
                storage_path=row.storage_path,
                created_at=row.created_at,
            )

    async def find_by_execution_id(self, execution_id: UUID) -> TraceRecord | None:
        async with self._session_factory() as session:
            result = await session.scalars(
                select(TraceModel)
                .where(TraceModel.execution_id == execution_id)
                .order_by(TraceModel.created_at.desc())
                .limit(1)
            )
            row = result.first()
            if row is None:
                return None
            return TraceRecord(
                trace_id=row.trace_id,
                execution_id=row.execution_id,
                status=row.status,
                span_count=row.span_count,
                latency_ms=row.latency_ms,
                storage_path=row.storage_path,
                created_at=row.created_at,
            )

    async def list_spans(self, trace_id: UUID) -> list[SpanRecord]:
        async with self._session_factory() as session:
            result = await session.scalars(
                select(SpanModel).where(SpanModel.trace_id == trace_id)
            )
            return [
                SpanRecord(
                    span_id=row.span_id,
                    trace_id=row.trace_id,
                    parent_span_id=row.parent_span_id,
                    span_type=row.span_type,
                    latency_ms=row.latency_ms,
                    model=row.model,
                    tokens_input=row.tokens_input,
                    tokens_output=row.tokens_output,
                    status=row.status,
                    error=row.error,
                    started_at=row.started_at,
                    ended_at=row.ended_at,
                )
                for row in result.all()
            ]

    async def delete(self, trace_id: UUID) -> None:
        async with self._session_factory() as session:
            row = await session.get(TraceModel, trace_id)
            if row is None:
                raise LookupError(f"Trace not found: {trace_id}")
            await session.delete(row)
            await session.commit()
