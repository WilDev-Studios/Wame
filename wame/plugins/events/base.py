from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.engine import Engine

__all__ = ("Event", "CancellableEvent",)

class Event:
    '''Base event implementation for `wame` plugins.'''

    def __init__(self, engine: 'Engine') -> None:
        self._engine: 'Engine' = engine

    @property
    def engine(self) -> 'Engine':
        '''The engine that is handling this plugin and dispatched this event.'''
        return self._engine

class CancellableEvent(Event):
    '''Base cancellable event implementation for `wame` plugins.'''

    def __init__(self, engine: 'Engine') -> None:
        super().__init__(engine)
        self._cancelled = False

    def cancel(self) -> None:
        '''Cancel this event from being further handled.'''
        self._cancelled = True

    @property
    def is_cancelled(self) -> bool:
        '''Check if this event has already been cancelled.'''
        return self._cancelled