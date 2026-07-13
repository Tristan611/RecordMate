from datetime import datetime

from core.state import State


class StateManager:

    def __init__(self):
        self._current = State.IDLE

    @property
    def current(self) -> State:
        return self._current

    def set(self, state: State):

        if state == self._current:
            return

        self._current = state

        print(
            f"[{datetime.now():%H:%M:%S}] "
            f"STATE -> {state.value}"
        )