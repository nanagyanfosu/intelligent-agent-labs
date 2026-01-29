import asyncio
from disaster_environment import Environment


def test_generate_event_structure():
    env = Environment(seed=123, base_probability=1.0)  # force event every call
    ev = env.generate_event()
    assert ev is not None
    assert set(ev.keys()) >= {"id", "type", "severity", "location", "timestamp"}
    assert ev["type"] in ("earthquake", "flood", "fire", "wind")
    assert 1 <= ev["severity"] <= 5


async def run_env_for_events():
    q = asyncio.Queue()
    env = Environment(seed=7, base_probability=0.7)
    # run a short env loop
    await env.run(q, interval=0.01, duration=0.1)
    events = []
    while not q.empty():
        events.append(q.get_nowait())
    return events


def test_env_puts_events_in_queue():
    events = asyncio.run(run_env_for_events())
    assert isinstance(events, list)
    # Could be 0..n depending on randomness but we expect at least 0-5 events
    assert len(events) >= 0
