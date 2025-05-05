# FPS Display
You want to have a text object that shows the player their own FPS (frames per second)? Look no further - `wame` makes this easy

## Program
```python
import pygame
import wame
import wame.ui as wui # Needed for the text object

class TutorialScene(wame.Scene):
    def __init__(self, engine: wame.Engine) -> None:
        super().__init__(engine) # All basic setup

        #                                    Parent       Text       RGB Color                  Font
        self.fps_text: wui.Text = wui.Text(self.frame, "FPS | 0", (125, 125, 125), pygame.font.SysFont("Ubuntu", 12))
        self.fps_text.set_pixel_position((5, 5)) # Sets the top-left of the text at `5, 5` on the screen
    
    def on_render(self) -> None:
        ...
    
    def on_update(self) -> None:
        self.fps_text.set_text(f"FPS | {round(self.engine.fps)}")

engine: wame.Engine = wame.Engine("FPS Display Tutorial", wame.Pipeline.PYGAME)
engine.register_scene("Tutorial", TutorialScene)
engine.set_scene("Tutorial")

engine.start()
```
You may be asking why there isn't a specific `draw`/`render` call for the `self.fps_text` object...good catch:
- This isn't specifically called because the `fps_text`'s parent is `self.frame`, as you can see when it's instantiated
- This is because the `UI` system of `wame` is rendered after the `on_render` method is called
- Although `self.fps_text` isn't directly rendered itself, `self.frame` renders each frame, thus it's children as well (including `self.fps_text`)

However, if you want a more specific approach without using the `self.frame` (to be completely unrelated, for some reason):
```python
import pygame
import wame
import wame.ui as wui

class TutorialScene(wame.Scene):
    def __init__(self, engine: wame.Engine) -> None:
        super().__init__(engine)

        self.fps_text: wui.Text = wui.Text(self.frame, "FPS | 0", (125, 125, 125), pygame.font.SysFont("Ubuntu", 12))
        self.fps_text.set_pixel_position((5, 5))

        self.frame.enabled = False
    
    def on_render(self) -> None:
        self.fps_text.render()
    
    def on_update(self) -> None:
        self.fps_text.set_text(f"FPS | {round(self.engine.fps)}")

engine: wame.Engine = wame.Engine("FPS Display Tutorial", wame.Pipeline.PYGAME)
engine.register_scene("Tutorial", TutorialScene)
engine.set_scene("Tutorial")

engine.start()
```
The example above works completely fine as well, as it disabled it's parent, `self.frame`, but we still demand it's rendering in `on_render` with `self.fps_text.render()`

However, there's still one more thing we'd like to point out. When rendering `UI` objects such as `self.fps_text`, it's a `Renderable` subclass, so it also has a `.enabled` state as well:
- This allows `self.fps_text` to be disabled during runtime, in case a key is pressed, etc.
- Using `.render()` on `UI` objects **MAKES** the object render, regardless if it's enabled/disabled
- In order to render the `UI` object if it's enabled, use `.ask_render()` so it checks to be sure if it can be rendered or not
```python
import pygame
import wame
import wame.ui as wui

class TutorialScene(wame.Scene):
    def __init__(self, engine: wame.Engine) -> None:
        super().__init__(engine)

        self.fps_text: wui.Text = wui.Text(self.frame, "FPS | 0", (125, 125, 125), pygame.font.SysFont("Ubuntu", 12))
        self.fps_text.set_pixel_position((5, 5))

        self.frame.enabled = False
    
    def on_render(self) -> None:
        self.fps_text.ask_render()
    
    def on_update(self) -> None:
        self.fps_text.set_text(f"FPS | {round(self.engine.fps)}")

engine: wame.Engine = wame.Engine("FPS Display Tutorial", wame.Pipeline.PYGAME)
engine.register_scene("Tutorial", TutorialScene)
engine.set_scene("Tutorial")

engine.start()
```
This example would be completely accurate if you wanted to disable the `self.frame`, because now if you disabled `self.fps_text` it wouldn't render unless you re-enable it during runtime.