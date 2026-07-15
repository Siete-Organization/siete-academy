"""Shared rate limiter.

Instance lives here (not in main.py) so any router can `from app.core.limiter
import limiter` and decorate an endpoint without circular imports.

Storage: Redis en producción para que los N workers de gunicorn compartan UN
contador (in-memory da un contador POR worker: con 3 workers el límite real
era 3x y errático). En dev/tests no hay Redis corriendo -> memoria.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings

_settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri=_settings.redis_url if _settings.app_env == "production" else "memory://",
)
