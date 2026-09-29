from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass(frozen=True)
class Event:
    name: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class EventBus:

    def __init__(self):
        self._handlers: dict[str, list[Callable]] = {}

    def subscribe(
        self,
        event_name: str,
        handler: Callable,
    ):
        self._handlers.setdefault(
            event_name,
            []
        ).append(handler)

    def unsubscribe(
        self,
        event_name: str,
        handler: Callable,
    ):
        handlers = self._handlers.get(event_name, [])

        if handler in handlers:
            handlers.remove(handler)

    def publish(self, event: Event):

        for handler in tuple(
            self._handlers.get(event.name, [])
        ):
            handler(event)