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
- Import it into your program, and follow the steps below:
```python
import wame

engine: wame.Engine = wame.Engine(...)
engine.start()
```

## Feature Documentation
Below is a list of different features of the engine and how to use them

### Basic Runtime Setup
- `ENGINE`: [Learn how to use the `Engine` here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/basic/ENGINE.md)
- `SCENE`: [Learn how to use the `Scene` here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/basic/SCENE.md)
- `PIPELINE`: [Learn what `Pipeline` is here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/basic/PIPELINE.md)
- `SETTINGS`: [Learn how to use `Settings` here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/basic/SETTINGS.md)

### Advanced Features
- `COLOR`: [Learn how to use the `Color` module here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/advanced/COLOR.md)
- `COMMON`: [Learn how to use the `Common` module here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/advanced/COMMON.md)
- `UI`: [Learn how to use the `UI` module here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/advanced/UI.md)
- `VECTOR`: [Learn how to use the `Vector` module here](https://github.com/WilDev-Studios/Wame/tree/main/docs/documentation/advanced/VECTOR.md)

## Program Tutorials
Below is a list of different tutorials that outlined programs that may be used a lot

### Basic Tutorials
- `FPS DISPLAY`: [Learn how to create a basic FPS text display here](https://github.com/WilDev-Studios/Wame/tree/main/docs/tutorials/basic/FPS_DISPLAY.md)

### Advanced Tutorials
- `TOGGLED FPS DISPLAY`: [Learn how to create a toggleable FPS text display here](https://github.com/WilDev-Studios/Wame/tree/main/docs/tutorials/advanced/TOGGLED_FPS_DISPLAY.md)