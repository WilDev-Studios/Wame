# Wame
Simple, Pythonic, Pygame Wrapper
- Latest Version `v0.7.0`
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

## Documentation
You can find our documentation [here](https://wame.wildevstudios.net/)

## Getting Started
After installation:
- Instantiate a new `Engine` (runs the game loop and dispatches events)
- Define a new `~Scene` subclass (manages your objects and logic)
```python
import wame

class BasicScene(wame.Scene):
    def __init__(self, engine: wame.Engine) -> None:
        super().__init__(engine)
    
    def on_render(self) -> None:
        ...
    
    def on_update(self) -> None:
        ...

engine: wame.Engine = wame.Engine("Basic Game Window", wame.Pipeline.PYGAME)
engine.register_scene("Basic", BasicScene)
engine.set_scene("Basic")

engine.start()
```
This will create a fullscreen, black window. You can close it by pressing `ALT`+`F4`.
- If you'd like to see more functional examples, visit our [Tutorials](https://wame.wildevstudios.net/en/latest/pages/tutorials) section of our documentation

## Contributing
Thanks for your interest in contributing to our game engine! Contributions are welcome, as they can only help us get to where we want to see `wame` go!
Whether you want to submit a bug report, fix a bug, add a new feature, remove parts of the program, we welcome your contributions.

### How to Contribute
1. Fork this repository
    - Fork this repository to your own GitHub account by clicking the "Fork" button at the top-right of this page.
2. Clone your fork
    - Clone the forked repository to your local machine using the following command:
    - `git clone https://github.com/your-username/your-fork.git`
3. Create a new branch
    - Before making any changes, create a new branch with a descriptive name for your work/changes. For example:
    - `git checkout -b feature-name`
4. Make your changes
    - Implement your changes, whether it's fixing bugs, improving documentation, or adding new features.
    - Be sure to write clear, concise commit messages explaining the changes you've made.
5. Commit your changes
    - Once your changes are ready, commit them to your local branch:
    - `git add .`
    - `git commit -m "Add feature-name"`
6. Push your changes
    - Push your changes to your forked repository:
    - `git push origin feature-name`
7. Create a pull request
    - Open a pull request on the original repository from your fork.
    - Ensure that your pull request explains the purpose of the changes and any relevant context.
    - If applicable, include links to relevant issues.

### Reporting Bugs
- If you find a bug or issue, please open an issue on the `Issues` page above.
- Be sure to provide detailed information to help us understand and reproduce the problem.

### Feature Requests
- We welcome suggestions for new features.
- If you have an idea, please open an issue on the `Issues` page above to discuss it first.
- This ensures that we're all on the same page and helps us prioritize improvements.

### Thanks for Contributing!
Your contributions make this project better and more useful for everyone! Thank you for taking the time to improve this project!

## License
This project is licensed under the [MIT License](https://github.com/WilDev-Studios/Wame/blob/main/LICENSE). Copyright &copy; 2025 WilDev Studios. All rights reserved. 