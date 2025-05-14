# Scene
On-demand context switching and organized events and calls - all features and elements of `wame`'s game engine.

## Scene Object
Defined in `wame.scene`:
- `Scene`s are defined by `wame`, with all methods and attributes already instantiated internally.
- In order to successfully use `Scene`, you have to subclass it into a custom `~Scene` of your own, and register it to the engine to use.
- Most of that functionality is featured in the `Engine` documentation, but this will be more in depth.
- If you'd like to use fixed updates like `Unreal` and `Unity` game engines, use `on_fixed_update` as well as:
    - `Interval`, an object containing very common `?/sec` interval values, like `30Hz`, `60Hz`, `120Hz`, etc.
    - Use with `Engine`.`set_update_interval` (which sets the fixed update interval).

## How Scenes Work
- The `Engine` only runs the game loop in the background, with enhanced functionality, but the `Scene` takes care of the rest.
- The `Scene` has internal methods that handle raw calls from the `Engine` that further dispatches those events into the known methods that we use inside of our scenes.
- Not only does this simplify the game loop, it declutters different game "fields", like a main menu and a level, for example.
- Scenes can be registered one-by-one, in a batch, or from a folder. Explained below.

## Example Programs
```python
# Creating a Scene
class TestScene(wame.Scene): # You MUST subclass `wame.Scene`.
    def __init__(self, engine: wame.Engine) -> None: # The engine will internally instantiate this `Scene` instance, and will pass itself into the constructor for reference purposes.
        super().__init__(engine) # Instantiates the original scene, methods, and attributes

    # MUST be defined - This method will be called when it's time to render everything in the game loop
    def on_render(self) -> None:
        ...
    
    # MUST be defined - This method will be called when it's time to update all logic and objects in the game loop
    def on_update(self) -> None:
        ...
```
```python
# Registering the Scene
engine: wame.Engine = wame.Engine(...)
engine.register_scene("Test", TestScene) # You should always begin the `Scene` subclass' name with the name you want to refer it to: "Test" in this case belongs to `TestScene`
engine.set_scene("Test") # Use the custom ID, as you cannot use a direct reference to the `TestScene` object without circular references when multiple scenes are used

engine.start()
```
The example above outlines the following process in the background, allowing the game to run:
- Instantiating the `Engine` creates the game loop and all backend logic
- Registering the `TestScene` tells the `Engine` to instantiate a `TestScene` instance when it sets the scene to "Test"
- Setting the `Engine`'s scene to "Test" tells the `Engine` to lookup a scene under the "Test" ID, which is `TestScene` in this case, and instantiate it and close the previous scene (if any)
- After creating the game loop, registering and setting the scene to start, then run the `Engine`'s backend game loop, thus running the game
```python
# Registering Multiple Scenes by Reference
engine: wame.Engine = wame.Engine(...)
engine.register_scenes({
    "Example1", Example1Scene,
    "Example2", Example2Scene,
    "Example3", Example3Scene
    # etc.
})

engine.start()
```
```python
# Registering Scenes from Folder (No Reference)
engine: wame.Engine = wame.Engine(...)
engine.register_scenes_from_folder("scenes")
engine.set_scene("Main")

engine.start()
```
In the example above:
- We try to register all scenes provided in all files from the `scenes` folder in our current directory
- All `wame.Scene` subclasses MUST begin with a unique name like "Test" for `TestScene`, "Example1" for `Example1Scene`, etc.
- When `register_scenes_from_folder` looks through all subclasses of `wame.Scene`, it creates the custom ID from the beginning words up to `Scene` in the name of the subclass. Creating, for example:
    - `MainMenuScene`'s unique ID would be "MainMenu", thus needing `engine.set_scene("MainMenu")` to switch to that scene
    - `Level1Scene`'s unique ID would be "Level1", thus needing `engine.set_scene("Level1")` to switch to that scene
    - etc.
    
So in the example above, there has to exist a `wame.Scene` subclass called `MainScene` so the `engine.set_scene("Main")` is referencing an actual scene subclass instance. Otherwise, errors will be raised.