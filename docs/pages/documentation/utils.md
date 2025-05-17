# Utilities
## Overview
This module defines methods, classes, and objects typically used frequently in game/application development.

- `Keys`: Provides a mapping of all common `WASD` keyboard keys (`KEYCODE: MODIFIERS`) and various helper functions to determine what type of character(s) was/were typed.
- `Tween`: Internalized functionality used in the animation of objects.

## Keys
Provides most functionality required for usual keyboard-related input.

### Features
- Well-documented mappings and methods.
- `KEYS`: A comprehensive key-modifier mapping that provides a letter that corresponds to general `Pygame` input.
- Helper functions:
    - `is_char`: If the key(s) pressed equate to any character on the `WASD` keyboard.
    - `is_letter`: If they equate to any letter.
    - `is_lower`: If they equate to any lowercase letter.
    - `is_number`: If they equate to any number.
    - `is_symbol`: If they equate to any symbol.
    - `is_upper`: If they equate to any uppercase letter.

### Examples
```python
key: str = KEYS[(keycode, modifiers)]
if KEYS[(keycode, modifiers)] == 'a': ...
return KEYS[(keycode, modifiers)]
if (keycode, modifiers) in KEYS: ...
```

## Tween
Animation/tweening helper class to assist developers in smoothly move objects.

### Features
- Framerate-independent animation.
- Type-safe methods and strict annotations.
- Heavily-optimized internal arithmetic for heavy, tight game loops.
- Automatic integration with `Scene` for ease-of-use and finishing event dispatching.
- Support for:
    - `pygame.Rect` with `rect`.
    - `ColorRGB` with `color_rgb`.
    - `ColorRGBA` with `color_rgba`.
- `Easing` bundling class for defined, handy easing functions:
    - Bounce: `BOUNCE_IN`, `BOUNCE_OUT`, `BOUNCE_IN_OUT`.
    - Cubic: `CUBIC_IN`, `CUBIC_OUT`, `CUBIC_INT_OUT`.
    - Linear with `LINEAR`.
    - Quad: `QUAD_IN`, `QUAD_OUT`, `QUAD_IN_OUT`.
    - Quartic: `QUARTIC_IN`, `QUARTIC_OUT`, `QUARTIC_IN_OUT`.
    - Quintic: `QUINTIC_IN`, `QUINTIC_OUT`, `QUINTIC_IN_OUT`.
    - Sine: `SINE_IN`, `SINE_OUT`, `SINE_IN_OUT`.

### Examples
```python
# Move and resize rectangle over 10 seconds
rect = pygame.Rect(0, 0, 100, 100)
destination = pygame.Rect(100, 100, 500, 500) # Move to 100, 100 and resize x5
tween.rect(rect, destination, 10.0, Easing.LINEAR) # 10s, linear easing
```