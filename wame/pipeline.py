from __future__ import annotations

class Pipeline:
    '''Engine Rendering Pipeline'''

    PYGAME:int = 0
    '''
    PyGame will render all elements/objects
    '''

    OPENGL:int = 1
    '''
    OpenGL will render all elements/objects

    Warning
    -------
    `OpenGL` is not handled by the `Engine` at all. You must create your own context(s) in a `Scene`'s `on_first` method.
    '''