# User Interface (UI)
Provides easy-to-use user-interface elements that are commonly used in games. `Wame` makes these easy to use and manipulate.

## Renderable
Defined in `wame.ui.renderable`:
- A `Renderable` is any object that subclasses the `Renderable` object.
- Each subclass of `Renderable` should have their own transform data (position, and most have size) as well as color attributes.
- These are always rendered under another `Renderable` (their "parent") that is first rendered by the `Scene`.
- Child `Renderables` inherit all transform attributes of their parent:
    - If the parent renderable starts at `0, 0` and it's size is `100, 100` pixels, then all children's max size will be `100` pixels or `1` scaled size.
    - Child `Renderables` can also have more children, which will further enhance this functionality.
    - For example, if the parent has a 100% width of the screen, and child #1 takes 50% of that total width, then the child of child #1 (child #2 in this case) would only take 25% of the total width if it's total width is 50%, and so on.
- Developers can define their own custom UI elements to fit their needs, so long as they subclass this `Renderable`. Many fields are required and promote the functionality `wame` aims to have.

## Frame
Defined in `wame.ui.frame`:
- A subclass of `Renderable`, the `Frame` is only a rectangular container that is primarily the "parent" of other objects.
- All `Scene`s come with a native `Frame`, enabled by default, under `Scene.frame`.
- These have their own color (can be completely transparent), position, and size attributes.
- Most objects will have the `Scene`s native `Frame` as their set parent.
- `Scene` `Frames` are always rendered after the `on_render()` method, as UI has to be rendered after the game.

## Button
Defined in `wame.ui.button`:
- A subclass of `Renderable`, the `Button` is identical to `Frame` but can have text and hover/click functionality/callbacks.
- Refer to the `Button` object itself for this functionality.

## Image
Defined in `wame.ui.image`:
- A subclass of `Renderable`, the `Image` is any pygame image loaded into this object.

## CheckboxInput
Defined in `wame.ui.input`:
- A subclass of `Renderable`, the `CheckboxInput` is basically a checkbox that has a position and size, and can be toggled `TRUE`/`FALSE`.

## TextInput
Defined in `wame.ui.input`:
- A subclass of `Renderable`, the `TextInput` is an input that becomes active when clicked in (as long as it's subscribed to in a `Scene`'s click listener).
- All characters typed while active will be sent into a predicate method defined by the developer that will return `TRUE`/`FALSE` as to whether the key input should be accepted and thus entered into the input.

## Text
Defined in `wame.ui.text`:
- A subclass of `Renderable`, the `Text` is a renderable text/font. It only has position and font size data internally, so size cannot be changed unless font size is changed as well.

## Example Programs
```python
# Disable the native `Scene` `Frame`
class ExampleScene(Scene):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

        self.frame.enabled = False

    def on_render(self) -> None:
        # Since the `Scene` `Frame` is automatically rendered if enabled, if not enabled you can do it manually (no idea why though)
        self.frame.ask_render() # ask_render() checks to see if it's enabled, and will render if so
        self.frame.render() # render() will force it to render, regardless if it's enabled
```
```python
# Make the `Scene` native `Frame` black
color: ColorRGB = ColorRGB(0, 0, 0)
self.frame.set_color(color)

# Note: This will only render black when the game runs, as the frame is rendered last, so everything will be black (that's why the frame is transparent by default)
```