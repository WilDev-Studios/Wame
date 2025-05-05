# Toggleable FPS Display
You already have a FPS display but want to toggle it? Look no further - `wame` makes this easy
- Desired that we toggle it when `F1` is pressed, for example
- FPS text is disabled by default

## Program
```python
# Assuming a basic FPS text display is already made
import pygame
import wame
import wame.ui as wui

class TutorialScene(wame.Scene):
    def __init__(self, engine: wame.Engine) -> None:
        super().__init__(engine)

        self.fps_text: wui.Text = wui.Text(self.frame, "FPS | 0", (125, 125, 125), pygame.font.SysFont("Ubuntu", 12))
        self.fps_text.set_pixel_position((5, 5))
        self.fps_text.enabled = False # Default to disabled
    
    def on_key_pressed(self, key: int, mods: int) -> None:
        if key == pygame.K_F1: # If `F1` key is pressed
            self.fps_text.enabled = not self.fps_text.enabled # Enable/Disable it

    def on_render(self) -> None:
        ... # Already automatically rendered from it's parent, `self.frame`
    
    def on_update(self) -> None:
        self.fps_text.set_text(f"FPS | {round(self.engine.fps)}") # Update text each frame

engine: wame.Engine = wame.Engine("Toggleable FPS Display Tutorial", wame.Pipeline.PYGAME)
engine.register_scene("Tutorial", TutorialScene)
engine.set_scene("Tutorial")

engine.start()
```