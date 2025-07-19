# Plugin Definition

To get started in making a plugin, understand the following:

- Plugins are automatically imported into the `Engine` before startup.
- There are different types of `Event`s:
    1. `LifetimeEvent`: Dispatched when the lifetime of your plugin changes (`LoadEvent`, `UnloadEvent`, etc.).
    2. `CancellableEvent`: Any type of event that can be cancelled and therefore prevent any further logic from occurring.
        - `SceneEvent`: Dispatched when any event occurs within any `Scene` (`KeyPressedEvent`, `MouseScrollEvent`, etc.).
- Each event "listener"/handler has a specific time in which it can fire - controlled by `ExecutionStep`:
    1. `BEFORE`: Fired before the `Engine`/`Scene`/developer even sees the event. If you cancel the event, the `Engine`/`Scene`/developer can't handle the event.
    2. `AFTER`: Fired after the `Engine`/`Scene`/developer sees/handles the event. If the event is cancelled before you handle it, you won't see the event.
    3. `ExecutionStep`.`BEFORE`/`AFTER` **does not** affect `LifetimeEvent` events.
- The normal game loop within `Engine` and `Scene` cannot be cancelled, i.e. `LifetimeEvent` or `EngineEvent` (not implemented, yet).
- Each `Event` has access to an external `engine` attribute, which is a direct reference to the running `Engine`.
- Each `SceneEvent` has access to an external `scene` attribute, which is a direct reference to the running `Scene` controlled by the `Engine`.
- Every type of `Event` has external attributes accessible depending on the context in which the event was dispatched (`key` and `mods` for a `KeyPressedEvent`, etc.).

## Getting Started

Define an inherited class of `Plugin` from `wame.plugins`. Give it a load/unload handler:

```python
from wame.plugins import * # Has all events and objects necessary for plugin development

class MyPlugin(Plugin):
    @on_event(LoadEvent)
    def on_load(self, event: LoadEvent) -> None:
        self.log_info("Hello world from MyPlugin!")
    
    @on_event(UnloadEvent)
    def on_unload(self, event: LoadEvent) -> None:
        self.log_info("Goodbye world from MyPlugin!")
```

As it stands, this will work wonderfully. The `Engine` will instantiate as normal, which will now load plugins. This will log:

```console
[ TIMESTAMP ][ INFO ][ MyPlugin ] Hello world from MyPlugin!
[ TIMESTAMP ][ INFO ][ MyPlugin ] Goodbye world from MyPlugin!
```

Please make sure to do the following before testing your plugin:

- It's within a `plugins/your_plugin` folder in your game's directory.
- Your plugin program's filename is `main.py`

Now, please note that you **cannot** override `__init__` when making a plugin, it won't work otherwise.
Further notes include:

- Event listener method names like `on_load` are not necessary, it can be named anything.
- Please do not get these confused with regular `Scene` listener methods like `on_key_pressed`, etc.
- The only way to listen to any `Event` is to listen with `on_event`.
- You can have infinitely many event listeners to any one `Event`. Keep in mind there is no guaranteed order in which they will be fired besides the control flow of `BEFORE` and `AFTER`, at least for now.
- Most regular `Scene` event listeners have a direct equivalent `Event`, i.e. `on_init` = `InitEvent`, `on_key_pressed` = `KeyPressedEvent`, etc.
- Every event listed in `Scene` has an equivalent `Event` for plugins.
