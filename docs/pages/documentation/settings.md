# Settings
The `wame` `Engine` automatically creates settings that the `Engine` will utilize during runtime and will save them persistently across sessions.

## Settings System
Defined in `wame.settings`:
- `Settings` is an internal object utilized by the `Engine` that allows for the persistent saving of client settings between game sessions.
- As of `0.4.0`, `Settings` are not currently allowed to be disabled natively for custom implementations. This will change in the future.

## Example Programs
```python
# Enable/Disable VSync (Vertical Sync)
engine.settings.vsync = True/False

# Enable/Disable Antialiasing
engine.settings.antialiasing = True/False

# Edit Max Frames Per Second
engine.settings.max_fps = 165

# Edit Tabbed/Out-of-Focus Frames Per Second
engine.settings.tabbed_fps = 30
```