from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.plugins.events.base import Event

class SceneEvent(Event):
    '''Base scene event implementation for `wame` plugins.'''

    @property
    def scene(self) -> 'Scene':
        '''The active scene that dispatched this event.'''
        return self._scene