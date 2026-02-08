"""Demo simulation and tests for disaster response system

Demonstrates a complete execution of a disaster response agent
responding to environmental events, transitioning FSM states, and 
pursuing goals.
"""

import asyncio
import logging
from disaster_response_agent import DisasterResponseAgent, demo_run
from disaster_environment import Environment


async def traced_execution():
    """Run a detailed execution trace showing agent behavior."""
    print("\n" + "="*60)
    print("DISASTER RESPONSE SYSTEM - GHANA")
    print("Monitoring and responding to emergencies")
    print("="*60 + "\n")

    q = asyncio.Queue()
    env = Environment(seed=99, base_probability=0.6)
    agent = DisasterResponseAgent("Agent-1", q)

    print(f"Agent: {agent.agent_id}")
    print(f"Status: Ready")
    print(f"Monitoring for 4 seconds...\n")

    # Run for 4 seconds with frequent events
    env_task = asyncio.create_task(env.run(q, interval=0.3, duration=4.0))
    agent_task = asyncio.create_task(agent.run(cycles=15, timeout=0.35))

    await asyncio.gather(env_task, agent_task)

    print(f"\n--- Summary ---")
    print(f"Final Status: {agent.fsm.current_state.value}")
    print(f"Total Actions: {len(agent.goals.goals)}")
    
    if agent.goals.goals:
        print(f"\nActions Taken:")
        for i, goal in enumerate(agent.goals.goals, 1):
            print(f"  {i}. {goal.goal_type.value.replace('_', ' ').title()} at {goal.location}")

    print("\n" + "="*60 + "\n")


def test_fsm_transitions():
    """Unit test: FSM state transitions work correctly."""
    from response_fsm import build_disaster_response_fsm, State

    fsm = build_disaster_response_fsm()
    assert fsm.current_state == State.IDLE

    fsm.handle_event("event_detected")
    assert fsm.current_state == State.MONITORING

    fsm.handle_event("assess_damage")
    assert fsm.current_state == State.ASSESSING

    fsm.handle_event("damage_confirmed")
    assert fsm.current_state == State.RESPONDING

    fsm.handle_event("goal_complete")
    assert fsm.current_state == State.RECOVERING

    fsm.handle_event("recovery_done")
    assert fsm.current_state == State.IDLE

    print("✓ FSM transitions test passed")


def test_goal_creation():
    """Unit test: goals are created and tracked."""
    from response_goals import Goal, GoalType, GoalSet, GoalStatus

    gs = GoalSet()
    assert len(gs.goals) == 0

    g1 = Goal(GoalType.ASSESS_DAMAGE, "Sector A", 4)
    gs.add_goal(g1)
    assert len(gs.goals) == 1

    g1.status = GoalStatus.ACTIVE
    active = gs.get_active_goals()
    assert len(active) == 1
    assert active[0].location == "Sector A"

    gs.mark_completed(g1)
    assert g1.status == GoalStatus.COMPLETED
    assert len(gs.get_active_goals()) == 0

    print("✓ Goal creation test passed")


if __name__ == "__main__":
    # Run tests
    print("Running unit tests...")
    test_fsm_transitions()
    test_goal_creation()
    print()

    # Run full execution trace
    asyncio.run(traced_execution())
