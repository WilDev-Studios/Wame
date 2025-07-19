from wame.plugins.events.scene.base import SceneEvent
from wame.vector.xy import IntVector2

class WindowEvent(SceneEvent):
    '''Base window event implementation.'''

class WindowCloseEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has closed.'''

class WindowDisplayChangedEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window's display has changed.'''

class WindowFocusGainedEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has gained focus.'''

class WindowFocusLostEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has lost focus.'''

class WindowHiddenEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has been hidden.'''

class WindowMaximizedEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has been maximized.'''

class WindowMinimizedEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has been minimized.'''

class WindowMouseEnterEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the mouse has entered the window.'''

class WindowMouseLeaveEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the mouse has left the window.'''

class WindowMovedEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has moved.'''

    @property
    def position(self) -> IntVector2:
        '''The position of the window.'''
        return self._position

class WindowResizeEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has been resized.'''

    @property
    def size(self) -> IntVector2:
        '''The size of the window.'''
        return self._size

class WindowRestoredEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has been restored.'''

class WindowShownEvent(WindowEvent):
    '''Dispatched when the scene recognizes that the window has been shown.'''