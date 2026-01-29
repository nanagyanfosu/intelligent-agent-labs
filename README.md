# Lab 2 — Perception and Environment Modeling

Objective: Implement agent perception of environmental and disaster-related events.

Quick start
-----------
1. Run the demo sensor that uses the embedded Environment simulator:

```bash
python3 sensor_agent.py
```

2. Or run the environment directly (prints generated events):

```bash
python3 disaster_environment.py
```

What's included
----------------
- `disaster_environment.py`: Environment simulator that generates random disaster events.
- `sensor_agent.py`: SensorAgent that consumes events and logs them to `disaster_events.log` and console.
- `agent_simple.py`: very small local agent example (for quick message tests).

Design notes
------------
- The environment generates randomized events with types, severities (1-5), and locations.
- The SensorAgent polls for events asynchronously and logs them; it is lightweight and suitable for unit testing.

Testing
-------
A simple test file is included. Run tests with pytest (if installed):

```bash
pytest -q
```

"}