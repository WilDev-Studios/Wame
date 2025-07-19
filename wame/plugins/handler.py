from typing import Any, Callable
from wame.plugins.events import *
from wame.plugins.execution import ExecutionStep

__all__ = ("on_event",)

def on_event(event: type[Event], execution: ExecutionStep = ExecutionStep.AFTER) -> Callable[[Any], None]:
    '''
    Register a plugin to listen to a specific event at a desired execution step.
    Use as a decorator in a plugin implementation.
    
    Parameters
    ----------
    event : Event
        Any `~Event`-like object you would like to listen for.
    execution: ExecutionStep
        The desired time in which this event will be fired for the plugin to handle.
    '''
    
    def wrapper(func: Callable) -> Callable:
        func.__wame_event__ = event
        func.__wame_execution__ = execution
        
        return func
    
    return wrapper