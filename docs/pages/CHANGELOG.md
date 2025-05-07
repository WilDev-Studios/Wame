# Changelog
- **NOTE**: `Wame`'s development status is still in `Beta`. Many breaking changes will occur until our stable `1.0.0` release.

## Version 0.5.0 (STAGING - Prerelease)
This is here to keep track of all changes before the release - to address expectations.

### Breaking Changes
- Removal of `Scene` `on_quit` method (as `on_cleanup` is used here).
- Removal of `TABBED_FPS` `Settings` attribute.
- `Engine` constructor parameter `icon_filepath` changed to `icon` and instead takes a `pygame.Surface` than a `str` filepath.

### Additions
- Provided complete documentation to all objects not documented previously.
- Joystick support for console devices, like controllers.
- Custom user events as `Pygame` allows.
- Additional `Scene` event dispatch methods:
    - `on_joy_axis_motion`
    - `on_joy_button_down`
    - `on_joy_button_up`
    - `on_joy_device_added`
    - `on_joy_device_removed`
    - `on_joy_hat_motion`
    - `on_user_event`
    - `on_window_close`
    - `on_window_display_changed`
    - `on_window_focus_gained`
    - `on_window_focus_lost`
    - `on_window_hidden`
    - `on_window_maximized`
    - `on_window_minimized`
    - `on_window_mouse_enter`
    - `on_window_mouse_leave`
    - `on_window_moved`
    - `on_window_resize`
    - `on_window_restored`
    - `on_window_shown`
- New `Interval` object under the `wame.common` module. Contains commonly used time durations (useful for `Engine.set_update_interval` with fixed updates).
- New `Scene` `on_fixed_update` that updates every configured interval, default `60Hz` (60 times/second). Edit with `Engine`.`set_update_interval`.
- New `Engine` constructor `settings_persistent` parameter. Allows developers to custom save/load game settings if they desire.

### Fixes
- Typos in existed documentation has been fixed.
- False errors raised when updating runtime `Engine` attributes (`Pipeline` and *`update_interval` values) before a `Scene` was ran.
- Public `Engine` attributes now cannot be edited, only referenced.
- Incorrect error types in documentation `Raises` sections.
- Referenced errors in documentation never had an actual error raise possible.
- `IntVector3` `cross` can no longer take `FloatVector3` values.
- `Settings` updated a local screen object instead of the `Engine`.

## Version 0.4.0
Released `May 5th, 2025`

### Breaking Changes
- Removed the `settingsOverride` parameter in the `Engine` constructor.
- Renamed the `Renderer` class to `Pipeline` to make it more understandable/readable.
- Complete rewrite of the UI system:
    - `Frame` object: Container for all UI objects - All `Scene`s have a native `Frame` under `Scene.frame`.
    - Position and sizes can now be absolute (pixel-based) or relatively sized (scaled by percentage).
    - Children of `Frame`s inherit the `Frame`'s size and position.
    - Any subclass of the `Renderable` can be enabled/disabled.
    - When rendering objects manually instead of through a parent->children render like `Frame`, use `ask_render()` not `render()` (to permit enable/disable behavior).
- UI system can be found in the `wame.ui` module.
- Vectors can be found in the `wame.vector` module.
- `Font` objects have been removed. Use `Pygame`'s `font` module.
- `OPENGL` `Pipeline` is now only flagged in window instantiation and background colors in the `Engine`. All other `OpenGL` code is managed by the user (unless in `ui` module).
- `Engine._scene` was renamed to `.scene` to promote external access.
- `Scene.on_start()` was removed. Please only use `Scene.on_first()`.
- `Scene` `on_update()` and `on_render()` methods are now required.
- All object parameter names are now using `snake_case` rather than `camelCase` (by `Python` convention).

### Additions
- New `FloatVector2` object.
- Ability to pass in data between scenes when switching them using the `Engine` `set_scene` method.
- Colors have been added in the `wame.color` module.
- All vector objects can now be compared to each other to see if their values match natively.
- All vector objects are now hashable.
- The rendering pipeline can now be switched during engine runtime (not changeable during gameloop, however), between scene swaps, etc.
- New `wame.common` module with some commonly necessary functions and objects:
    - `Key` objects and checkers.
- All `Scene`s must define `on_render` and `on_update` for the `Scene` to be instantiated.
- Mouse button argument added when `Scene` dispatches `on_mouse_pressed` and `on_mouse_released` events.
- `Engine` is now a singleton object as now only one instance can be created.
- `Engine.pipeline` is now added as a property, so you can check the pipeline during runtime if necessary.
- Python `3.7+` is now supported, instead of `3.10+`.

### Fixes
- Never called a scene's `on_first` event when the scene was switched to after another scene was already loaded.
- Any arguments requiring a `wame` vector object should now be able to accept `tuple` objects.
- `Engine` `set_mouse_visible` and `set_mouse_locked` never updated the actual state of the mouse's visibility or grab status.
- `Engine` will no longer automatically clear the console on startup.
- `max_fps` `Setting` wasn't updating the `Engine`'s set FPS.
- `Engine().scene` wasn't set when `on_first` was called.

## Version 0.3.0
Released `October 13th, 2024`

No changelog recorded.

## Version 0.2.0
Released `August 28th, 2024`

No changelog recorded.

## Version 0.1.0
Released `July 11th, 2024`

No changelog recorded.

## Version 0.0.1 (YANKED)
Released `July 11th, 2024`

No changelog recorded - Served as a PyPI module test version with early source code

## Version 0.0.1.dev2 (PRERELEASE)
Released `July 11th, 2024`

No changelog recorded - Served as a PyPI module test version with early source code

## Version 0.0.1.dev1 (PRERELEASE)
Released `July 11th, 2024`

No changelog recorded - Served as a PyPI module test version with early source code