# God's Eye

Main documentation moved to the repo root: [`README.md`](../README.md).

God's Eye is an AI observability platform with four independent products:
the language-neutral Execution Protocol, the Python SDK, the optional Platform,
and customer runtimes.

## Install

```bash
# Core SDK (Pydantic only)
uv add gods_eye

# Optional Platform backend (API + persistence + storage)
uv add "gods_eye[platform]"

# This repository / reference runtime
uv sync --extra reference --extra dev
```

## Minimal instrumentation

```python
from gods_eye import Contracts, configure, execution, span
from gods_eye.execution_stream import InMemoryExecutionStream

configure(
    publisher=InMemoryExecutionStream(),
    model_info=Contracts.ModelInfo(provider="acme", model_name="demo"),
)

@span("my_stage")
async def run_stage(query: str) -> dict[str, str]:
    return {"answer": "ok"}

@execution("query")
async def main(query: str) -> dict[str, str]:
    return await run_stage(query)
```

Customer code writes business logic and annotates boundaries. The SDK owns
execution lifecycle, tracing, event publication, and stage inference.

Use the optional Platform to project those facts into persistence:

```python
from gods_eye_platform.event_subscribers import register_persistence_subscribers
from gods_eye_platform.execution_store import TracePersister
from gods_eye_platform.persistence.postgres import (
    PostgresExecutionSnapshotRepository,
)
```

The SDK never imports `gods_eye_platform`, FastAPI, SQLAlchemy, Supabase, or
the reference runtime.

## Public API

Frozen exports from `gods_eye`:

- `GodsEye`
- `configure`
- `execution`
- `span`
- `ExecutionStream`
- `Contracts`
- `Plugin`
- ambient correlation getters

See [docs/public-api.md](docs/public-api.md), [docs/architecture.md](docs/architecture.md),
and [protocol/README.md](protocol/README.md).

Replay, evaluation, analytics, and dashboard namespaces are reserved under
`gods_eye_platform`; no engines or dashboard are implemented yet.

## Reference runtime

`examples/reference_runtime` is a demo customer application. It consumes the
SDK and opts into Platform persistence/API packages. It is **not** part of the
installable wheel.

```bash
cp .env.example .env
uv sync --extra reference --extra dev
uv run alembic upgrade head
uv run uvicorn examples.reference_runtime.main:app --reload
```

Seed sample documents (server must be running):

```bash
uv run python examples/reference_runtime/scripts/seed_sample_documents.py
```

Deprecated compatibility launcher (one release):

```bash
uv run uvicorn app.main:app --reload
```

Canonical command:

```bash
uv run uvicorn examples.reference_runtime.main:app --reload
```

## Migrations

- Reference deployment (this repo): `alembic.ini` →
  `examples/reference_runtime/db/migrations` (registers demo document models;
  uses the shared Platform revision chain).
- Platform-only installs: point Alembic at
  `gods_eye_platform/persistence/postgres/migrations`.

Do not rewrite applied revision history. Stamp/upgrade paths are documented in
[docs/architecture.md](docs/architecture.md).

## Development checks

```bash
uv run ruff check .
uv run mypy
uv run pytest
uv run alembic upgrade head
uv run alembic check
```
