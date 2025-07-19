__all__ = ("ExecutionStep",)

class ExecutionStep:
    '''Plugin execution flow for controlling when events are dispatched - Does not affect `~LifetimeEvent`.'''

    BEFORE: int = 1
    '''Execute before the engine handles the event - Does not affect `~LifetimeEvent`.'''

    AFTER: int = 2
    '''Execute after the engine handles the event - Does not affect `~LifetimeEvent`.'''