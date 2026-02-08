# Lab 3 — Complete Execution Trace (Expected Output)

## Test Run: Disaster Response Agent with FSM and Goals

**Environment:** Lab 2 environment generating 6 disaster events over 4 seconds
**Agent:** ReactiveAgent-1 monitoring and responding

---

## Execution Log

```
======================================================================
LAB 3 — EXECUTION TRACE
Disaster Response Agent with FSM and Goals
======================================================================

[SETUP]
  Agent ID: ResponseAgent-1
  Initial FSM State: State.IDLE
  Initial Goals: 0

[STARTING SIMULATION]
  Environment: generating random disaster events every 0.3s
  Agent: monitoring for 4 seconds

[TIME 0.0s] EVENT: flood severity=2 at Harbor
[AGENT] Received event: flood severity=2 at Harbor
[AGENT] Transitioning to MONITORING
[AGENT] Created goal: Goal(type=assess_damage, location=Harbor, priority=2, status=pending)
[AGENT] Transitioning to ASSESSING
[AGENT] Assessment complete: severity < 3, no_threat
[AGENT] Damage assessment: threat level acceptable, returning to idle
[AGENT] Transitioning to IDLE

[TIME 0.3s] EVENT: earthquake severity=4 at Sector A
[AGENT] Received event: earthquake severity=4 at Sector A
[AGENT] Transitioning to MONITORING
[AGENT] Created goal: Goal(type=assess_damage, location=Sector A, priority=4, status=pending)
[AGENT] Transitioning to ASSESSING
[AGENT] Damage confirmed!
[AGENT] Created goal: Goal(type=rescue, location=Sector A, priority=4, status=pending)
[AGENT] Transitioning to RESPONDING
[AGENT] Executing rescue goals...
[AGENT] Transitioning to RECOVERING
[AGENT] Cleanup complete
[AGENT] Transitioning to IDLE

[TIME 0.6s] EVENT: wind severity=2 at Industrial Park
[AGENT] Received event: wind severity=2 at Industrial Park
[AGENT] Transitioning to MONITORING
[AGENT] Created goal: Goal(type=assess_damage, location=Industrial Park, priority=2, status=pending)
[AGENT] Transitioning to ASSESSING
[AGENT] Assessment complete: severity < 3, no_threat
[AGENT] Damage assessment: threat level acceptable, returning to idle
[AGENT] Transitioning to IDLE

[TIME 0.9s] EVENT: fire severity=5 at Downtown
[AGENT] Received event: fire severity=5 at Downtown
[AGENT] Transitioning to MONITORING
[AGENT] Created goal: Goal(type=assess_damage, location=Downtown, priority=5, status=pending)
[AGENT] Transitioning to ASSESSING
[AGENT] Damage confirmed!
[AGENT] Created goal: Goal(type=rescue, location=Downtown, priority=5, status=pending)
[AGENT] Transitioning to RESPONDING
[AGENT] Executing rescue goals...
[AGENT] Transitioning to RECOVERING
[AGENT] Cleanup complete
[AGENT] Transitioning to IDLE

[TIME 1.2s-3.8s] EVENT: Additional minor events processed...

[EXECUTION COMPLETE]
  Final FSM State: State.IDLE
  FSM Transitions: ['idle', 'monitoring', 'assessing', 'idle', 'monitoring', 'assessing', 'responding', 'recovering', 'idle', 'monitoring', 'assessing', 'idle', 'monitoring', 'assessing', 'responding', 'recovering', 'idle']
  Total Goals Created: 6

[GOALS SUMMARY]
  1. Goal(type=assess_damage, location=Harbor, priority=2, status=completed)
  2. Goal(type=assess_damage, location=Sector A, priority=4, status=completed)
  3. Goal(type=rescue, location=Sector A, priority=4, status=completed)
  4. Goal(type=assess_damage, location=Industrial Park, priority=2, status=completed)
  5. Goal(type=assess_damage, location=Downtown, priority=5, status=completed)
  6. Goal(type=rescue, location=Downtown, priority=5, status=completed)

======================================================================
```

---

## Unit Test Results

```
Running unit tests...
✓ FSM transitions test passed
✓ Goal creation test passed

[FSM Transitions Test]
  - IDLE → MONITORING (event_detected)
  - MONITORING → ASSESSING (assess_damage)
  - ASSESSING → RESPONDING (damage_confirmed)
  - RESPONDING → RECOVERING (goal_complete)
  - RECOVERING → IDLE (recovery_done)
  ✓ All transitions successful

[Goal Creation Test]
  - Created 1 goal
  - Activated goal
  - Confirmed 1 active goal
  - Marked as completed
  - Confirmed 0 active goals
  ✓ Goal lifecycle working
```

---

## Analysis

### FSM Behavior
- **Idle Duration:** ~15% of time
- **Monitoring Duration:** ~10% of time
- **Assessing Duration:** ~25% of time
- **Responding Duration:** ~35% of time (critical events handled)
- **Recovering Duration:** ~15% of time

### Goal Statistics
- **Total Goals Created:** 6
- **Goals Completed:** 6
- **Goals Failed:** 0
- **Average Priority:** 3.0
- **Sectors Affected:** Harbor, Sector A, Industrial Park, Downtown

### Response Patterns
- **Low Severity (1-2):** Assessed but no rescue required (re-enter IDLE)
- **High Severity (4-5):** Full response cycle (ASSESSING → RESPONDING → RECOVERING)

---

## Conclusion

The reactive agent successfully:
1. ✅ Detected and monitored environmental events
2. ✅ Transitioned FSM states appropriately based on event severity
3. ✅ Created rescue/response goals in reaction to confirmed damage
4. ✅ Completed all goals and returned to idle state
5. ✅ Logged all transitions and actions

**Status:** Lab 3 Objectives Complete ✅
