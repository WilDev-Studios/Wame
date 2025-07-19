from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.engine import Engine

from typing import Callable
from wame.plugins.events.base import Event
from wame.plugins.events.lifetime import LifetimeEvent
from wame.plugins.execution import ExecutionStep

__all__ = ("Plugin",)

class Plugin:
    '''Base plugin implementation for `wame` plugins.'''

    __slots__ = (
        "_engine", "_directory", "_lifetime_events", "_events",
    )

    def __init__(self, engine: 'Engine', directory: str) -> None:
        '''
        Instantiate a new plugin instance and register all event listeners and hooks.
        
        Parameters
        ----------
        engine : Engine
            The engine instance responsible for running and interfacing with this plugin.
        directory : str
            The parent folder/directory of this plugin.

        Warning
        -------
        This is an internal method and should not be called externally.
        '''

        self._engine: 'Engine' = engine
        self._directory: str = directory

        self._lifetime_events: dict[Event, set[Callable]] = {}
        self._events: dict[ExecutionStep, dict[Event, set[Callable]]] = {}

        for attribute_name in dir(self):
            method: Callable = getattr(self, attribute_name)

            event: type[Event] = getattr(method, "__wame_event__", None)
            execution: ExecutionStep = getattr(method, "__wame_execution__", None)

            if not event or not execution:
                continue

            if issubclass(event, LifetimeEvent):
                if event not in self._lifetime_events:
                    self._lifetime_events[event] = set()
                
                self._lifetime_events[event].add(method)
                continue

            if execution not in self._events:
                self._events[execution] = {}
            
            if event not in self._events[execution]:
                self._events[execution][event] = set()
            
            self._events[execution][event].add(method)
    
    @property
    def directory(self) -> str:
        '''The directory that this plugin is located in.'''
        return self._directory

    @property
    def engine(self) -> 'Engine':
        '''The engine instance responsible for running and interfacing with this plugin.'''
        return self._engine
    
    def log_critical(self, log: str) -> None:
        '''
        Log a critical error message.
        
        Parameters
        ----------
        log : str
            The message to log to the console.
        '''
        
        self._engine._log_crit(self.__class__.__name__, log)

    def log_debug(self, log: str) -> None:
        '''
        Log a debug message.
        
        Parameters
        ----------
        log : str
            The message to log to the console.
        '''
        
        self._engine._log_dbug(self.__class__.__name__, log)

    def log_info(self, log: str) -> None:
        '''
        Log an informational message.
        
        Parameters
        ----------
        log : str
            The message to log to the console.
        '''
        
        self._engine._log_info(self.__class__.__name__, log)

    def log_warn(self, log: str) -> None:
        '''
        Log a warning message.
        
        Parameters
        ----------
        log : str
            The message to log to the console.
        '''
        
        self._engine._log_warn(self.__class__.__name__, log)