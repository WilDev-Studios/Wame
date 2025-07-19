# Plugin Examples

## FPS Display

```python
from wame.plugins import *
from wame.ui import Text

import pygame

class FPSDisplayPlugin(Plugin):
    @on_event(LoadEvent)
    def on_load(self, _: LoadEvent) -> None:
        self.log_info("Plugin has successfully loaded")
    
    @on_event(UnloadEvent)
    def on_unload(self, _: UnloadEvent) -> None:
        self.log_info("Plugin has successfully unloaded")
    
    # don't initialize values like this in LoadEvent listeners, as `event.scene.frame` is `None` before the engine runs
    @on_event(FirstEvent, ExecutionStep.AFTER)
    def on_first(self, event: FirstEvent) -> None:
        self.fps_display: Text = Text(
            event.scene,
            event.scene.frame,
            text="FPS | 0", # default text until updated
            color=(255, 255, 255),
            font=pygame.font.SysFont("Ubuntu", 12),
            position=(4, 4) # top-left of screen
        )
    
    # important to be AFTER to render after the engine, to stay on top of the UI
    # keep in mind that fixed updates occur every interval that the game developer sets (default 60 times/second)
    @on_event(FixedUpdateEvent, ExecutionStep.AFTER)
    def on_fixed_update(self, event: FixedUpdateEvent) -> None:
        self.fps_display.text = f"FPS | {round(event.engine.fps)}"
```
