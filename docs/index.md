# Wame Engine Documentation
Simple, Pythonic, Pygame Wrapper

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
- Import it into your program