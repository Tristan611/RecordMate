from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventManager:

    def __init__(self):
        self._subscribers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        callback: Callable[..., Any],
    ) -> None:
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)

    def unsubscribe(
        self,
        event_name: str,
        callback: Callable[..., Any],
    ) -> None:
        callbacks = self._subscribers.get(event_name, [])

        if callback in callbacks:
            callbacks.remove(callback)

    def emit(
        self,
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        for callback in list(self._subscribers.get(event_name, [])):
            callback(*args, **kwargs)