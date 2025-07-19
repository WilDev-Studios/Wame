from wame.plugins.events.base import CancellableEvent
from wame.plugins.events.scene.base import SceneEvent

class KeyEvent(SceneEvent, CancellableEvent):
    '''Base key event implementation.'''

    @property
    def key(self) -> int:
        '''The key that this event relates to.'''
        return self._key
    
    @property
    def mods(self) -> int:
        '''The bitwise-combined keycodes of all modification keys pressed at the time of this event.'''
        return self._mods

class KeyPressedEvent(KeyEvent):
    '''Dispatched when the scene recognizes that a key has been pressed.'''

class KeyPressingEvent(KeyEvent):
    '''Dispatched when the scene recognizes that a key is currently being pressed.'''

class KeyReleasedEvent(KeyEvent):
    '''Dispatched when the scene recognizes that a key has been released.'''