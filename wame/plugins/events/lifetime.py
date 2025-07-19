from wame.plugins.events.base import Event

class LifetimeEvent(Event):
    '''Base lifetime event implementation for `wame` plugins.'''

class LoadEvent(LifetimeEvent):
    '''Dispatched when the engine flags your plugin to load/start.'''

class UnloadEvent(LifetimeEvent):
    '''Dispatched when the engine flags your plugin to unload/stop.'''