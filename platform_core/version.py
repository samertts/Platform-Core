"""
Platform-Core Version Information
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    stage: str = "alpha"

    @property
    def string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}-{self.stage}"


VERSION = Version(
    major=0,
    minor=1,
    patch=0,
    stage="alpha",
)
