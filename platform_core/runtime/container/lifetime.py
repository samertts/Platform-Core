from enum import StrEnum


class Lifetime(StrEnum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"
