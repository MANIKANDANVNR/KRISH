from enum import Enum


class SystemState(Enum):

    CREATED = "created"

    INITIALIZING = "initializing"

    READY = "ready"

    RUNNING = "running"

    LOCKED = "locked"

    SHUTDOWN = "shutdown"

    ERROR = "error"