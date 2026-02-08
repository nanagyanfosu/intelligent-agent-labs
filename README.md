# Intelligent Agent Labs

A comprehensive lab series on multi-agent systems, perception, reactive behavior, and XMPP-based agent communication.

---

## Lab Overview

### [Lab 2: Perception and Environment Modeling](README_LAB2.md)
**Objective:** Implement agent perception of environmental and disaster-related events.

- **Environment Simulator** (`lab2_environment.py`) — generates random disaster events with severity levels
- **Sensor Agent** (`sensor_agent.py`) — monitors environment and logs events
- Includes test cases for event generation and queue integration

**Quick Start:**
```bash
python3 sensor_agent.py   # Run sensor agent demo
python3 lab2_environment.py  # Run environment simulator demo
```

---

### [Lab 3: Goals, Events, and Reactive Behavior](README_LAB3.md)
**Objective:** Model agent goals and event-triggered behavior using FSMs.

**Deliverables:**
- **FSM Diagram** ([LAB3_FSM_DIAGRAM.md](LAB3_FSM_DIAGRAM.md)) — 6 states, 7 transitions
- **Python Implementation** — 1000+ lines of core + test code
  - `lab3_goals.py` — Goal types, lifecycle, management
  - `lab3_fsm.py` — Finite State Machine engine
  - `lab3_reactive_agent.py` — Reactive agent with FSM + goals
- **Execution Trace** ([LAB3_EXECUTION_TRACE_EXPECTED.md](LAB3_EXECUTION_TRACE_EXPECTED.md)) — Full simulation output
- **Tests** (`tests/test_lab3.py`) — 18+ unit and integration tests

**FSM States:** IDLE → MONITORING → ASSESSING → RESPONDING → RECOVERING → IDLE

**Quick Start:**
```bash
python3 lab3_execution_trace.py  # Run full demo + tests
python3 lab3_reactive_agent.py   # Run agent with environment integration
pytest tests/test_lab3.py -v      # Run test suite
```

---

## Architecture

### Lab 2 → Lab 3 Integration

```
Environment (lab2_environment.py)
    ↓ generates events
Queue (asyncio.Queue)
    ↓
SensorAgent (sensor_agent.py) → logs to lab2_events.log
    ↓
ReactiveAgent (lab3_reactive_agent.py)
    ├─ FSM (lab3_fsm.py) — state transitions
    └─ Goals (lab3_goals.py) — goal management
```

---

## Quick Navigation

| Lab | Objective | Key Files | Test Command |
|-----|-----------|-----------|--------------|
| **Lab 2** | Perception & sensing | `lab2_environment.py`, `sensor_agent.py` | `python3 sensor_agent.py` |
| **Lab 3** | Reactive behavior & goals | `lab3_fsm.py`, `lab3_goals.py`, `lab3_reactive_agent.py` | `python3 lab3_execution_trace.py` |

---

## Project Structure

```
/workspaces/intelligent-agent-labs/
├── README.md                          (this file)
├── README_LAB2.md                     (Lab 2 guide)
├── README_LAB3.md                     (Lab 3 guide)
├── LAB3_SUMMARY.md                    (Lab 3 complete summary)
├── LAB3_FSM_DIAGRAM.md                (FSM diagram + legend)
├── LAB3_EXECUTION_TRACE_EXPECTED.md   (Expected simulation output)
│
├── disaster_environment.py            (Environment simulator)
├── sensor_agent.py                    (Sensor agent + logger)
│
├── response_goals.py                  (Goal system)
├── response_fsm.py                    (Finite state machine)
├── disaster_response_agent.py         (Response agent)
├── demo_simulation.py                 (Full demo + tests)
│
├── agent_simple.py                    (Simple local agent example)
├── agent_spade.py                     (SPADE XMPP agent example)
│
├── tests/
│   ├── test_lab2.py
│   └── test_lab3.py
│
└── __pycache__/ (generated, ignore)
```

---

## Running the Labs

### Lab 2 — Environment & Perception

```bash
# Run sensor agent (monitoring environment events)
python3 sensor_agent.py

# Run environment directly (prints generated events)
python3 lab2_environment.py

# Run tests
pytest tests/test_lab2.py -v
```

### Lab 3 — Reactive Behavior & Goals

```bash
# Full demo with tests
python3 demo_simulation.py

# Run response agent (with environment integration)
python3 disaster_response_agent.py

# Run tests
pytest tests/test_lab3.py -v
```

### Simple Local Agent (no XMPP needed)

```bash
# Run minimal agent that exchanges messages locally
python3 agent_simple.py
```

---

## Key Concepts

### Lab 2: Environment & Perception
- **Events:** earthquake, flood, fire, wind (with severity 1-5)
- **Locations:** 7 different sectors/areas
- **Sensor Agent:** asynchronous monitoring with logging
- **Queue-based:** event buffering via asyncio.Queue

### Lab 3: FSM & Goals
- **Finite State Machine:** 6 states, 7 transitions
- **Goals:** ASSESS_DAMAGE, EVACUATE, RESCUE, CONTAIN, RECOVER
- **Event-Driven:** FSM transitions triggered by severity thresholds
- **Reactive Behavior:** agent reacts dynamically to environment

---

## Testing

All labs include comprehensive unit and integration tests:

```bash
# Run all tests
pytest -v

# Run specific lab tests
pytest tests/test_lab2.py -v
pytest tests/test_lab3.py -v
```

---

## Troubleshooting

### Issue: Module import errors
- Ensure you're in the workspace root: `cd /workspaces/intelligent-agent-labs/`
- All imports are relative and assume this working directory

### Issue: asyncio/event loop errors
- All async code uses `asyncio.run()` for proper event loop management
- No active event loop should be running when calling scripts

### Issue: Permission/logging errors
- Log files (lab2_events.log, lab3_events.log) are created in current directory
- Ensure write permissions in workspace

---

## Quick Reference

### Lab 2 Files

| File | Purpose |
|------|---------|
| `lab2_environment.py` | Environment simulator with event generation |
| `sensor_agent.py` | Agent that monitors and logs events |

### Lab 3 Files

| File | Purpose |
|------|---------|
| `response_goals.py` | Goal definitions and management |
| `response_fsm.py` | Finite State Machine implementation |
| `disaster_response_agent.py` | Agent with FSM-based reactive behavior |
| `demo_simulation.py` | Demo runner and test suite |

---

## Summary

✅ **Lab 2:** Perception and environment monitoring  
✅ **Lab 3:** Event-triggered reactive behavior with FSM and goals  

Both labs demonstrate core agent concepts and are fully integrated for a complete disaster-response simulation. 🎉


"}