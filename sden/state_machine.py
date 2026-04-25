from enum import Enum

from fastapi import HTTPException


class State(str, Enum):
    IDLE = "IDLE"
    REQUEST_RECEIVED = "REQUEST_RECEIVED"
    VALIDATED = "VALIDATED"
    PRICED = "PRICED"
    INVOICED = "INVOICED"
    PAID = "PAID"
    DELIVERED = "DELIVERED"
    TERMINATED = "TERMINATED"


# Each state maps to the single state that may legally follow it.
# TERMINATED and DELIVERED are terminal — no outgoing transitions.
_TRANSITIONS: dict[State, State] = {
    State.IDLE: State.REQUEST_RECEIVED,
    State.REQUEST_RECEIVED: State.VALIDATED,
    State.VALIDATED: State.PRICED,
    State.PRICED: State.INVOICED,
    State.INVOICED: State.PAID,
    State.PAID: State.DELIVERED,
}

_TERMINAL = {State.DELIVERED, State.TERMINATED}


class StateMachine:
    def __init__(self) -> None:
        self.state = State.IDLE

    def advance(self, expected_current: State) -> None:
        """Advance to the next state.

        Raises HTTPException(409) if the current state doesn't match
        expected_current, or if there is no valid next state.
        """
        if self.state != expected_current:
            raise HTTPException(
                status_code=409,
                detail=f"Expected state {expected_current}, currently {self.state}",
            )
        next_state = _TRANSITIONS.get(self.state)
        if next_state is None:
            raise HTTPException(
                status_code=409,
                detail=f"State {self.state} has no valid transition",
            )
        self.state = next_state

    def terminate(self) -> None:
        self.state = State.TERMINATED

    def require(self, required: State) -> None:
        """Assert the machine is in a specific state, raise 409 if not."""
        if self.state != required:
            raise HTTPException(
                status_code=409,
                detail=f"Required state {required}, currently {self.state}",
            )

    @property
    def is_terminal(self) -> bool:
        return self.state in _TERMINAL
