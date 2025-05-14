# Passing Data Between Scenes
If you have objects, instances, or configuration data you'd like to pass between scenes, look no further - `wame` makes this easy

## Breakdown
- `Engine` allows to pass `args` in the `set_scene` function call. These `args` are where you'd pass in your positional data.
- Each `~Scene` constructor requires `self`, `engine`, and your positional `args` (if any).
- When you switch scenes, either from the first `set_scene` call to begin you game or if switching scenes during runtime, this will work.
- This is particularly helpful if your scenes are separated into different files.

## Program
```python
# Passing Data to First Scene
import json
import wame

class TutorialScene(wame.Scene):
    def __init__(self, engine: wame.Engine, config: dict[str, str]) -> None:
        super().__init__(engine)

        self.config: dict[str, str] = config
        # Do whatever you need with config (or any other object you pass)

    ...

with open("config.json") as file:
    config: dict[str, str] = json.load(file)

engine: wame.Engine = wame.Engine("Passing Data Tutorial", wame.Pipeline.PYGAME)
engine.register_scene("Tutorial", TutorialScene)
engine.set_scene("Tutorial", config) # Pass the `config` object as a positional argument

engine.start()
```
```python
# Passing Data Between Scenes
import json
import pygame
import wame

class Tutorial1Scene(wame.Scene):
    def __init__(self, engine: wame.Engine, config: dict[str, str]) -> None:
        super().__init__(engine)

        self.config: dict[str, str] = config

    def on_key_pressed(self, key: int, mods: int) -> None:
        if key == pygame.K_ESCAPE: # Switch scenes when ESCAPE is pressed
            self.engine.set_scene("Tutorial2", self.config) # Pass `config` to 2nd scene

    ...

class Tutorial2Scene(wame.Scene):
    def __init__(self, engine: wame.Engine, config: dict[str, str]) -> None:
        super().__init__(engine)

        self.config: dict[str, str] = config # Passed from first scene

    ...

with open("config.json") as file:
    config: dict[str, str] = json.load(file)

engine: wame.Engine = wame.Engine("Passing Data Tutorial", wame.Pipeline.PYGAME)
engine.register_scenes({
    "Tutorial1": Tutorial1Scene,
    "TUtorial2": Tutorial2Scene
})
engine.set_scene("Tutorial1", config) # Pass the `config` object as a positional argument

engine.start()
```