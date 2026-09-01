"""Document models share the God's Eye SQLAlchemy Base for one DB upgrade path."""

from gods_eye_platform.persistence.postgres.base import Base

__all__ = ["Base"]
