import pytest
from fastapi import HTTPException

from sden.state_machine import State, StateMachine


def test_happy_path():
    sm = StateMachine()
    for expected in [
        State.IDLE,
        State.REQUEST_RECEIVED,
        State.VALIDATED,
        State.PRICED,
        State.INVOICED,
        State.PAID,
    ]:
        sm.advance(expected)
    assert sm.state == State.DELIVERED


def test_out_of_order_raises():
    sm = StateMachine()
    with pytest.raises(HTTPException) as exc_info:
        sm.advance(State.INVOICED)
    assert exc_info.value.status_code == 409


def test_terminal_state_has_no_transition():
    sm = StateMachine()
    sm.terminate()
    assert sm.is_terminal
    with pytest.raises(HTTPException):
        sm.advance(State.TERMINATED)


def test_require_passes_on_correct_state():
    sm = StateMachine()
    sm.require(State.IDLE)  # no exception


def test_require_raises_on_wrong_state():
    sm = StateMachine()
    with pytest.raises(HTTPException) as exc_info:
        sm.require(State.PAID)
    assert exc_info.value.status_code == 409
