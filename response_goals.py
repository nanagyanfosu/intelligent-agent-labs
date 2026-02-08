"""Response goals for disaster management

Agents pursue goals in response to environmental events.
This module defines goal types and lifecycle.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class GoalStatus(Enum):
    """Goal lifecycle states."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class GoalType(Enum):
    """Goal categories for rescue/response."""
    ASSESS_DAMAGE = "assess_damage"
    EVACUATE = "evacuate"
    RESCUE = "rescue"
    CONTAIN = "contain"
    RECOVER = "recover"


@dataclass
class Goal:
    """A single goal instance."""
    goal_type: GoalType
    location: str
    priority: int  # 1 (low) to 5 (critical)
    status: GoalStatus = GoalStatus.PENDING
    event_id: Optional[str] = None  # triggering event id

    def __str__(self) -> str:
        return f"Goal(type={self.goal_type.value}, location={self.location}, priority={self.priority}, status={self.status.value})"


class GoalSet:
    """Manager for active goals."""
    def __init__(self):
        self.goals = []

    def add_goal(self, goal: Goal) -> None:
        """Register a new goal."""
        self.goals.append(goal)

    def get_active_goals(self) -> list:
        """Return all ACTIVE goals, sorted by priority (descending)."""
        active = [g for g in self.goals if g.status == GoalStatus.ACTIVE]
        return sorted(active, key=lambda g: g.priority, reverse=True)

    def mark_completed(self, goal: Goal) -> None:
        """Mark a goal as completed."""
        if goal in self.goals:
            goal.status = GoalStatus.COMPLETED

    def mark_failed(self, goal: Goal) -> None:
        """Mark a goal as failed."""
        if goal in self.goals:
            goal.status = GoalStatus.FAILED


if __name__ == "__main__":
    # demo
    gs = GoalSet()
    g1 = Goal(GoalType.ASSESS_DAMAGE, "Sector A", 4, event_id="evt1")
    gs.add_goal(g1)
    g1.status = GoalStatus.ACTIVE
    print(g1)
    print(f"Active goals: {gs.get_active_goals()}")
