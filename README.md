# Wame
Pygame Wrapper to Create and Manage Games Easily
- Programmed in `CPython 3.12.4`

## What is Wame?
Wame was created as a backend Pygame wrapper, where all backend (and tedious) code is left in the background. This allows for events to be dispatched in specific event methods rather than in a messy manner like default Pygame and most other engine program loops.
This is primarily because handling the game backend and frontend in a singular file (or a couple) can be an eyesore, and Wame fixes this issue.

## What are Wame's features?
- Encapsulates Pygame's backend game programming
- Dispatches and calls methods needed to render and update game code, while executing events in a structured manner
- Allows on-demand scene switching (more about this later)
- Provides basic objects like font rendering (text), drawing, buttons, etc. (a pain to always make on many projects)

## How do I use Wame?
- Install `Wame` via `PyPI`: `pip install wame-engine`
- Import it into your program, and follow the steps below:
```python
import wame

engine:wame.Engine = wame.Engine(...)
engine.start()
```

This, of course, is an extremely simple setup, and won't do you anything except give you an internal error for no scene being registered/set.

## How do I create a scene and use it in my engine?
`Wame` allows for many ways of registering a scene. A scene in `Wame` is much like any other game engine, with code that can be completely independent of any other code in another scene. This is the same with objects and properties, kind of like 3D game engines (but of course we manage all of those instances manually, us programmers). Creating a scene is very simple, actually. All you need to do is subclass the `Scene` object provided by `Wame`, and the scene will automatically handle all backend code for you, abstracting the things necessary for game/UI development:
```python
import wame

class ExampleScene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

engine:wame.Engine = wame.Engine(...)
engine.start()
```
Doing this creates a scene, and doesn't do much else. To hook this scene into the Engine where it can actually be used, we need to register it with the engine and tell it to use it. This is how:
```python
import wame

class ExampleScene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

engine:wame.Engine = wame.Engine(...)
engine.register_scene("Example", ExampleScene)
engine.set_scene("Example")
engine.start()
```
Why do we have to register the scene and then set it using a unique name? This allows for us to have multiple scenes that can be switched instantaneously and without stutter, without a direct reference to the scene we would like to switch to (avoiding circular imports).
Doing this also allows us to switch the scene in the middle of our current scene, i.e. if somebody clicks a button, we can set the callback to switch the scene from a main menu to a level.

However, this will still not run, as the constructor for `wame.Engine()` needs some arguments. Of these that is important is the `name` and `renderer`. `Wame` uses both `Pygame` and `OpenGL` as it's rendering pipelines, but `OpenGL` is still having issues that we are working on, so `Pygame` will be our renderer for now. `name` is just the name of the window that `Wame` will open. `Wame` creates applications in fullscreen by default (can be changed using the `size` parameter. `(0, 0)` is default). Let's implement this:
```python
import wame

class ExampleScene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

engine:wame.Engine = wame.Engine("My Example Game", wame.Renderer.PYGAME)
engine.register_scene("Example", ExampleScene)
engine.set_scene("Example")
engine.start()
```
This, right now, will open a black, full-functioning game window. You can't do much with it until we start manipulating the scene.
How can we do this? Well, scene's have built-in methods for handling game code. One of the most popular ways of doing this is inside of a `on_update` and `on_render` method, where `on_update` is where game logic is updated (like positions, text content, etc.) and `on_render` is where everything is drawn to the screen. This is how these simple methods can be introduced:
```python
import wame

class ExampleScene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

  def on_render(self) -> None:
    ... # Render objects, text, UI elements, etc.

  def on_update(self) -> None:
    ... # Update game logic, text content, etc.

engine:wame.Engine = wame.Engine("My Example Game", wame.Renderer.PYGAME)
engine.register_scene("Example", ExampleScene)
engine.set_scene("Example")
engine.start()
```
This still doesn't do anything...so let's make a basic FPS text counter using `Wame`'s `Text` class:
```python
import wame

class ExampleScene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

    self.fps_text:wame.Text = wame.Text(self, "FPS | 0", wame.SysFont("Ubuntu", 12), (255, 255, 255)) # The font can be any pygame font
    self.fps_text.set_position((5, 5)) # Starts from top-left to bottom-right of the screen

  def on_render(self) -> None:
    self.fps_text.render() # Renders the text every frame after `on_update` is called

  def on_update(self) -> None:
    self.fps_text.set_text(f"FPS | {round(self.engine.fps)}") # Sets the text of the `fps_text` object before being rendered

engine:wame.Engine = wame.Engine("My Example Game", wame.Renderer.PYGAME)
engine.register_scene("Example", ExampleScene)
engine.set_scene("Example")
engine.start()
```
This, in theory, should run without issue, and you should see `FPS | XXX` at the top-left of your screen.

## How can I create multiple scenes and switch between them?
Great question! This is where `Wame` shines above the rest. Let's create two scenes and register them really quick.

```python
import wame

class Ex1Scene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

    self.text:wame.Text = wame.Text(self, "Hello there!", wame.SysFont("Ubuntu", 100), (255, 255, 255))
    self.text.set_position((100, 100))

  def on_render(self) -> None:
    self.text.render()

class Ex2Scene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

    self.text:wame.Text = wame.Text(self, "Hey there!", wame.SysFont("Ubuntu", 100), (255, 255, 255))
    self.text.set_position((100, 100))

  def on_render(self) -> None:
    self.text.render()

engine:wame.Engine = wame.Engine("My Example Game", wame.Renderer.PYGAME)
engine.register_scene("1", Ex1Scene)
engine.register_scene("2", Ex2Scene)
engine.set_scene("1")
engine.start()
```
This registers both scenes and sets the engine to only render the 1st one. The 1st will render `Hello there!` while the 2nd will render `Hey there!`. So far, we can only see `Hello there!` when this is run because the engine is set to render the 1st, not the 2nd scene. To change this, we can subscribe to an event (whatever works for you) to allow us to do something to change to the other scene. Let's change the scene when the `ESC` (escape) key is pressed. Here's how:
```python
import pygame
import wame

class Ex1Scene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

    self.text:wame.Text = wame.Text(self, "Hello there!", wame.SysFont("Ubuntu", 100), (255, 255, 255))
    self.text.set_position((100, 100))

  def on_key_pressed(self, key:int, mods:int):
    match key:
      case pygame.K_ESCAPE:
        self.engine.set_scene("2")

  def on_render(self) -> None:
    self.text.render()

class Ex2Scene(wame.Scene):
  def __init__(self, engine) -> None:
    super().__init__(engine)

    self.text:wame.Text = wame.Text(self, "Hey there!", wame.SysFont("Ubuntu", 100), (255, 255, 255))
    self.text.set_position((100, 100))

  def on_key_pressed(self, key:int, mods:int):
    match key:
      case pygame.K_ESCAPE:
        self.engine.set_scene("1")

  def on_render(self) -> None:
    self.text.render()

engine:wame.Engine = wame.Engine("My Example Game", wame.Renderer.PYGAME)
engine.register_scene("1", Ex1Scene)
engine.register_scene("2", Ex2Scene)
engine.set_scene("1")
engine.start()
```
This code should run perfectly fine, and when we press the `ESC` key, it should swap to the other scene, and vice-versa. This is what scenes are for - to allow multiple scenes to be switched between on command and with ease.
But there has to be a better way to manage the scenes so our file isn't so messy, right? Of course!

## What are the different ways I can create and register scenes?
Glad you asked. There is currently 2 (3 depending on how you look at it) ways you can register scenes. Here are the current ways to do so:
- `engine.register_scene(...)`
- `engine.register_scenes(...)`
- `engine.register_scenes_from_folder`
<br>We already showed how to use `register_scene`, but what is `register_scenes`?
It's essentially the same as multiple `register_scene` calls in one...just pass a dictionary:
```python
engine.register_scene("1", Ex1Scene)
engine.register_scene("2", Ex2Scene)

# This is the same as below:

engine.register_scenes({
    "1": Ex1Scene,
    "2": Ex2Scene
})
```
So what is `register_scenes_from_folder` then? It allows multiple scenes to be placed into different files, and automatically imported into the engine. Here's how:
```python
import wame

engine:wame.Engine = wame.Engine("Example Application", wame.Renderer.PYGAME)
engine.register_scenes_from_folder("scenes")
engine.set_scene("Example1")

engine.start()
```
```python
# scenes/example1.py
import wame

class Example1Scene(wame.Scene):
  ...
```
```python
# scenes/example2.py
import wame

class Example2Scene(wame.Scene):
  ...
```
As you can see, both scenes in both files have been automatically imported through the `register_scenes_from_folder` method. However, the engine automatically registers these scene's unique names as the name of the scene subclass object (just with `Scene` at the end removed). Subclassed scenes using this method must end in `Scene` to avoid imports of classes meant to be localized to that file specifically.


























