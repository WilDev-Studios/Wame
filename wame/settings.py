from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.engine import Engine

from wame.pipeline import Pipeline

import pygame

class Settings:
    '''Engine Global Settings'''

    def __init__(self, data:dict[str, int], engine:'Engine') -> None:
        """
        Warning
        -------
        This is an internal object and should not be instantiated elsewhere.
        """
        
        self._engine:'Engine' = engine

        self._antialiasing:int = data["antialiasing"] if "antialiasing" in data else 0

        self._max_fps:int = data["max_fps"] if "max_fps" in data else 0

        self._tabbed_fps:int = data["tabbed_fps"] if "tabbed_fps" in data else 30

        self._vsync:int = data["vsync"] if "vsync" in data else 0

    @property
    def antialiasing(self) -> bool:
        '''Graphics technique used to remove jagged edges'''

        return bool(self._antialiasing)
    
    @antialiasing.setter
    def antialiasing(self, value:bool) -> None:
        if not isinstance(value, bool):
            error:str = "Antialiasing setting must be a boolean"
            raise ValueError(error)
        
        self._antialiasing = int(value)
    
    @property
    def max_fps(self) -> int:
        '''The maximum framerate that the engine will render scenes at'''

        return self._max_fps
    
    @max_fps.setter
    def max_fps(self, value:int) -> None:
        if not isinstance(value, int):
            error:str = "Max FPS value must be an integer"
            raise ValueError(error)
        
        if value < 0:
            error:str = "Max FPS value must be 0 or above"
            raise ValueError(error)
        
        self._max_fps = value
        self._engine._set_fps = self._max_fps
    
    @property
    def tabbed_fps(self) -> int:
        '''The maximum framerate that the engine will render scenes at when the cursor is outside the application'''

        return self._tabbed_fps

    @tabbed_fps.setter
    def tabbed_fps(self, value:int) -> None:
        if not isinstance(value, int):
            error:str = "Tabbed FPS value must be an integer"
            raise ValueError(error)
        
        if value < 0:
            error:str = "Tabbed FPS value must be 0 or above"
            raise ValueError(error)
        
        self._tabbed_fps = value
    
    @property
    def vsync(self) -> bool:
        '''Syncs the graphics card's framerate with the refresh rate of the display device'''

        return bool(self._vsync)
    
    @vsync.setter
    def vsync(self, value:bool) -> None:
        if not isinstance(value, bool):
            error:str = "VSync value must be a boolean"
            raise ValueError(error)
        
        self._vsync = int(value)

        if self._engine._pipeline == Pipeline.PYGAME:
            self.screen = pygame.display.set_mode(self._engine._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF, display=self._engine._display, vsync=self._vsync)
        else:
            self.screen = pygame.display.set_mode(self._engine._size.to_tuple(), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL, display=self._engine._display, vsync=self._vsync)

    def export(self) -> dict[str, int]:
        return {
            "antialiasing": self._antialiasing,
            "max_fps": self._max_fps,
            "tabbed_fps": self._tabbed_fps,
            "vsync":self._vsync
        }