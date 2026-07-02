from enum import Enum


class KernelState(str, Enum):

    CREATED = "created"

    INITIALIZED = "initialized"

    STARTING = "starting"

    RUNNING = "running"

    STOPPING = "stopping"

    STOPPED = "stopped"

    FAILED = "failed"
