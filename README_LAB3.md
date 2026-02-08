# Lab 3 — Goals, Events, and Reactive Behavior

## Objective
Model agent goals and event-triggered behavior using FSMs and goal management.

## Deliverables ✅

### 1. FSM Diagram
See [LAB3_FSM_DIAGRAM.md](LAB3_FSM_DIAGRAM.md) for the state machine diagram and state descriptions.

**States:**
- **IDLE** → waiting for events
- **MONITORING** → sensor detected anomaly
- **ASSESSING** → evaluating damage severity
- **RESPONDING** → executing rescue/containment goals
- **RECOVERING** → post-incident cleanup

**Transitions:** Triggered by events like `event_detected`, `damage_confirmed`, `goal_complete`, etc.

### 2. Python Implementation

#### Modules:
- **response_goals.py** — Goal definitions, GoalType, GoalStatus, GoalSet for tracking
- **response_fsm.py** — FSM engine with states, transitions, and callbacks
- **disaster_response_agent.py** — DisasterResponseAgent that combines FSM + goals + sensor input

#### Key Classes:
- `Goal` — individual goal with type, location, priority, status
- `GoalSet` — collection manager for goals
- `FSM` — finite state machine with transitions and callbacks
- `DisasterResponseAgent` — agent that reacts to env events, transitions FSM, pursues goals

### 3. Execution Trace

Run the **execution trace** with:
```bash
python3 demo_simulation.py
```

Expected output:
- Unit test results (FSM transitions, goal creation)
- Full simulation run showing:
  - FSM state transitions (IDLE → MONITORING → ASSESSING → RESPONDING → RECOVERING → IDLE)
  - Goals created in response to detected events
  - Agent behavior summary and goal status

## Quick Start

### Run the full demo (environment + agent + FSM):
```bash
python3 disaster_response_agent.py
```

### Run the execution trace (with tests):
```bash
python3 demo_simulation.py
```

### Run individual components:
```bash
python3 response_fsm.py        # FSM state transitions demo
python3 response_goals.py       # Goal creation demo
```

## Integration with Earlier Labs

- **Environment** → generates disaster events
- **Sensor** → detects and logs events to queue
- **DisasterResponseAgent** → consumes events and reacts via FSM + goal pursuit

```
Environment → Queue → SensorAgent (log) → Queue → DisasterResponseAgent (FSM+Goals)
```

## Example Execution Flow

1. **Event generated:** earthquake severity=4 at Sector A
2. **IDLE** → `event_detected` → **MONITORING**
3. **MONITORING** → `assess_damage` → **ASSESSING**
4. **ASSESSING:** severity ≥ 3 → `damage_confirmed` → **RESPONDING**
5. **RESPONDING:** execute rescue goals → `goal_complete` → **RECOVERING**
6. **RECOVERING:** → `recovery_done` → **IDLE**

Each transition logs state changes and creates/updates goals accordingly.

## Testing

Run unit tests:
```bash
pytest -q tests/ 
# or
python3 lab3_execution_trace.py
```
