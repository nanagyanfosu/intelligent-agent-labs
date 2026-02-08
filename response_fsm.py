"""Finite State Machine for disaster response agent behavior

FSM states:
  IDLE -> (event detected) -> MONITORING
  MONITORING -> (assess_damage goal) -> ASSESSING
  ASSESSING -> (damage confirmed) -> RESPONDING or (no threat) -> IDLE
  RESPONDING -> (goal complete) -> RECOVERING
  RECOVERING -> IDLE
"""

from enum import Enum
from typing import Callable, Optional, Dict, Any


class State(Enum):
    """FSM state space."""
    IDLE = "idle"
    MONITORING = "monitoring"
    ASSESSING = "assessing"
    RESPONDING = "responding"
    RECOVERING = "recovering"


class FSM:
    """Simple Finite State Machine for agent behavior."""

    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.history = [initial_state]
        self.transitions: Dict[State, Dict[str, State]] = {}
        self.on_enter_callbacks: Dict[State, Callable] = {}
        self.on_exit_callbacks: Dict[State, Callable] = {}

    def add_transition(self, from_state: State, event: str, to_state: State) -> None:
        """Define a transition (from_state --[event]--> to_state)."""
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state

    def on_enter(self, state: State, callback: Callable) -> None:
        """Register a callback to fire when entering a state."""
        self.on_enter_callbacks[state] = callback

    def on_exit(self, state: State, callback: Callable) -> None:
        """Register a callback to fire when exiting a state."""
        self.on_exit_callbacks[state] = callback

    def handle_event(self, event: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Process an event; transition if possible. Return True if transition occurred."""
        context = context or {}
        if self.current_state not in self.transitions:
            return False
        if event not in self.transitions[self.current_state]:
            return False

        next_state = self.transitions[self.current_state][event]

        # Call exit callback
        if self.current_state in self.on_exit_callbacks:
            self.on_exit_callbacks[self.current_state](context)

        # Transition
        self.current_state = next_state
        self.history.append(next_state)

        # Call enter callback
        if next_state in self.on_enter_callbacks:
            self.on_enter_callbacks[next_state](context)

        return True

    def is_in_state(self, state: State) -> bool:
        """Check if FSM is in a specific state."""
        return self.current_state == state


def build_disaster_response_fsm() -> FSM:
    """Build and return a configured FSM for disaster response."""
    fsm = FSM(State.IDLE)

    # Define transitions
    fsm.add_transition(State.IDLE, "event_detected", State.MONITORING)
    fsm.add_transition(State.MONITORING, "assess_damage", State.ASSESSING)
    fsm.add_transition(State.ASSESSING, "damage_confirmed", State.RESPONDING)
    fsm.add_transition(State.ASSESSING, "no_threat", State.IDLE)
    fsm.add_transition(State.RESPONDING, "goal_complete", State.RECOVERING)
    fsm.add_transition(State.RECOVERING, "recovery_done", State.IDLE)

    return fsm


if __name__ == "__main__":
    # demo
    fsm = build_disaster_response_fsm()
    print(f"Initial state: {fsm.current_state}")

    fsm.handle_event("event_detected")
    print(f"After event_detected: {fsm.current_state}")

    fsm.handle_event("assess_damage")
    print(f"After assess_damage: {fsm.current_state}")

    fsm.handle_event("damage_confirmed")
    print(f"After damage_confirmed: {fsm.current_state}")

    fsm.handle_event("goal_complete")
    print(f"After goal_complete: {fsm.current_state}")

    fsm.handle_event("recovery_done")
    print(f"After recovery_done: {fsm.current_state}")

    print(f"\nFSM history: {fsm.history}")
