# Wame
Simple, Pythonic, Pygame Wrapper
- Latest Version `v0.4.0`
- Supports Python `3.7+`

[![Documentation Status](https://readthedocs.org/projects/wame/badge/?version=latest&style=for-the-badge)](https://wame.readthedocs.io/en/latest/?badge=latest)

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
- Import it into your program using `import wame`

## Feature Documentation
Below is a list of different features of the engine and how to use them

### Basic Runtime Setup
- `ENGINE`: [Learn how to use the `Engine` here](https://wame.wildevstudios.net/en/latest/pages/documentation/engine/)
- `SCENE`: [Learn how to use the `Scene` here](https://wame.wildevstudios.net/en/latest/pages/documentation/scene/)
- `PIPELINE`: [Learn what `Pipeline` is here](https://wame.wildevstudios.net/en/latest/pages/documentation/pipeline/)
- `SETTINGS`: [Learn how to use `Settings` here](https://wame.wildevstudios.net/en/latest/pages/documentation/settings/)

### Advanced Features
- `COLOR`: [Learn how to use the `Color` module here](https://wame.wildevstudios.net/en/latest/pages/documentation/color/)
- `COMMON`: [Learn how to use the `Common` module here](https://wame.wildevstudios.net/en/latest/pages/documentation/common/)
- `UI`: [Learn how to use the `UI` module here](https://wame.wildevstudios.net/en/latest/pages/documentation/ui/)
- `VECTOR`: [Learn how to use the `Vector` module here](https://wame.wildevstudios.net/en/latest/pages/documentation/vector/)

## Program Tutorials
Below is a list of different tutorials that outlined programs that may be used a lot

### Basic Tutorials
- `FPS DISPLAY`: [Learn how to create a basic FPS text display here](https://wame.wildevstudios.net/en/latest/pages/tutorials/fps_display/)

### Advanced Tutorials
- `TOGGLED FPS DISPLAY`: [Learn how to create a toggleable FPS text display here](https://wame.wildevstudios.net/en/latest/pages/tutorials/toggled_fps_display/)