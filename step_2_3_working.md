# Step 2.3 Working – Runtime Scheduling & Simulation

## Items

- [x] 12) Review the three‑clock definitions and their interactions; ensure no ambiguity about which clock drives which events.
- [X] 13) Validate the TriggerEngine rule example (global_step heartbeat) and test edge cases (conflicts, ordering).
    - no major issues with current design
- [X] 14) Assess whether the simple round‑robin turn management will scale with many System 1 agents.


## Item 12

### ClockPort (draft)

```python
# Required imports for the protocol definition
from __future__ import annotations
from typing import Protocol, Callable
from datetime import datetime
# Assuming an Event class exists elsewhere in the codebase
from core.event import Event  # adjust import path if needed

class ClockPort(Protocol):
    """Abstract interface for the three‑clock model.
    Primary tick notification is via ``subscribe_tick`` which receives the
    full ``Event`` object (payload includes step count and realtime stamp).
    """

    # ----- read‑only -------------------------------------------------
    def real_time(self) -> datetime:
        """Current wall‑clock (datetime.now() in production)."""

    def global_step(self) -> int:
        """Current global step counter."""

    def actor_step(self, actor_id: str) -> int:
        """Step count for a given actor/system."""

    # ----- registration ------------------------------------------------
    def register_actor(self, actor_id: str) -> None:
        """Ensure ``actor_id`` exists with an initial step count of 0.
        Called before any ``inc_actor_step`` to avoid accidental typos.
        """

    # ----- mutators --------------------------------------------------
    def tick(self) -> None:
        """Advance the global step, publish a ``global_tick`` event on the
        injected ``EventBusPort``, and invoke any local tick callbacks.
        The ``global_tick`` payload is ``{"step": int, "time": datetime}``.
        """

    def inc_actor_step(self, actor_id: str, delta: int = 1) -> None:
        """Add *delta* to the step count of *actor_id*.
        Caller should have registered the actor first.
        """

    # ----- optional in‑process listeners -------------------------------
    def subscribe_tick(self, handler: Callable[[Event], None]) -> None:
        """Register a callback that receives the full ``Event`` emitted on each tick.
        The callback can inspect ``event.payload['step']`` and ``event.payload['time']``.
        """

    def unsubscribe_tick(self, handler: Callable[[Event], None]) -> None:
        """Remove a previously registered tick callback."""

    # ----- utility ----------------------------------------------------
    def reset(self) -> None:
        """Reset global step to 0 and clear all actor counters.
        Useful for tests or re‑initialising the clock.
        """
```

*Notes*
- Intended to be injected where needed (TriggerEngine, TurnManager, etc.).
- Concrete implementation can live in `core/time.py` and expose a singleton instance.
- Adding this port makes the clocks first‑class citizens and clarifies their usage across the codebase.
- The implementation should protect mutable state with a lock if multithreading is introduced later.
- ``subscribe_tick`` is now the primary way for in‑process components to receive tick notifications; the bus publish remains for cross‑process listeners.

## Item 14 – Turn‑manager scalability assessment

The turn‑manager design was updated in **step_1_working.md** (see the recent edits).  
Key points:

- The baseline `InMemoryTurnManager` now uses a `set` of actor IDs and an `idx` dict, giving O(1) `add_actor`, `remove_actor`, and membership checks. This eliminates the linear scan that would become costly with many System 1 agents.
- A `size()` helper was added for quick introspection.
- The hierarchical registration note was added so each nested VSM registers its own manager with the parent via `add_actor(child_tm.id)`.
- An optional **WeightedRootManager** sketch was added to allow unequal time slices for child VSMs; it still runs in O(1) per tick.
- The root manager still interleaves sub‑managers in a simple round‑Robin, which scales well because the per‑tick work is constant regardless of the total number of actors across all VSMs.
- Persistence remains trivial (save the `actor_order` list).

Overall, the design now supports dozens‑to‑hundreds of System 1 agents without degrading per‑tick performance, and the optional weighted manager gives a path for future scaling needs.

*Note: the concrete code changes were applied to `step_1_working.md`; this file only records the assessment.*

