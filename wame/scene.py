from __future__ import annotations

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wame.engine import Engine

from wame.pipeline import Pipeline
from wame.plugins.execution import ExecutionStep
from wame.plugins.events.base import Event
from wame.plugins.events.scene import *
from wame.ui.frame import Frame
from wame.vector import IntVector2

from OpenGL.GL import *

import pygame
import time
import warnings

__all__ = ("Scene",)

def _warn_init_override(cls):
    original = cls.__init__

    def new(self, *args, **kwargs):
        caller = self.__class__

        if caller is not cls:
            if "__init__" in caller.__dict__:
                warnings.warn(
                    f"{caller.__name__} overrides __init__ which is discouraged. Use on_init instead.",
                    UserWarning, 2
                )
        
        return original(self, *args, **kwargs)

    cls.__init__ = new
    return cls

@_warn_init_override
class Scene:
    '''Handles all events and rendering for the engine.'''

    __slots__ = (
        "engine", "screen", "frame", "_first_elapsed", "_events_first", "_events_update",
        "_subscribers_key_pressed", "_subscribers_mouse_click", "_subscribers_mouse_move",
    )

    def __init__(self, engine: 'Engine', *args, **kwargs) -> None:
        '''
        Warning
        -------
        Do not override `__init__` in subclasses. Use `on_init` instead.
        All `Scene` objects/instances are managed and created internally by the `Engine`. At no point will any developer need to do anything more than define a subclass of `Scene`.
        '''
        
        self.engine: 'Engine' = engine
        '''The engine running the scene.'''

        self.screen: pygame.Surface = self.engine.screen
        '''The screen rendering all objects.'''

        self._first_elapsed: bool = False
        
        self._events_first: set[Callable[[], None]] = set()
        self._events_update: set[Callable[[], None]] = set()

        self._subscribers_key_pressed: set[Callable[[int, int], None]] = set()
        self._subscribers_mouse_click: set[Callable[[IntVector2, int], None]] = set()
        self._subscribers_mouse_move: set[Callable[[IntVector2, IntVector2], None]] = set()

        self._subscribers_key_pressed.add(self.on_key_pressed)
        self._subscribers_mouse_click.add(self.on_mouse_pressed)
        self._subscribers_mouse_move.add(self.on_mouse_move)

        self.frame: Frame = Frame(self, None, position=(0, 0), size=(1.0, 1.0))
        '''The UI frame responsible for handling all scene UI objects natively - Rendered each frame after `on_render` automatically, unless disabled.'''

        self.engine._dispatch_plugin_event(ExecutionStep.BEFORE, InitEvent, args=args, kwargs=kwargs)
        self.on_init(*args, **kwargs)
        self.engine._dispatch_plugin_event(ExecutionStep.AFTER, InitEvent, args=args, kwargs=kwargs)

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self._dispatch(
                    JoystickAxisMotionEvent,
                    self.on_joystick_axis_motion,
                    (event.joy, event.axis, event.value),
                    scene=self, joystick=event.joy, axis=event.axis, position=event.value
                )
            elif event.type == pygame.JOYBUTTONDOWN:
                self._dispatch(
                    JoystickButtonDownEvent,
                    self.on_joystick_button_down,
                    (event.joy, event.button),
                    scene=self, joystick=event.joy, button=event.button
                )
            elif event.type == pygame.JOYBUTTONUP:
                self._dispatch(
                    JoystickButtonUpEvent,
                    self.on_joystick_button_up,
                    (event.joy, event.button),
                    scene=self, joystick=event.joy, button=event.button
                )
            elif event.type == pygame.JOYDEVICEADDED:
                self._dispatch(
                    JoystickDeviceAddedEvent,
                    self.on_joystick_device_added,
                    (event.device_index),
                    scene=self, joystick=event.device_index
                )
            elif event.type == pygame.JOYDEVICEREMOVED:
                self._dispatch(
                    JoystickDeviceRemovedEvent,
                    self.on_joystick_device_removed,
                    (event.device_index),
                    scene=self, joystick=event.device_index
                )
            elif event.type == pygame.JOYHATMOTION:
                position: IntVector2 = IntVector2.from_iterable(event.value)

                self._dispatch(
                    JoystickHatMotionEvent,
                    self.on_joystick_hat_motion,
                    (event.joy, event.hat, position),
                    scene=self, joystick=event.joy, hat=event.hat, position=position
                )
            elif event.type == pygame.KEYDOWN:
                self._dispatch(
                    KeyPressedEvent,
                    lambda key, mods: [subscriber(key, mods) for subscriber in self._subscribers_key_pressed],
                    (event.key, event.mod),
                    scene=self, key=event.key, mod=event.mod
                )
            elif event.type == pygame.KEYUP:
                self._dispatch(
                    KeyReleasedEvent,
                    self.on_key_released,
                    (event.key, event.mod),
                    scene=self, key=event.key, mod=event.mod
                )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [4, 5]:  # Skip scroll wheel events here
                    continue

                position: IntVector2 = IntVector2.from_iterable(event.pos)

                self._dispatch(
                    MousePressedEvent,
                    lambda pos, button: [subscriber(pos, button) for subscriber in self._subscribers_mouse_click],
                    (position, event.button),
                    scene=self, position=position, button=event.button
                )
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in [4, 5]:
                    continue

                position: IntVector2 = IntVector2.from_iterable(event.pos)

                self._dispatch(
                    MouseReleasedEvent,
                    self.on_mouse_released,
                    (position, event.button),
                    scene=self, position=position, button=event.button
                )
            elif event.type == pygame.MOUSEMOTION:
                position: IntVector2 = IntVector2.from_iterable(event.pos)
                relative: IntVector2 = IntVector2.from_iterable(event.rel)

                self._dispatch(
                    MouseMoveEvent,
                    lambda pos, rel_: [subscriber(pos, rel_) for subscriber in self._subscribers_mouse_move],
                    (position, relative),
                    scene=self, position=position, relative=relative
                )
            elif event.type == pygame.MOUSEWHEEL:
                position: IntVector2 = IntVector2.from_iterable(pygame.mouse.get_pos())

                self._dispatch(
                    MouseWheelScrollEvent,
                    self.on_mouse_wheel_scroll,
                    (position, event.y),
                    scene=self, position=position, amount=event.y
                )
            elif event.type == pygame.QUIT:
                self.engine._running = False
            elif event.type == pygame.USEREVENT:
                self._dispatch(
                    UserEvent,
                    self.on_user_event,
                    (event,),
                    scene=self, event=event
                )
            elif event.type == pygame.WINDOWCLOSE:
                self._dispatch(
                    WindowCloseEvent,
                    self.on_window_close,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWDISPLAYCHANGED:
                self._dispatch(
                    WindowDisplayChangedEvent,
                    self.on_window_display_changed,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWENTER:
                self._dispatch(
                    WindowMouseEnterEvent,
                    self.on_window_mouse_enter,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWFOCUSGAINED:
                self._dispatch(
                    WindowFocusGainedEvent,
                    self.on_window_focus_gained,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWFOCUSLOST:
                self._dispatch(
                    WindowFocusLostEvent,
                    self.on_window_focus_lost,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWHIDDEN:
                self._dispatch(
                    WindowHiddenEvent,
                    self.on_window_hidden,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWLEAVE:
                self._dispatch(
                    WindowMouseLeaveEvent,
                    self.on_window_mouse_leave,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWMAXIMIZED:
                self._dispatch(
                    WindowMaximizedEvent,
                    self.on_window_maximized,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWMINIMIZED:
                self._dispatch(
                    WindowMinimizedEvent,
                    self.on_window_minimized,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWMOVED:
                position: IntVector2 = IntVector2(event.x, event.y)

                self._dispatch(
                    WindowMovedEvent,
                    self.on_window_moved,
                    (position,),
                    scene=self, position=position
                )
            elif event.type == pygame.WINDOWRESIZED:
                size: IntVector2 = IntVector2(event.x, event.y)

                self._dispatch(
                    WindowResizeEvent,
                    self.on_window_resize,
                    (size,),
                    scene=self, size=size
                )
            elif event.type == pygame.WINDOWRESTORED:
                self._dispatch(
                    WindowRestoredEvent,
                    self.on_window_restored,
                    (),
                    scene=self
                )
            elif event.type == pygame.WINDOWSHOWN:
                self._dispatch(
                    WindowShownEvent,
                    self.on_window_shown,
                    (),
                    scene=self
                )
    
    def _check_keys(self) -> None:
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        mods: int = pygame.key.get_mods()

        for key in range(len(keys)):
            if not keys[key]:
                continue

            self._dispatch(KeyPressingEvent, self.on_key_pressing, (key, mods), scene=self, key=key, mods=mods)
    
    def _cleanup(self) -> None:
        self._dispatch(CleanupEvent, self.on_cleanup, (), scene=self)
    
    def _dispatch(self, event: type[Event], local_callback: Callable, args: tuple, **kwargs: dict) -> None:
        if self.engine._dispatch_plugin_event(ExecutionStep.BEFORE, event, **kwargs):
            return
        
        local_callback(*args)
        self.engine._dispatch_plugin_event(ExecutionStep.AFTER, event, **kwargs)

    def _first(self) -> None:
        self._dispatch(FirstEvent, lambda: ([event() for event in self._events_first], self.on_first()), (), scene=self)

        if not self.engine._game_loop_enabled:
            self.engine.step_game_loop()

    def _fixed_update(self) -> None:
        self._dispatch(FixedUpdateEvent, self.on_fixed_update, (), scene=self)

    def _render(self) -> None:
        if self.engine._pipeline == Pipeline.PYGAME:
            self.engine.screen.fill(self.engine.background_color.to_tuple())
        elif self.engine._pipeline == Pipeline.OPENGL:
            glClearColor(self.engine.background_color.nr, self.engine.background_color.ng, self.engine.background_color.nb, 1.0)

        self._dispatch(RenderEvent, lambda: (self.on_render(), self.frame.request_render()), (), scene=self)

        pygame.display.flip()
        
        target_frame_time: float = 1.0 / self.engine._set_fps if self.engine._set_fps > 0 else 0
        elapsed: float = time.perf_counter() - self.engine._last_frame_time
        sleep_time: float = target_frame_time - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)

    def _update(self) -> None:
        if not self._first_elapsed:
            self._first_elapsed = True
        
        self._dispatch(UpdateEvent, lambda: ([event() for event in self._events_update], self.on_update()), (), scene=self)
    
    def on_cleanup(self) -> None:
        '''
        Code below should be executed when the scene is being switched/cleaned up

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_fixed_update(self) -> None:
                ... # Update positions, text, etc.
        ```
        '''
        
        ...

    def on_init(self, *args, **kwargs) -> None:
        '''
        Code below should be executed after the instance has been initialized by the engine.
        
        Info
        ----
        This should be treated as any other `__init__` method.
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                # Initialize variables, logic, etc.
                ...
        ```
        '''

        ...

    def on_joystick_axis_motion(self, stick: int, axis: int, position: float) -> None:
        '''
        Code below should be executed when a joystick's axis moves
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_joystick_axis_motion(self, stick: int, axis: int, position: float) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joystick_button_down(self, stick: int, button: int) -> None:
        '''
        Code below should be executed when a joystick's button gets pressed
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_joystick_button_down(self, stick: int, button: int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joystick_button_up(self, stick: int, button: int) -> None:
        '''
        Code below should be executed when a joystick's button gets released
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_joystick_button_up(self, stick: int, button: int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joystick_device_added(self, device: int) -> None:
        '''
        Code below should be executed when a new joystick device is added
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_joystick_device_added(self, device: int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joystick_device_removed(self, device: int) -> None:
        '''
        Code below should be executed when an old joystick device is removed
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_joystick_device_removed(self, device: int) -> None:
                ...
        ```
        '''
        
        ...
    
    def on_joystick_hat_motion(self, stick: int, hat: int, position: IntVector2) -> None:
        '''
        Code below should be executed when a joystick's hat/D-Pad moves
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_joystick_hat_motion(self, stick: int, hat: int, position: wame.IntVector2) -> None:
                ...
        ```
        '''
        
        ...

    def on_key_pressed(self, key: int, mods: int) -> None:
        '''
        Code below should be executed when a key is pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_key_pressed(self, key: int, mods: int) -> None:
                ... # Pause game, display UI, etc.
        ```
        '''
        
        ...
    
    def on_key_pressing(self, key: int, mods: int) -> None:
        '''
        Code below should be executed when a key is being pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_key_pressing(self, key: int, mods: int) -> None:
                ... # Move forward, honk horn, etc.
        ```
        '''
        
        ...
    
    def on_key_released(self, key: int, mods: int) -> None:
        '''
        Code below should be executed when a key is released

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_key_released(self, key: int, mods: int) -> None:
                ... # Stop moving forward, etc.
        ```
        '''
        
        ...
    
    def on_mouse_move(self, mouse_position: IntVector2, relative: IntVector2) -> None:
        '''
        Code below should be executed when the mouse moves

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_mouse_move(self, mouse_position: wame.IntVector2, relative: wame.IntVector2) -> None:
                print(f"Mouse was moved {relative} amount @ {mouse_position}")
        ```
        '''
        
        ...
    
    def on_mouse_pressed(self, mouse_position: IntVector2, button: int) -> None:
        '''
        Code below should be executed when a mouse button was pressed

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_mouse_pressed(self, mouse_position: wame.IntVector2, button: int) -> None:
                ... # Start shooting, rotate character, etc.
        ```
        '''
        
        ...
    
    def on_mouse_released(self, mouse_position: IntVector2, button: int) -> None:
        '''
        Code below should be executed when a mouse button was released

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_mouse_released(self, mouse_position: wame.IntVector2, button: int) -> None:
                ... # Shoot arrow, stop shooting, etc.
        ```
        '''
        
        ...
    
    def on_mouse_wheel_scroll(self, mouse_position: IntVector2, amount: int) -> None:
        '''
        Code below should be executed when the scroll wheel moves

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_mouse_wheel_scroll(self, mouse_position: wame.IntVector2, amount: int) -> None:
                if amount > 0:
                    print(f"Scroll wheel moved up @ {mouse_position}!")
                else:
                    print(f"Scroll wheel moved down @ {mouse_position}!")
        ```
        '''

        ...

    def on_user_event(self, event: pygame.event.Event) -> None:
        '''
        Code below should be executed when a custom user event is called
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_user_event(self, event: pygame.event.Event) -> None:
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_window_mouse_leave(self) -> None:
                ...
        ```
        '''

        ...
    
    def on_window_moved(self, position: IntVector2) -> None:
        '''
        Code below should be executed when the window moves
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_window_moved(self, position: wame.IntVector2) -> None:
                ...
        ```
        '''

        ...

    def on_window_resize(self, size: IntVector2) -> None:
        '''
        Code below should be executed when the window is resized
        
        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_window_resize(self, size: wame.IntVector2) -> None:
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_window_shown(self) -> None:
                ...
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
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
            def on_init(self, *args, **kwargs) -> None:
                ...
            
            def on_update(self) -> None:
                ... # Update positions, text, etc.
        ```
        '''
        
        ...