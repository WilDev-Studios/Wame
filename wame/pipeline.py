from __future__ import annotations

from enum import auto, Enum

class Pipeline(Enum):
    '''Engine Rendering Pipeline.'''

    PYGAME: int = auto()
    '''
    Pygame will render all elements/objects.
    '''

    OPENGL: int = auto()
    '''
    OpenGL will render all elements/objects.

    Warning
    -------
    `OpenGL` is not handled by the `Engine` at all. You must create your own context(s) in a `Scene`'s `on_first` method.
    '''