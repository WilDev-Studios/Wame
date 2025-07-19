from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.color.rgb import ColorRGB
from wame.plugins.events.base import Event
from wame.pipeline import Pipeline

class EngineEvent(Event):
    '''Base engine event implementation.'''

class BackgroundChangedEvent(EngineEvent):
    '''Dispatched when the engine's background color changed.'''

    @property
    def color(self) -> ColorRGB:
        '''The new background color.'''
        return self._color

class GameLoopStatusChangedEvent(EngineEvent):
    '''Dispatched when the engine's game loop enabled status changed.'''

    @property
    def enabled(self) -> bool:
        '''If the game loop is enabled.'''
        return self._enabled

class GameLoopSteppedEvent(EngineEvent):
    '''Dispatched when the game loop has been polled to step.'''

class MouseLockChangedEvent(EngineEvent):
    '''Dispatched when the mouse's lock state changed.'''

    @property
    def locked(self) -> bool:
        '''If the mouse is locked.'''
        return self._locked

class MouseVisibilityChangedEvent(EngineEvent):
    '''Dispatched when the mouse's visibility changed.'''

    @property
    def visible(self) -> bool:
        '''If the mouse is visible.'''
        return self._visible

class PipelineChangedEvent(EngineEvent):
    '''Dispatched when the rendering pipeline has changed.'''

    @property
    def pipeline(self) -> Pipeline:
        '''The new rendering pipeline.'''
        return self._pipeline

class SceneRegisteredEvent(EngineEvent):
    '''Dispatched when the engine registers a scene.'''

    @property
    def name(self) -> str:
        '''The name of the registered scene.'''
        return self._name

    @property
    def scene(self) -> 'Scene':
        '''The scene that was registered - Not to be confused with the `Engine`'s current scene.'''
        return self._scene

class SceneSwitchedEvent(EngineEvent):
    '''Dispatched when the engine's scene switches.'''

    @property
    def name(self) -> str:
        '''The name registered to this scene.'''
        return self._name
    
    @property
    def scene(self) -> 'Scene':
        '''The scene that the engine switched to.'''
        return self._scene

class UpdateIntervalChangedEvent(EngineEvent):
    '''Dispatched when the fixed update interval changed.'''

    @property
    def interval(self) -> float:
        '''The new fixed update interval.'''
        return self._interval