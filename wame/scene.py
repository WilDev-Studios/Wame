from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wame.engine import Engine

from wame.pipeline import Pipeline
from wame.ui.frame import Frame
from wame.utils.tween import Tween
from wame.vector import IntVector2

from OpenGL.GL import *

import pygame

class Scene(ABC):
    '''Handles all events and rendering for the engine.'''

    def __init__(self, engine:'Engine') -> None:
        '''
        Warning
        -------
        All `Scene` objects/instances are managed and created internally by the `Engine`. At no point will any developer need to do anything more than define a subclass of `Scene`.
        '''
        
        self.engine:'Engine' = engine
        '''The engine running the scene.'''

        self.screen:pygame.Surface = self.engine.screen
        '''The screen rendering all objects.'''

        self.frame:Frame = Frame(engine)
        '''The UI frame responsible for handling all scene UI objects natively - Rendered each frame after `on_render` automatically, unless disabled.'''
        self.frame.set_pixel_position((0, 0))
        self.frame.set_pixel_size((self.screen.get_width(), self.screen.get_height()))

        self._first_elapsed:bool = False
        
        self._events_first: set[Callable[[], None]] = set()
        self._events_update: set[Callable[[], None]] = set()
        
        self.tween:Tween = Tween(self)
        '''The tweening object responsible for animating objects.'''

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.on_joy_axis_motion(event.joy, event.axis, event.value)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.on_joy_button_down(event.joy, event.button)
            elif event.type == pygame.JOYBUTTONUP:
                self.on_joy_button_up(event.joy, event.button)
            elif event.type == pygame.JOYDEVICEADDED:
                self.on_joy_device_added(event.device_index)
            elif event.type == pygame.JOYDEVICEREMOVED:
                self.on_joy_device_removed(event.device_index)
            elif event.type == pygame.JOYHATMOTION:
                self.on_joy_hat_motion(event.joy, event.hat, IntVector2.from_iterable(event.value))
            elif event.type == pygame.KEYDOWN:
                self.on_key_pressed(event.key, event.mod)
            elif event.type == pygame.KEYUP:
                self.on_key_released(event.key, event.mod)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition: IntVector2 = IntVector2.from_iterable(event.pos)

                if event.button in [4, 5]:  # Scrolling shouldn't send a `MOUSEBUTTONDOWN` event
                    continue

                self.on_mouse_pressed(mousePosition, event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePosition: IntVector2 = IntVector2.from_iterable(event.pos)

                if event.button in [4, 5]:  # Scrolling shouldn't send a `MOUSEBUTTONUP` event
                    continue

                self.on_mouse_released(mousePosition, event.button)
            elif event.type == pygame.MOUSEMOTION:
                mousePosition: IntVector2 = IntVector2.from_iterable(event.pos)

                self.on_mouse_move(mousePosition, IntVector2.from_iterable(event.rel))
            elif event.type == pygame.MOUSEWHEEL:
                mousePosition: IntVector2 = IntVector2.from_iterable(pygame.mouse.get_pos())

                self.on_mouse_wheel_scroll(mousePosition, event.y)
            elif event.type == pygame.QUIT:
                self.engine._running = False
            elif event.type == pygame.USEREVENT:
                self.on_user_event(event)
            elif event.type == pygame.WINDOWCLOSE:
                self.on_window_close()
            elif event.type == pygame.WINDOWDISPLAYCHANGED:
                self.on_window_display_changed()
            elif event.type == pygame.WINDOWENTER:
                self.on_window_mouse_enter()
            elif event.type == pygame.WINDOWFOCUSGAINED:
                self.on_window_focus_gained()
            elif event.type == pygame.WINDOWFOCUSLOST:
                self.on_window_focus_lost()
            elif event.type == pygame.WINDOWHIDDEN:
                self.on_window_hidden()
            elif event.type == pygame.WINDOWLEAVE:
                self.on_window_mouse_leave()
            elif event.type == pygame.WINDOWMAXIMIZED:
                self.on_window_maximized()
            elif event.type == pygame.WINDOWMINIMIZED:
                self.on_window_minimized()
            elif event.type == pygame.WINDOWMOVED:
                self.on_window_moved(IntVector2(event.x, event.y))
            elif event.type == pygame.WINDOWRESIZED:
                self.on_window_resize(IntVector2.from_iterable(event.size))
            elif event.type == pygame.WINDOWRESTORED:
                self.on_window_restored()
            elif event.type == pygame.WINDOWSHOWN:
                self.on_window_shown()
    
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
        for event in self._events_first:
            event()

        if not self.engine._game_loop_enabled:
            self.engine.step_game_loop()

        self.on_first()

    def _fixed_update(self) -> None:
        self.on_fixed_update()

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
        if not self._first_elapsed:
            self._first_elapsed = True
        
        for event in self._events_update:
            event()

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

    def on_fixed_update(self) -> None:
        '''
        Code below should be executed every configurable, elapsed duration before objects are rendered to provide updates to instance states.

        Info
        ----
        This only runs on a certain configured duration, by default 60 times/second. If you wish to run this every frame, use `on_update`.

        Tip
        ---
        If you wish to change the duration of the fixed update, use `engine.set_update_interval`.

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_fixed_update(self) -> None:
                ... # Update positions, text, etc.
        ```
        '''
        
        ...

    def on_joy_axis_motion(self, stick:int, axis:int, position:float) -> None:
        '''
        Code below should be executed when a joystick's axis moves
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_joy_axis_motion(self, stick:int, axis:int, position:float) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joy_button_down(self, stick:int, button:int) -> None:
        '''
        Code below should be executed when a joystick's button gets pressed
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_joy_button_down(self, stick:int, button:int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joy_button_up(self, stick:int, button:int) -> None:
        '''
        Code below should be executed when a joystick's button gets released
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_joy_button_up(self, stick:int, button:int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joy_device_added(self, device:int) -> None:
        '''
        Code below should be executed when a new joystick device is added
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_joy_device_added(self, device:int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joy_device_removed(self, device:int) -> None:
        '''
        Code below should be executed when an old joystick device is removed
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_joy_device_removed(self, device:int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joy_hat_motion(self, stick:int, hat:int, position:IntVector2) -> None:
        '''
        Code below should be executed when a joystick's hat/D-Pad moves
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_joy_hat_motion(self, stick:int, hat:int, position:wame.IntVector2) -> None:
                ...
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

    def on_tweened(self, object_: Any) -> None:
        '''
        Code below should be executed when a tweened object using `self.tween` has finished tweening.
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)

            def on_tweened(self, object_: Any) -> None:
                ...
        ```
        '''

    def on_user_event(self, event:pygame.event.Event) -> None:
        '''
        Code below should be executed when a custom user event is called
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_user_event(self, event:pygame.event.Event) -> None:
                ...
        ```
        '''

        ...

    def on_window_close(self) -> None:
        '''
        Code below should be executed when the window is requested to close
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_close(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_display_changed(self) -> None:
        '''
        Code below should be executed when the window's display/monitor changes
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_display_changed(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_focus_gained(self) -> None:
        '''
        Code below should be executed when the window gains focus
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_focus_gained(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_focus_lost(self) -> None:
        '''
        Code below should be executed when the window loses focus
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_focus_lost(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_hidden(self) -> None:
        '''
        Code below should be executed when the window is hidden
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_hidden(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_maximized(self) -> None:
        '''
        Code below should be executed when the window gets maximized
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_maximized(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_minimized(self) -> None:
        '''
        Code below should be executed when the window gets minimized
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_minimized(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_mouse_enter(self) -> None:
        '''
        Code below should be executed when the mouse enters the window
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_mouse_enter(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_mouse_leave(self) -> None:
        '''
        Code below should be executed when the mouse leaves the window
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_mouse_leave(self) -> None:
                ...
        ```
        '''

        ...
    
    def on_window_moved(self, position:IntVector2) -> None:
        '''
        Code below should be executed when the window moves
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_moved(self, position:wame.IntVector2) -> None:
                ...
        ```
        '''

        ...

    def on_window_resize(self, size:IntVector2) -> None:
        '''
        Code below should be executed when the window is resized
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_resize(self, size:wame.IntVector2) -> None:
                ... # Edit OpenGL viewport, etc.
        ```
        '''

        ...

    def on_window_restored(self) -> None:
        '''
        Code below should be executed when the window is restored from a minimized or maximized state
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_restored(self) -> None:
                ...
        ```
        '''

        ...

    def on_window_shown(self) -> None:
        '''
        Code below should be executed when window becomes visible
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
            def on_window_shown(self) -> None:
                ...
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