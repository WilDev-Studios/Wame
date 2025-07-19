from pygame.event import Event as PygameEvent
from typing import Any
from wame.plugins.events.base import CancellableEvent
from wame.plugins.events.scene.base import SceneEvent

class CleanupEvent(SceneEvent):
    '''Dispatched when the scene is about to clean up.'''

class FirstEvent(SceneEvent):
    '''Dispatched when the scene is about to begin the game loop.'''

class FixedUpdateEvent(SceneEvent):
    '''Dispatched when the scene is about to run the fixed update cycle.'''

class InitEvent(SceneEvent):
    '''Dispatched when the scene is about to run the developer-defined initializer.'''

    @property
    def args(self) -> Any:
        '''The arguments associated with this scene's loading.'''
        return self._args
    
    @property
    def kwargs(self) -> dict[str, Any]:
        '''The keyword-arguments associated with this scene's loading.'''
        return self._kwargs

class UserEvent(SceneEvent, CancellableEvent):
    '''Dispatched when the scene recognizes that a custom, developer-defined event has been fired.'''

    @property
    def event(self) -> PygameEvent:
        '''The custom, developer-defined event fired by `Pygame`.'''
        return self._event

class RenderEvent(SceneEvent):
    '''Dispatched when the engine flags your plugin to render.'''

class UpdateEvent(SceneEvent):
    '''Dispatched when the engine flags your plugin to update.'''