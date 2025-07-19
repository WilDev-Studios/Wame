from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from abc import ABC, abstractmethod
from typing import Callable, Union
from wame.pipeline import Pipeline
from wame.vector.xy import IntVector2

import pygame

__all__ = ("Element",)

class Element(ABC):
    '''Base User-Interface Element/Object.'''

    __slots__ = ("_scene", "_parent", "_children", "enabled", "_tween_callback",)
    _scene: 'Scene'
    _parent: Element
    _children: list[Element]
    enabled: bool
    _tween_callback: Callable[[None], None]

    @abstractmethod
    def __init__(self, scene: 'Scene', parent: Element) -> None:
        '''
        Create a new inherited UI element.
        '''
    
        self._scene: 'Scene' = scene
        self._parent: Element = parent
        self._children: list[Element] = []

        self.enabled: bool = True
        '''If this element is enabled.'''

        self._tween_callback: Callable[[None], None] = None
        self._scene._events_update.add(self._update)

    @abstractmethod
    def __repr__(self) -> str:
        ...

    def _apply_transform(self) -> None:
        ...

    def _calculate_transform(self) -> tuple[IntVector2, ...]:
        ...

    @staticmethod
    def _interpolate(start: Union[int, float], end: Union[int, float], progress: float) -> Union[int, float]:
        ...

    @abstractmethod
    def _update(self) -> None:
        ...

    def add_child(self, child: Element) -> None:
        '''
        Add a child to this element.
        
        Parameters
        ----------
        child : Element
            The child to add to this element.
        
        Raises
        ------
        TypeError
            If the child provided is not an `Element`.
        '''

        if not isinstance(child, Element):
            error: str = "Type of provided child must be an Element."
            raise TypeError(error)

        self._children.append(child)

    @property
    @abstractmethod
    def bounds(self) -> pygame.Rect:
        '''The bounding `pygame.Rect` of this element.'''
        ...

    @property
    def children(self) -> tuple[Element]:
        '''All children of this element.'''
        return tuple(self._children)

    @property
    def parent(self) -> Element:
        '''The parent of this element.'''
        return self._parent

    def remove_child(self, child: Element) -> None:
        '''
        Remove a child from this element.
        
        Parameters
        ----------
        child : Element
            The child to remove from this element.
        
        Raises
        ------
        TypeError
            If the child provided is not an `Element`.
        '''

        if not isinstance(child, Element):
            error: str = "Type of provided child must be an Element."
            raise TypeError(error)
    
        self._children.remove(child)

    @abstractmethod
    def render(self) -> None:
        '''Forceably render this element to the screen using an already-implemented `Pygame` rendering program.'''
        ...

    def render_opengl(self) -> None:
        '''Forceably render this element to the screen using a custom-implemented OpenGL rendering program.'''
        
        error: str = "You must subclass this object and overwrite the `render_opengl` method with your own program."
        raise RuntimeError(error)

    def request_render(self) -> None:
        '''Render this element and it's children to the screen, if enabled.'''

        if not self.enabled:
            return
        
        if self._scene.engine.pipeline == Pipeline.PYGAME:
            self.render()
        elif self._scene.engine.pipeline == Pipeline.OPENGL:
            self.render_opengl()

        for child in self._children:
            child.request_render()
    
    def set_tween_callback(self, callback: Callable[[None], None]) -> None:
        '''
        Set a callback method for when this element finishes tweening/animating.
        '''

        self._tween_callback = callback
    
    @abstractmethod
    def tween(self, end, duration: float, easing: Callable[[float], float]) -> None:
        '''
        Tween/Animate this element to an end state over a period of time.
        '''
        ...