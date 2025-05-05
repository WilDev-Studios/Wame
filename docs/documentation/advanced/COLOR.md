# Color Module
Easy access to different colors and functionality for them is frequently necessary for developing games. `Wame` has you covered here.

## RGB Objects
Defined in `wame.color.rgb`, the two `RGB` objects are:
- `ColorRGB`: Contains internal `r`, `g`, and `b` fields (`RED`, `GREEN`, `BLUE`). This makes color organization simple, and the `Engine` understands these.
- `ColorRGBA`: Similar to `ColorRGB`, but has an additional `a` (`ALPHA`/`TRANSPARENCY`) field.

`~ColorRGB` objects also contain internal `nr`, `ng`, and `nb` fields, which are normalized `RGB` values. These are necessary for objects that take normalized (`0-1`) `RGB` values rather than regular `RGB` values (`0-255`). `OpenGL` commonly uses normalized fields.

These objects aren't usually necessary for the developer to use, as it's provided internally by the `Engine`. The `Engine` also supports raw `tuple` values in contexts where `RGB` values are required.

## Values
Defined in `wame.color.values`:
- `RGB`: Contains commonly predefined `ColorRGB` objects, like `Black` (RGB: `0`, `0`, `0`), `White` (`255`, `255`, `255`), etc.

## Example Programs
```python
# Setting the background color of the `Engine`
color: ColorRGB = ColorRGB(0, 255, 255) # Cyan

engine: Engine = wame.Engine(...)
engine.set_background(color) # Takes a `ColorRGBA` object, but supports `ColorRGB` (converted natively)

print(color)
print(color.r, color.nb)
```
```
>>> R: 0, G: 255, B: 255
>>> 0, 1
```