"""Process-wide God's Eye instrumentation configuration."""

from __future__ import annotations

from dataclasses import dataclass, field

from gods_eye.contracts import ModelInfo, PromptReference
from gods_eye.execution_stream import ExecutionEventPublisher


@dataclass(frozen=True, slots=True)
class InstrumentationSettings:
    """Immutable configure-once settings for execution instrumentation."""

    publisher: ExecutionEventPublisher
    model_info: ModelInfo
    prompt_catalog: dict[str, PromptReference] = field(default_factory=dict)


_settings: InstrumentationSettings | None = None


def configure(
    *,
    publisher: ExecutionEventPublisher,
    model_info: ModelInfo,
    prompt_catalog: dict[str, PromptReference] | None = None,
) -> InstrumentationSettings:
    """Configure God's Eye instrumentation once at the application composition root.

    Customer business logic should not call this. The composition root wires the
    execution stream and default model/prompt metadata before handling requests.
    """
    global _settings
    settings = InstrumentationSettings(
        publisher=publisher,
        model_info=model_info,
        prompt_catalog=dict(prompt_catalog or {}),
    )
    _settings = settings
    return settings


def get_settings() -> InstrumentationSettings:
    """Return the active instrumentation settings."""
    if _settings is None:
        raise RuntimeError(
            "God's Eye is not configured. Call gods_eye.configure(...) "
            "once in your application composition root before observing executions."
        )
    return _settings


def reset_configuration() -> None:
    """Clear configure-once settings. Intended for tests only."""
    global _settings
    _settings = None


__all__ = [
    "InstrumentationSettings",
    "configure",
    "get_settings",
    "reset_configuration",
]
