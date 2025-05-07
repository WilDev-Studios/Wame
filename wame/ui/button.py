from __future__ import annotations

from typing import Callable

from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.vector.xy import IntVector2, FloatVector2

from OpenGL.GL import *

class Button(Renderable):
    '''UI Button Object'''

    def __init__(self, parent:Frame) -> None:
        '''
        Instantiate a new button
        
        Parameters
        ----------
        parent : wame.ui.frame.Frame
            The parent frame that this button will be a child to
        '''
        
        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent:Frame = parent

        self._click_callback:Callable = None

        self._hovering:bool = False
        self._hover_callback:Callable = None
        self._unhover_callback:Callable = None

    def check_click(self, position:IntVector2) -> None:
        '''
        Check to see if the mouse clicked this object, and handles appropriately if so
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The position of the mouse
        '''
        
        if not self.rect.collidepoint(position.to_tuple()):
            return
        
        if not self._click_callback:
            return
        
        self._click_callback()
    
    def check_hover(self, position:IntVector2) -> None:
        '''
        Check to see if the mouse is hovering over this object, and handles appropriately if so
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The position of the mouse
        '''
        
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

    def set_click_callback(self, func:Callable[[], None]) -> None:
        '''
        Set the callback for when this object is clicked
        
        Parameters
        ----------
        func : typing.Callable[[], None]
            The callback method to execute when clicked
        '''

        self._click_callback = func
    
    def set_hover_callback(self, func:Callable[[], None]) -> None:
        '''
        Set the callback for when this object is hovered over
        
        Parameters
        ----------
        func : typing.Callable[[], None]
            The callback method to execute when hovered over
        '''
        
        self._hover_callback = func

    def set_pixel_position(self, position:IntVector2) -> None:
        '''
        Set the exact pixel position of this object
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The exact position of this object from the top-left point
        '''

        position = position if isinstance(position, IntVector2) else IntVector2.from_tuple(position)

        if self._parent:
            position.x += self._parent.position.x
            position.y += self._parent.position.y
        
        self.position = position

    def set_pixel_size(self, size:IntVector2) -> None:
        '''
        Set the exact pixel size of this object
        
        Parameters
        ----------
        size : wame.vector.xy.IntVector2
            The exact size of this object
        '''

        self.size = size if isinstance(size, IntVector2) else IntVector2.from_tuple(size)

    def set_scaled_position(self, position:FloatVector2) -> None:
        '''
        Set the scaled position of this object
        
        Parameters
        ----------
        position : wame.vector.xy.FloatVector2
            The scaled position of this object from the top-left point
        '''

        position = position if isinstance(position, FloatVector2) else FloatVector2.from_tuple(position)

        if position.x > 1 or position.x < 0 or position.y > 1 or position.y < 0:
            error:str = "Scaled position X, Y values must be between 0 and 1"
            raise ValueError(error)

        self.position = IntVector2(
            int(self._parent.position.x + (self._parent.size.x * position.x)),
            int(self._parent.position.y + (self._parent.size.y * position.y))
        )
    
    def set_scaled_size(self, size:IntVector2) -> None:
        '''
        Set the scaled size of this object
        
        Parameters
        ----------
        size : wame.vector.xy.IntVector2
            The scaled size of this object
        '''
        
        size = size if isinstance(size, FloatVector2) else FloatVector2.from_tuple(size)

        if size.x > 1 or size.x < 0 or size.y > 1 or size.y < 0:
            error:str = "Scaled size X, Y values must be between 0 and 1"
            raise ValueError(error)

        self.size = IntVector2(
            int(self._parent.size.x * size.x),
            int(self._parent.size.y * size.y)
        )
    
    def set_unhover_callback(self, func:Callable) -> None:
        '''
        Set the callback for when this object is no longer hovered over
        
        Parameters
        ----------
        func : typing.Callable[[], None]
            The callback method to execute when no longer hovered over
        '''

        self._unhover_callback = func