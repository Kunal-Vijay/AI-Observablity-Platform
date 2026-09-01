"""Concrete object-storage providers for God's Eye Platform."""

from gods_eye_platform.storage.local_provider import LocalStorageProvider
from gods_eye_platform.storage.supabase_provider import SupabaseStorageProvider

__all__ = ["LocalStorageProvider", "SupabaseStorageProvider"]
