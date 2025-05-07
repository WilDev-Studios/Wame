# Settings
The `wame` `Engine` automatically creates settings that the `Engine` will utilize during runtime and will save them persistently across sessions.

## Settings System
Defined in `wame.settings`:
- `Settings` is an internal object utilized by the `Engine` that allows for the persistent saving of client settings between game sessions.

## Example Programs
```python
# Enable/Disable VSync (Vertical Sync)
engine.settings.vsync = True/False

# Enable/Disable Antialiasing
engine.settings.antialiasing = True/False

# Edit Max Frames Per Second
engine.settings.max_fps = 165
```
```python
# Disable `Engine` handling of settings - So devs can save/load using custom logic
engine: wame.Engine = wame.Engine(..., settings_persistent=False)
```