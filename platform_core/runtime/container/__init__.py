"""
Platform-Core Service Container
"""

from .container import ServiceContainer
from .lifetime import Lifetime

__all__ = [
    "ServiceContainer",
    "Lifetime",
]
