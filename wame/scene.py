from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.engine import Engine

from wame.pipeline import Pipeline
from wame.ui.frame import Frame
from wame.vector import IntVector2

from OpenGL.GL import *

import pygame

class Scene(ABC):
    '''Handles all events and rendering for the engine'''

    def __init__(self, engine:'Engine') -> None:
        '''
        Warning
        -------
        All `Scene` objects/instances are managed and created internally by the `Engine`. At no point will any developer need to do anything more than define a subclass of `Scene`.
        '''
        
        self.engine:'Engine' = engine
        '''The engine running the scene'''

        self.screen:pygame.Surface = self.engine.screen
        '''The screen rendering all objects'''

        self.frame:Frame = Frame(engine)
        '''The UI frame responsible for handling all scene UI objects natively - Rendered each frame after `on_render` automatically'''
        self.frame.set_pixel_position((0, 0))
        self.frame.set_pixel_size((self.screen.get_width(), self.screen.get_height()))

        self._first_elapsed:bool = False

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.on_key_pressed(event.key, event.mod)
            elif event.type == pygame.KEYUP:
                self.on_key_released(event.key, event.mod)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition: IntVector2 = IntVector2.from_tuple(event.pos)

                if event.button in [4, 5]:  # Scrolling shouldn't send a `MOUSEBUTTONDOWN` event
                    continue

                self.on_mouse_pressed(mousePosition, event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePosition: IntVector2 = IntVector2.from_tuple(event.pos)

                if event.button in [4, 5]:  # Scrolling shouldn't send a `MOUSEBUTTONUP` event
                    continue

                self.on_mouse_released(mousePosition, event.button)
            elif event.type == pygame.MOUSEMOTION:
                mousePosition: IntVector2 = IntVector2.from_tuple(event.pos)

                self.on_mouse_move(mousePosition, IntVector2.from_tuple(event.rel))
            elif event.type == pygame.MOUSEWHEEL:
                mousePosition: IntVector2 = IntVector2.from_tuple(pygame.mouse.get_pos())

                self.on_mouse_wheel_scroll(mousePosition, event.y)
            elif event.type == pygame.QUIT:
                self.engine._running = False

                self.on_quit()
            elif event.type == pygame.WINDOWENTER:
                self.engine._set_fps = self.engine.settings.max_fps
            elif event.type == pygame.WINDOWLEAVE:
                self.engine._set_fps = self.engine.settings.tabbed_fps
    
    def _check_keys(self) -> None:
        keys:pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        mods:int = pygame.key.get_mods()

        for key in range(len(keys)):
            if not keys[key]:
                continue

            self.on_key_pressing(key, mods)
    
    def _cleanup(self) -> None:
        self.on_cleanup()
    
    def _first(self) -> None:
        self.on_first()

        self._first_elapsed = True

    def _render(self) -> None:
        if self.engine._pipeline == Pipeline.PYGAME:
            self.engine.screen.fill(self.engine.background_color.to_tuple())
        elif self.engine._pipeline == Pipeline.OPENGL:
            glClearColor(self.engine.background_color.nr, self.engine.background_color.ng, self.engine.background_color.nb, self.engine.background_color.a)

        self.on_render()
        self.frame.ask_render()

        pygame.display.flip()
        self.engine._deltaTime = self.engine._clock.tick(self.engine._set_fps) / 1000.0

    def _update(self) -> None:
        self.on_update()
    
    def on_cleanup(self) -> None:
        '''
        Code below should be executed when the scene is being switched/cleaned up

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_cleanup(self) -> None:
                ... # Terminate background threads, save data, etc.
        ```
        '''

        ...

    def on_first(self) -> None:
        '''
        Code below should be executed when the scene is about to start rendering

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_first(self) -> None:
                ... # Start game timers, etc.
        ```
        '''

        ...

    def on_key_pressed(self, key:int, mods:int) -> None:
        '''
        Code below should be executed when a key is pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_key_pressed(self, key:int, mods:int) -> None:
                ... # Pause game, display UI, etc.
        ```
        '''
        
        ...
    
    def on_key_pressing(self, key:int, mods:int) -> None:
        '''
        Code below should be executed when a key is being pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_key_pressing(self, key:int, mods:int) -> None:
                ... # Move forward, honk horn, etc.
        ```
        '''
        
        ...
    
    def on_key_released(self, key:int, mods:int) -> None:
        '''
        Code below should be executed when a key is released

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_key_released(self, key:int, mods:int) -> None:
                ... # Stop moving forward, etc.
        ```
        '''
        
        ...
    
    def on_mouse_move(self, mouse_position:IntVector2, relative:IntVector2) -> None:
        '''
        Code below should be executed when the mouse moves

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_move(self, mouse_position:wame.IntVector2, relative:wame.IntVector2) -> None:
                print(f"Mouse was moved {relative} amount @ {mouse_position}")
        ```
        '''
        
        ...
    
    def on_mouse_pressed(self, mouse_position:IntVector2, button:int) -> None:
        '''
        Code below should be executed when a mouse button was pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_pressed(self, mouse_position:wame.IntVector2, button:int) -> None:
                ... # Start shooting, rotate character, etc.
        ```
        '''
        
        ...
    
    def on_mouse_released(self, mouse_position:IntVector2, button:int) -> None:
        '''
        Code below should be executed when a mouse button was released

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_released(self, mouse_position:wame.IntVector2, button:int) -> None:
                ... # Shoot arrow, stop shooting, etc.
        ```
        '''
        
        ...
    
    def on_mouse_wheel_scroll(self, mouse_position:IntVector2, amount:int) -> None:
        '''
        Code below should be executed when the scroll wheel moves

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_wheel_scroll(self, mouse_position:wame.IntVector2, amount:int) -> None:
                if amount > 0:
                    print(f"Scroll wheel moved up @ {mouse_position}!")
                else:
                    print(f"Scroll wheel moved down @ {mouse_position}!")
        ```
        '''

        ...

    @abstractmethod
    def on_render(self) -> None:
        '''
        Code below should be executed every frame to render all objects after being updated
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_render(self) -> None:
                ... # Render text, objects, etc.
        ```
        '''

        ...

    @abstractmethod
    def on_update(self) -> None:
        '''
        Code below should be executed every frame before objects are rendered to provide updates to instance states

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_update(self) -> None:
                ... # Update positions, text, etc.
        ```
        '''
        
        ...