from __future__ import annotations

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.vector.xy import IntVector2, FloatVector2

from OpenGL.GL import *

import pygame

class Button(Renderable):
    '''UI Button Object.'''

    __slots__ = (
        "_parent", "_click_callback", "_hovering", "_hover_callback",
        "_unhover_callback",
    )

    def __init__(self, scene: 'Scene', parent: Frame) -> None:
        '''
        Instantiate a new button.
        
        Parameters
        ----------
        scene : Scene
            The scene handling this button for automatic event dispatching.
        parent : Frame
            The parent frame that this button will be a child to.
        '''
        
        super().__init__(parent._engine)

        parent.add_child(self)
        
        self._parent:Frame = parent
        scene._subscribers_mouse_click.add(self._check_click)
        scene._subscribers_mouse_move.add(self._check_hover)

        self._click_callback:Callable = None

        self._hovering:bool = False
        self._hover_callback:Callable = None
        self._unhover_callback:Callable = None

    def _check_click(self, position: IntVector2, _: int) -> None:
        if not self.rect.collidepoint(position.to_tuple()):
            return
        
        if not self._click_callback:
            return
        
        self._click_callback()
    
    def _check_hover(self, position: IntVector2, _: IntVector2) -> None:
        if self.rect.collidepoint(position.to_tuple()):
            if not self._hovering:
                self._hovering = True

                if self._hover_callback:
                    self._hover_callback()
        else:
            if self._hovering:
                self._hovering = False

                if self._unhover_callback:
                    self._unhover_callback()

    def render(self) -> None:
        for child in self._children:
            child.ask_render()

    def set_click_callback(self, func: Callable[[], None]) -> None:
        '''
        Set the callback for when this object is clicked.
        
        Parameters
        ----------
        func : typing.Callable[[], None]
            The callback method to execute when clicked.
        '''

        self._click_callback = func
    
    def set_hover_callback(self, func: Callable[[], None]) -> None:
        '''
        Set the callback for when this object is hovered over.
        
        Parameters
        ----------
        func : typing.Callable[[], None]
            The callback method to execute when hovered over.
        '''
        
        self._hover_callback = func

    def set_pixel_transform(self, position: IntVector2, size: IntVector2) -> None:
        '''
        Set the exact pixel transform (position, size) of this object.
        
        Parameters
        ----------
        position : IntVector2
            The exact position of this object from the top-left point.
        size : IntVector2
            The exact size of this object.
        '''

        position = position if isinstance(position, IntVector2) else IntVector2.from_iterable(position)
        position.x += self._parent.rect.left
        position.y += self._parent.rect.top

        size = size if isinstance(size, IntVector2) else IntVector2.from_iterable(size)

        self.rect = pygame.Rect(*position, *size)
    
    def set_scaled_transform(self, position: FloatVector2, size: FloatVector2) -> None:
        '''
        Set the scaled transform (position, size) of this object.
        
        Parameters
        ----------
        position : FloatVector2
            The scaled position of this object from the top-left point.
        size : FloatVector2
            The scaled size of this object.
        '''

        position = position if isinstance(position, FloatVector2) else FloatVector2.from_iterable(position)
        size = size if isinstance(size, FloatVector2) else FloatVector2.from_iterable(size)

        if position.x < 0 or position.x > 1 or position.y < 0 or position.y > 1:
            error: str = "Scaled position X, Y values must be between 0 and 1."
            raise ValueError(error)
        
        if size.x < 0 or size.x > 1 or size.y < 0 or size.y > 1:
            error: str = "Scaled size X, Y values must be between 0 and 1."
            raise ValueError(error)
        
        position = IntVector2(
            int(self._parent.rect.left + (self._parent.rect.width * position.x)),
            int(self._parent.rect.top + (self._parent.rect.height * position.y))
        )
        size = IntVector2(
            int(self._parent.rect.width * size.x),
            int(self._parent.rect.height * size.y)
        )

        self.rect = pygame.Rect(*position, *size)
    
    def set_unhover_callback(self, func: Callable[[], None]) -> None:
        '''
        Set the callback for when this object is no longer hovered over.
        
        Parameters
        ----------
        func : typing.Callable[[], None]
            The callback method to execute when no longer hovered over.
        '''

        self._unhover_callback = func