"""
Platform Health
"""

from __future__ import annotations

import platform
import sys
from typing import Any


def system_info() -> dict[str, Any]:
    return {
        "python": sys.version,
        "os": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
