# Colors
## Overview
This module defines two primary classes for representing and manipulating colors in RGB and RGBA formats:

- `ColorRGB`: A basic color representation using `red`, `green`, and `blue` channels.
- `ColorRGB`: An extended color representation that includes an `alpha` (transparency) channel.

Both classes offer built-in type safety, format conversion, normalization, and conventient interoperability with Python data structures and `NumPy`.

!!! success "Compatibility"
    - Fully compatible with `NumPy` arrays and Python `tuple`/`list` types for input/output.
    - Intended for use in both scripting and performance-sensitive applications.

## `ColorRGB`
Represents a color defined by red, green, and blue components (`0`-`255` each). Provides various utilities for converting and interacting with color values.

### Features
- Type-safe construction with automatic validation of RGB values.
- Normalization support via `.nr`, `.ng`, and `.nb` properties for values between `0`-`1`.
- Interoperable access using indexing (`[0]` for red, `[1]` for green, and `[2]` for blue), iteration, and tuple unpacking.
- Color format conversion:
    - `hex()`: RGB to hexadecimal string (`#000000`).
    - `hsl()`: RGB to HSL tuple.
    - `hsv()`: RGB to HSV tuple.
    - `int()`: RGB to packed 24-bit integer.
- Mutability through both item-style (`color[0] = 100`) and attribute-style (`color.r = 100`) assignment.
- Representation utilities:
    - `__str__`, `__repr__` support.
    - Custom `__format__` strings: `"hex"`, `"hsl"`, `"hsv"`, `"int"`, and `"tuple"`.

### Examples
```python
color = ColorRGB(255, 100, 50)
print(color.hex())              # "#FF6432"
print(color.hsv())              # (0.04..., 0.80..., 1.0)
r, g, b = color                 # Unpacks to RGB values
```

## `ColorRGBA`
Represents a color defined by red, green, and blue components (`0`-`255` each) and an alpha field (`0`-`1`). Provides various utilities for converting and interacting with color values.

### Features
- Type-safe construction with automatic validation of RGBA values.
- Normalization support via `.nr`, `.ng`, and `.nb` properties for values between `0`-`1`.
- Interoperable access using indexing (`[0]` for red, `[1]` for green, `[2]` for blue, and `[3]` for alpha), iteration, and tuple unpacking.
- Color format conversion:
    - `hex()`: RGB to hexadecimal string (`#000000`).
    - `hsla()`: RGB to HSLA tuple.
    - `hsva()`: RGB to HSVA tuple.
    - `int()`: RGB to packed 32-bit integer.
- Mutability through both item-style (`color[0] = 100`) and attribute-style (`color.r = 100`) assignment.
- Representation utilities:
    - `__str__`, `__repr__` support.
    - Custom `__format__` strings: `"hex"`, `"hsla"`, `"hsva"`, `"int"`, and `"tuple"`.

### Examples
```python
color = ColorRGBA(255, 100, 50, 0.5)
print(color.hex())              # "#FF643280"
print(color.hsva())              # (0.04..., 0.80..., 1.0, 0.5)
r, g, b, a = color                 # Unpacks to RGBA values
```