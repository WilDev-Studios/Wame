from wame.plugins.events.base import CancellableEvent
from wame.plugins.events.scene.base import SceneEvent
from wame.vector.xy import IntVector2

class JoystickEvent(SceneEvent, CancellableEvent):
    '''Base joystick event implementation.'''

    @property
    def joystick(self) -> int:
        '''The joystick that this event is associated with.'''
        return self._joystick

class JoystickAxisMotionEvent(JoystickEvent):
    '''Dispatched when the scene recognizes movement in a joystick axis.'''
    
    @property
    def axis(self) -> int:
        '''The axis of motion in which the joystick moved.'''
        return self._axis
    
    @property
    def position(self) -> float:
        '''The new position of the joystick that moved.'''
        return self._position

class JoystickButtonDownEvent(JoystickEvent):
    '''Dispatched when the scene recognizes that a button has been pressed on a joystick.'''

    @property
    def button(self) -> int:
        '''The button that was pressed.'''
        return self._button
    
class JoystickButtonUpEvent(JoystickEvent):
    '''Dispatched when the scene recognizes that a button has been released on a joystick.'''

    @property
    def button(self) -> int:
        '''The button that was released.'''
        return self._button

class JoystickDeviceAddedEvent(JoystickEvent):
    '''Dispatched when the scene recognizes that a joystick device has been added to the system.'''

class JoystickDeviceRemovedEvent(JoystickEvent):
    '''Dispatched when the scene recognizes that a joystick device has been removed from the system.'''

class JoystickHatMotionEvent(JoystickEvent):
    '''Dispatched when the scene recognizes that the hat of a joystick has moved.'''

    @property
    def hat(self) -> int:
        '''The ID of the hat that moved.'''
        return self._hat
    
    @property
    def position(self) -> IntVector2:
        '''The new position of the hat that moved.'''
        return self._position