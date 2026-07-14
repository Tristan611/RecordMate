from datetime import datetime

from core.events import Events
from core.state import State


class StateManager:

    def __init__(self, events=None):
        self._current = State.IDLE
        self.events = events

    @property
    def current(self) -> State:
        return self._current

    def set(self, state: State) -> None:
        if state == self._current:
            return

        self._current = state

        print(
            f"[{datetime.now():%H:%M:%S}] "
            f"STATE -> {state.value}"
        )

        if self.events:
            self.events.emit(
                Events.STATE_CHANGED,
                state,
            )