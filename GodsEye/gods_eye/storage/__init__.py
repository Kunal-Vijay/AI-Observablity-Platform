"""Compatibility export for the storage interface.

New code should import :class:`StorageProvider` from :mod:`gods_eye.ports`.
Concrete providers live under :mod:`gods_eye_platform.storage`.
"""

from gods_eye.ports.storage import StorageProvider

__all__ = ["StorageProvider"]
