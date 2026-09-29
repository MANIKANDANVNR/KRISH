from core.configuration import Configuration
from core.events import Event, EventBus
from core.lifecycle import Lifecycle
from core.service_registry import ServiceRegistry
from core.state import SystemState


class Runtime:

    def __init__(self, config=None):

        self.config = config or Configuration()

        self.lifecycle = Lifecycle()

        self.events = EventBus()

        self.services = ServiceRegistry()

        # =====================================================
        # SECURITY / CAPABILITY STATE
        # =====================================================
        #
        # These are runtime capability requests/states.
        # They are NOT authorization by themselves.
        #
        # The security layer remains responsible for deciding
        # whether a capability can actually be used.
        #

        self._capabilities = {
            "internet": False,
            "web_search": False,
            "external_data": False,

            "file_access": False,

            "system_access": False,
            "application_launch": False,
            "python_terminal": False,

            "voice_input": False,
            "voice_output": False,

            "automatic_evolution": False,
        }

    # =========================================================
    # LIFECYCLE
    # =========================================================

    def initialize(self):

        self.lifecycle.transition(
            SystemState.INITIALIZING
        )

        self.events.publish(
            Event("runtime.initializing")
        )

        # Deny by default on every initialization.
        self._reset_capabilities()

        self.lifecycle.transition(
            SystemState.READY
        )

        self.events.publish(
            Event("runtime.ready")
        )

    def start(self):

        if self.lifecycle.state != SystemState.READY:
            raise RuntimeError(
                "Runtime is not ready."
            )

        self.lifecycle.transition(
            SystemState.RUNNING
        )

        self.events.publish(
            Event("runtime.started")
        )

    def lock(self):

        if self.lifecycle.state in (
            SystemState.READY,
            SystemState.RUNNING,
        ):

            self._reset_capabilities()

            self.lifecycle.transition(
                SystemState.LOCKED
            )

            self.events.publish(
                Event("runtime.locked")
            )

    def shutdown(self):

        if self.lifecycle.state == SystemState.SHUTDOWN:
            return

        self._reset_capabilities()

        self.lifecycle.transition(
            SystemState.SHUTDOWN
        )

        self.events.publish(
            Event("runtime.shutdown")
        )

    # =========================================================
    # CAPABILITIES
    # =========================================================

    @property
    def capabilities(self):

        return dict(
            self._capabilities
        )

    def capability_enabled(self, name):

        if name not in self._capabilities:
            raise KeyError(
                f"Unknown capability: {name}"
            )

        return self._capabilities[name]

    def request_capability(self, name, enabled=True):

        if name not in self._capabilities:
            raise KeyError(
                f"Unknown capability: {name}"
            )

        enabled = bool(enabled)

        # Automatic evolution has a hard architectural
        # restriction. Runtime cannot turn it on merely
        # because a UI toggle or LLM requests it.
        if name == "automatic_evolution" and enabled:
            raise PermissionError(
                "Automatic evolution requires explicit "
                "owner authorization."
            )

        self._capabilities[name] = enabled

        self.events.publish(
            Event(
                "runtime.capability_changed",
                {
                    "capability": name,
                    "enabled": enabled,
                },
            )
        )

        return enabled

    def disable_capability(self, name):

        return self.request_capability(
            name,
            False,
        )

    def _reset_capabilities(self):

        for name in self._capabilities:
            self._capabilities[name] = False

    # =========================================================
    # SECURITY SAFE HELPERS
    # =========================================================

    def capability_snapshot(self):

        return {
            name: bool(enabled)
            for name, enabled
            in self._capabilities.items()
        }

    def is_operational(self):

        return self.lifecycle.state in (
            SystemState.READY,
            SystemState.RUNNING,
        )

    def is_locked(self):

        return (
            self.lifecycle.state
            == SystemState.LOCKED
        )