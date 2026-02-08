import asyncio
import logging
from response_fsm import FSM, State, build_disaster_response_fsm
from response_goals import Goal, GoalType, GoalSet, GoalStatus


def setup_logger(logfile: str = "response_events.log") -> logging.Logger:
    """Setup logger for response agent."""
    logger = logging.getLogger("response_agent")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(logfile)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        # Also add console
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger


class DisasterResponseAgent:
    def __init__(self, agent_id: str, queue: asyncio.Queue, logger: logging.Logger = None):
        self.agent_id = agent_id
        self.queue = queue
        self.logger = logger or setup_logger("response_events")
        self.fsm = build_disaster_response_fsm()
        self.goals = GoalSet()
        self.running = False

    def _on_idle_enter(self, context):
        self.logger.info(f"[{self.agent_id}] Waiting for alerts")

    def _on_monitoring_enter(self, context):
        self.logger.info(f"[{self.agent_id}] Alert detected - checking details")

    def _on_assessing_enter(self, context):
        self.logger.info(f"[{self.agent_id}] Assessing the situation")

    def _on_responding_enter(self, context):
        self.logger.info(f"[{self.agent_id}] Sending response team")

    def _on_recovering_enter(self, context):
        self.logger.info(f"[{self.agent_id}] Recovery in progress")

    def setup_fsm_callbacks(self):
        """Register FSM state callbacks."""
        self.fsm.on_enter(State.IDLE, self._on_idle_enter)
        self.fsm.on_enter(State.MONITORING, self._on_monitoring_enter)
        self.fsm.on_enter(State.ASSESSING, self._on_assessing_enter)
        self.fsm.on_enter(State.RESPONDING, self._on_responding_enter)
        self.fsm.on_enter(State.RECOVERING, self._on_recovering_enter)

    async def process_event(self, event_data: dict) -> None:
        """React to an environmental event."""
        ev_type = event_data["type"]
        severity = event_data["severity"]
        location = event_data["location"]
        ev_id = event_data["id"]

        self.logger.info(f"[{self.agent_id}] Alert: {ev_type} at {location} (level {severity})")

        
        if self.fsm.is_in_state(State.IDLE):
            self.fsm.handle_event("event_detected", {"event": event_data})

        # Create assessment goal
        if self.fsm.is_in_state(State.MONITORING):
            goal = Goal(
                goal_type=GoalType.ASSESS_DAMAGE,
                location=location,
                priority=severity,
                event_id=ev_id
            )
            self.goals.add_goal(goal)
            self.logger.info(f"[{self.agent_id}] Plan: Assess damage at {goal.location}")
            self.fsm.handle_event("assess_damage", {"goal": goal})

        # Simulate assessment; if severity >= 3, confirm damage
        if self.fsm.is_in_state(State.ASSESSING):
            await asyncio.sleep(0.1)  # quick simulation of assessment
            if severity >= 3:
                self.fsm.handle_event("damage_confirmed", {})
                # Create response goal
                response_goal = Goal(
                    goal_type=GoalType.RESCUE,
                    location=location,
                    priority=severity,
                    event_id=ev_id
                )
                self.goals.add_goal(response_goal)
                self.logger.info(f"[{self.agent_id}] Damage confirmed - sending rescue to {location}")
            else:
                self.fsm.handle_event("no_threat", {})
                self.logger.info(f"[{self.agent_id}] Situation safe - no major action needed")

        # Execute response
        if self.fsm.is_in_state(State.RESPONDING):
            await asyncio.sleep(0.1)  # simulate response time
            self.fsm.handle_event("goal_complete", {})

        # Recover
        if self.fsm.is_in_state(State.RECOVERING):
            await asyncio.sleep(0.05)
            self.fsm.handle_event("recovery_done", {})

    async def run(self, cycles: int = 20, timeout: float = 0.5) -> None:
        """Run the agent for a number of cycles."""
        self.setup_fsm_callbacks()
        self.running = True
        self.logger.info(f"[{self.agent_id}] System online - monitoring...")

        for _ in range(cycles):
            try:
                event_data = await asyncio.wait_for(self.queue.get(), timeout)
                await self.process_event(event_data)
            except asyncio.TimeoutError:
                pass

        self.running = False
        self.logger.info(f"[{self.agent_id}] Monitoring complete")


async def demo_run(duration: float = 3.0):
    """Demo: Environment -> Sensor -> DisasterResponseAgent with FSM."""
    from disaster_environment import Environment

    q = asyncio.Queue()
    env = Environment(seed=42, base_probability=0.5)
    agent = DisasterResponseAgent("ResponseAgent-1", q)

    env_task = asyncio.create_task(env.run(q, interval=0.3, duration=duration))
    agent_task = asyncio.create_task(agent.run(cycles=int(duration / 0.3) + 3, timeout=0.35))

    await asyncio.gather(env_task, agent_task)


if __name__ == "__main__":
    asyncio.run(demo_run())
