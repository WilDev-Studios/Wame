from __future__ import annotations

from wame.vector import IntVector2

import pygame
import wame

class Renderable:
    '''Base UI object that all `wame` UI objects inherit'''

    def __init__(self, engine:'wame.Engine') -> None:
        '''
        Instantiate a renderable UI object
        
        Parameters
        ----------
        engine : wame.Engine
            The engine to hook this UI object to
        '''
        
        self._engine:'wame.Engine' = engine

        self.enabled:bool = True
        '''If this renderable should render on the screen'''

        self.position:IntVector2 = None
        '''The absolute X, Y position (pixel position) of this object'''

        self.size:IntVector2 = None
        '''The absolute X, Y size (pixel amount) of this object'''

        self._children:list[Renderable] = []

    def add_child(self, child:'Renderable') -> None:
        '''
        Add a subordinate child object to this UI object
        
        Parameters
        ----------
        child : wame.ui.renderable.Renderable
            The child renderable object
        
        Raises
        ------
        ValueError
            If the provided child is not a `Renderable`
        '''

        if not isinstance(child, Renderable):
            error:str = "Child object must be an instance of `wame.ui.renderable.Renderable`"
            raise ValueError(error)
    
        self._children.append(child)

    def ask_render(self) -> None:
        '''Request to render if this renderable is enabled'''
        
        if not self.enabled:
            return
        
        self.render()

    @property
    def rect(self) -> pygame.Rect:
        '''The bounding size and positions of this object'''
        
        return pygame.Rect(self.position.to_tuple(), self.size.to_tuple())

    def remove_child(self, child:'Renderable') -> None:
        '''
        Remove a subordinate child object from this UI object
        
        Parameters
        ----------
        child : wame.ui.renderable.Renderable
            The child renderable object
        
        Raises
        ------
        ValueError
            - Child must be a `Renderable`
            - Child was not found as a child to this parent
        '''

        if not isinstance(child, Renderable):
            error:str = "Child object must be an instance of `wame.ui.renderable.Renderable`"
            raise ValueError(error)
        
        try:
            self._children.remove(child)
        except ValueError:
            error:str = "Child object was not found in the parent frame"
            raise ValueError(error)

    def render(self) -> None:
        '''
        Render this object to the screen
        
        Note
        ----
        This should only be called by the `~ask_render` method, as this ignores the objects `enabled` attribute.'''
        
        for child in self._children:
            child.ask_render()