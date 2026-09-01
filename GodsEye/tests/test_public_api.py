from __future__ import annotations

import gods_eye
from gods_eye import (
    Contracts,
    ExecutionStream,
    GodsEye,
    Plugin,
    configure,
    execution,
    get_current_execution_id,
    get_current_execution_latency_ms,
    get_current_trace_id,
    span,
)
from gods_eye.tracing import observe, trace_span


def test_public_exports_are_importable() -> None:
    assert configure is gods_eye.configure
    assert execution is gods_eye.execution
    assert span is gods_eye.span
    assert GodsEye is gods_eye.GodsEye
    assert Contracts is gods_eye.Contracts
    assert ExecutionStream is gods_eye.ExecutionStream
    assert Plugin is gods_eye.Plugin
    assert get_current_execution_id is gods_eye.get_current_execution_id
    assert get_current_trace_id is gods_eye.get_current_trace_id
    assert (
        get_current_execution_latency_ms
        is gods_eye.get_current_execution_latency_ms
    )


def test_frozen_surface_hides_lifecycle_management() -> None:
    assert "ExecutionContext" not in gods_eye.__all__
    assert "ObservedResult" not in gods_eye.__all__
    assert "record_metadata" not in gods_eye.__all__
    assert "ExecutionRepository" not in gods_eye.__all__
    assert "TraceRepository" not in gods_eye.__all__


def test_observe_is_trace_span_alias() -> None:
    assert observe is trace_span


def test_adapters_are_not_top_level_exports() -> None:
    assert not hasattr(gods_eye, "PostgresTraceRepository")
    assert not hasattr(gods_eye, "SupabaseStorageProvider")
    assert not hasattr(gods_eye, "LocalStorageProvider")
