# Pipeline
The `wame` game `Engine` uses different rendering pipelines, defined below, to render objects/elements onto the screen during runtime.

## Pipeline Types
Defined in `wame.pipeline`:
- `OPENGL`: Flags the `Engine` to only set `Pygame` up to use `OpenGL` rendering, and only changes the background color to the desired, normalized `RGB` values:
    - Allows the use of most `Pygame` functionality, but rendering is left to raw `OpenGL` commands, like those found in `PyOpenGL`.
    - This is very advanced, and not recommended for most developers unless performance is critical (and development time is extended).
- `PYGAME`: Flags the `Engine` to run `Pygame` as normal:
    - Allows the use of all normal `Pygame` functionality, including drawing, fonts, etc.

## Example Programs
```python
# Only used when instantiating the `Engine`
engine: wame.Engine = wame.Engine("Test Window", wame.Pipeline.OPENGL)
# OR
engine: wame.Engine = wame.Engine("Test Window", wame.Pipeline.PYGAME)
```
```python
# If you'd like to draw a line, it depends on what `Pipeline` you used

# If `PYGAME` is desired, your life is easy:
def on_render(self) -> None: # Inside `Scene`
    pygame.draw.line(self.screen, (255, 255, 255), point_xy_1, point_xy_2)
    # Draw a line     On screen      All white      1st Point   2nd Point
    #                                \--RGB--/      \----- tuples -----/

# If `OPENGL` is desired (why):
def on_render(self) -> None: # Inside `Scene`
    glBegin(GL_LINES) # Tell OpenGL to draw using lines
    glColor3f(1, 1, 1) # Use normalized RGB values (normalized = RGB / 255)

    glVertex2f(*point_xy_1) # Tell it the first coordinate
    glVertex2f(*point_xy_2) # Tell it the second coordinate

    glEnd() # End the draw call
```
> [!CAUTION]
> If using OpenGL, be sure to create your context in `on_first`. The `Engine` only manages the background color, everything else is up to you.