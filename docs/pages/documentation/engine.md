# Engine
The `Engine` is the starting point of any game made with the `wame` module.

## What is the Engine?
The `Engine` encapsulates all backend `Pygame` code that manages the window, rendering, audio, etc. of the game. All the `Engine` does it organize it into one object that is extremely intuitive and easy to use.

## How do I instantiate the Engine?
!!! note
    Keep in mind, the `Engine` is a singleton instance, so there can only ever be one instance per program.

This is how you create it:
```python
import wame

engine: wame.Engine = wame.Engine(...)
```
Simple right? Of course it is...however, we have to put some arguments into the constructor:

- `name` is the name of the window that should be created.
- `pipeline` is the rendering pipeline that the `Engine` should use when rendering elements to the screen (more on this in the `Pipeline` docs).
- There's other arguments like `size`, `display`, and `icon_filepath` that are all documented as well.

Here's how it's implemented:
```python
import wame

engine: wame.Engine = wame.Engine("Test Game", wame.Pipeline.PYGAME)
```
Great! This still won't work...let's find out why.

## Scene Registry
The `wame` `Engine` runs on `Scene`s, separated "code-spaces" that allow the organization of different parts of a game, within the game. Think of them as `Unity` `levels`.

The `Engine` requires all `Scene`s to be defined before runtime. This will be covered more in the `Scene` docs, but as of now this is a basic `Scene`:
```python
import wame

class TestScene(wame.Scene):
    def on_init(self, *args, **kwargs) -> None:
        ...
    
    def on_render(self) -> None:
        ...
    
    def on_update(self) -> None:
        ...

engine: wame.Engine = wame.Engine(...)
engine.register_scene("Test", TestScene)
```
Why do we register it?

- This is so the `Engine` can keep track of it, so when we switch to different scene during runtime, it knows which scene to switch to.
- However, to avoid circular imports, we track it by a unique name ("Test" in this case) so we can directly identify it without a direct reference.

This will not work still, because it's registered, but not set, so the `Engine` has no idea which `Scene` to start with, as you can register multiple scenes (more in `Scene` docs):
```python
engine: wame.Engine = wame.Engine(...)
engine.register_scene("Test", TestScene)
engine.set_scene("Test")

engine.start() # Make sure the engine is started, otherwise it won't work (duh)
```
This should run the window with just a black screen, assuming the color wasn't changed with `engine.set_background(...)`.
!!! warning
    Please note that since the game engine is an infinite running loop (assuming no interrupts), no code below the `.start()` line will execute until the `Engine` has quit.