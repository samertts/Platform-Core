"""
Platform Health
"""

import platform
import sys


def system_info():

    return {
        "python": sys.version,
        "os": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
