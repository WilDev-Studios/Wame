from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from wame.engine import Engine

from wame.vector import IntVector2, IntVector3
from wame.render import Renderer
from wame.input import TextInput
from wame.button import Button

from OpenGL.GL import *

import pygame

class Scene:
    '''Handles all events and rendering for the engine'''

    def __init__(self, engine:'Engine') -> None:
        '''
        Instantiate a new scene
        
        Parameters
        ----------
        engine : `wame.Engine`
            The engine instance
        '''
        
        self.engine:'Engine' = engine
        '''The engine running the scene'''

        self.screen:pygame.Surface = self.engine.screen
        '''The screen rendering all objects'''

        self._buttons:list[Button] = []
    
    def _check_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    self.on_key_pressed(event.key, event.mod)
                case pygame.KEYUP:
                    self.on_key_released(event.key, event.mod)
                case pygame.MOUSEBUTTONDOWN:
                    mousePosition:IntVector2 = IntVector2.from_tuple(event.pos)
                    
                    if event.button in [4, 5]:
                        continue

                    for button in self._buttons:
                        button._check_click(mousePosition)

                    self.on_mouse_pressed(mousePosition)
                case pygame.MOUSEBUTTONUP:
                    mousePosition:IntVector2 = IntVector2.from_tuple(event.pos)

                    self.on_mouse_released(mousePosition)
                case pygame.MOUSEMOTION:
                    mousePosition:IntVector2 = IntVector2.from_tuple(event.pos)

                    for button in self._buttons:
                        button._check_hover(mousePosition)

                    self.on_mouse_move(mousePosition, IntVector2.from_tuple(event.rel))
                case pygame.MOUSEWHEEL:
                    mousePosition:IntVector2 = IntVector2.from_tuple(pygame.mouse.get_pos())

                    self.on_mouse_wheel_scroll(mousePosition, event.y)
                case pygame.QUIT:
                    self.engine._running = False

                    self.on_quit()
                case pygame.WINDOWENTER:
                    self.engine._set_fps = self.engine.settings.max_fps
                case pygame.WINDOWLEAVE:
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
    
    def _first(self) -> Self:
        if self.engine._renderer == Renderer.OPENGL:
            color:IntVector3 = self.engine._background_color
            glClearColor(color.x / 255, color.y / 255, color.z / 255, 1.0)

        self.on_first()

        return self

    def _render(self) -> None:
        if self.engine._renderer == Renderer.PYGAME:
            self.engine.screen.fill(self.engine._background_color.to_tuple())
        else:
            color:IntVector3 = self.engine._background_color
            glClearColor(color.x / 255, color.y / 255, color.z / 255, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.on_render()

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
    
    def on_mouse_move(self, mousePosition:IntVector2, relative:IntVector2) -> None:
        '''
        Code below should be executed when the mouse moves

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_move(self, mousePosition:wame.IntVector2, relative:wame.IntVector2) -> None:
                print(f"Mouse was moved {relative} amount @ {mousePosition}")
        ```
        '''
        
        ...
    
    def on_mouse_pressed(self, mousePosition:IntVector2) -> None:
        '''
        Code below should be executed when a mouse button was pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_pressed(self, mousePosition:wame.IntVector2) -> None:
                ... # Start shooting, rotate character, etc.
        ```
        '''
        
        ...
    
    def on_mouse_released(self, mousePosition:IntVector2) -> None:
        '''
        Code below should be executed when a mouse button was released

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_released(self, mousePosition:wame.IntVector2) -> None:
                ... # Shoot arrow, stop shooting, etc.
        ```
        '''
        
        ...
    
    def on_mouse_wheel_scroll(self, mousePosition:IntVector2, amount:int) -> None:
        '''
        Code below should be executed when the scroll wheel moves

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_mouse_wheel_scroll(self, mousePosition:wame.IntVector2, amount:int) -> None:
                if amount > 0:
                    print(f"Scroll wheel moved up @ {mousePosition}!")
                else:
                    print(f"Scroll wheel moved down @ {mousePosition}!")
        ```
        '''

        ...

    def on_start(self) -> None:
        '''
        Code below should be executed when the engine is starting

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_start(self) -> None:
                ... # Create threads, background processes for networking, etc.
        ```
        '''
        
        ...
    
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
    
    def on_quit(self) -> None:
        '''
        Code below should be executed when the engine quits

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_quit(self) -> None:
                ... # Save data, cleanup objects, etc.
        ```
        '''
        
        ...