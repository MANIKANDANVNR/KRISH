from core.state import SystemState


class Lifecycle:

    ALLOWED = {
        SystemState.CREATED: {
            SystemState.INITIALIZING
        },

        SystemState.INITIALIZING: {
            SystemState.READY,
            SystemState.ERROR
        },

        SystemState.READY: {
            SystemState.RUNNING,
            SystemState.LOCKED,
            SystemState.SHUTDOWN
        },

        SystemState.RUNNING: {
            SystemState.READY,
            SystemState.LOCKED,
            SystemState.ERROR
        },

        SystemState.LOCKED: {
            SystemState.READY,
            SystemState.SHUTDOWN
        },

        SystemState.ERROR: {
            SystemState.INITIALIZING,
            SystemState.SHUTDOWN
        },

        SystemState.SHUTDOWN: set(),
    }

    def __init__(self):
        self.state = SystemState.CREATED

    def transition(self, new_state):

        if new_state not in self.ALLOWED[self.state]:
            raise RuntimeError(
                f"Invalid transition: "
                f"{self.state.value} -> "
                f"{new_state.value}"
            )

        self.state = new_state