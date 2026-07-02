"""
Platform Exceptions
"""


class PlatformError(Exception):
    """Base Platform Exception."""


class ConfigurationError(PlatformError):
    """Configuration Error."""


class RuntimePlatformError(PlatformError):
    """Runtime Error."""


class ValidationError(PlatformError):
    """Validation Error."""


class FilesystemError(PlatformError):
    """Filesystem Error."""


class SecurityError(PlatformError):
    """Security Error."""
