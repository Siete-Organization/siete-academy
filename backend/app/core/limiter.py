"""Shared rate limiter.

Instance lives here (not in main.py) so any router can `from app.core.limiter
import limiter` and decorate an endpoint without circular imports.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=[])
