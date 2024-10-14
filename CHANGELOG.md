# Changelog
- Versions `0.0.1+dev1` -> `0.3.0`
- **NOTE**: `Wame`'s development status is still in `Beta`. Many breaking changes may occur until our stable `1.0.0` release.

## Breaking Changes
- Removed the `Engine` `set_renderer` method and incorporated it into the `Engine` constructor.

## Added:
- Mouse movement amount (from previous to current) passed into scene `on_mouse_move` events.
- Text now able to render with OpenGL pipeline.
- More comprehensible error messages instead of Python-provided default errors.
- Vector objects are now compatible with numpy (math and conversion).
- Configurable background color using the engine's `set_background` method.
- Option to lock the cursor (`Engine` `set_mouse_locked` method).
- Option to hide the cursor (`Engine` `set_mouse_visible` method).
- Included engine `screen` property into active scenes for easy access.
- Transform attributes added to the `Button` object through it's `rect`.
- Adjusted `set_...` methods in `Text` objects to return the instance of the `Text` object to allow call-chaining.
- Added `mods` parameter to `Scene` `on_key_...` events.
- Added `add_color_option`, `add_font_option`, and `set_font` methods to the `Text` object to allow on-the-go font and color changes.
- Added a separate `on_render` event to `Scene` from `on_update` to maintain standard development practice.
- Added a new `settingsOverride` parameter to the `Engine` constructor to allow program-mandated settings that don't allow setting persistence.
- New `TextInput` class that allows for text manipulation. This is still being worked on, but a lot can still be done with it thus far.
- New `draw` module allowing for easy `wame`-sided draw calls similar to `pygame`'s. Completely optional but recommended for certain draws.

## Fixed:
- Keys being pressed weren't being dispatched correctly through scene `on_key_pressing` events.
- Position of mouse wasn't being handled properly in scene `on_mouse_scroll` events.
- Button -> engine reference errors.
- `Scene` `on_mouse_pressed` being called when scroll wheel moves.
