from wame.plugins.events.base import CancellableEvent
from wame.plugins.events.scene.base import SceneEvent
from wame.vector.xy import IntVector2

class MouseEvent(SceneEvent, CancellableEvent):
    '''Base mouse event implementation.'''

    @property
    def position(self) -> IntVector2:
        return self._position

class MouseMoveEvent(MouseEvent):
    '''Dispatched when the scene recognizes that the mouse has moved.'''

    @property
    def relative(self) -> IntVector2:
        '''The amount of pixels the mouse has moved.'''
        return self._relative
    
class MousePressedEvent(MouseEvent):
    '''Dispatched when the scene recognizes that a button on the mouse has been pressed.'''

    @property
    def button(self) -> int:
        '''The ID of the button pressed.'''
        return self._button

class MouseReleasedEvent(MouseEvent):
    '''Dispatched when the scene recognizes that a button on the mouse has been released.'''

    @property
    def button(self) -> int:
        '''The ID of the button released.'''
        return self._button

class MouseWheelScrollEvent(MouseEvent):
    '''Dispatched when the scene recognizes that the scroll wheel on the mouse has moved.'''

    @property
    def amount(self) -> int:
        '''The amount the scroll wheel has moved - Positive if `up`, negative if `down`.'''
        return self._amount