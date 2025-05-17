from __future__ import annotations

from wame.color.rgb import ColorRGBA
from wame.vector.xy import FloatVector2, IntVector2
from wame.ui.renderable import Renderable

from OpenGL.GLU import *
from OpenGL.GL import *

import pygame
import wame

class Frame(Renderable):
    '''UI Container.'''

    __slots__ = (
        "_parent", "_children", "_color", "_border_color", "_border_width",
        "_flipped",
    )

    def __init__(self, parent: 'Frame', *, color: ColorRGBA=None, y_flipped: bool=False) -> None:
        '''
        Create a UI frame.
        
        Parameters
        ----------
        parent : Frame
            The parent of this frame.
        color : ColorRGBA
            The background color of the frame.
        y_flipped : bool
            If it should be rendered with the Y-axis flipped - May be necessary depending on your OpenGL setup.
        
        Note
        ----
        Scenes already natively contain a UI frame. Unless you want to make a sub-frame to encapsulate other child renderables, using the `Scene`'s `frame` attribute should be sufficient

        Info
        ----
        The `y_flipped` variable is only needed if you are using the `OPENGL` `Pipeline` and this object is upside down based on your `OpenGL` context.
        '''

        super().__init__(parent if isinstance(parent, wame.Engine) else parent._engine)

        if isinstance(parent, Frame):
            parent.add_child(self)
            
            self._parent = parent
        else: # If natively set to the engine, this is the scene's native frame (no parent)
            self._parent = None

        self._children:list[Renderable] = []

        self._color:ColorRGBA = (color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)) if color else None

        self._border_color:ColorRGBA = None
        self._border_width:int = None

        self._flipped:bool = y_flipped

    def render(self) -> None:
        '''
        Render this frame and it's children to the screen.
        '''

        if not self.rect:
            error:str = "The frame must have its size and position set before rendering"
            raise ValueError(error)
    
        if self._color:
            if self._engine._pipeline == wame.Pipeline.PYGAME:
                pygame.draw.rect(
                    self._engine.screen, self._color.to_tuple(), self.rect
                )
            elif self._engine._pipeline == wame.Pipeline.OPENGL:
                posY:int = self._engine.screen.get_height() - (self.rect.top + self.rect.height)
                posWidth:int = self.rect.left + self.rect.width
                posHeight:int = self.rect.top + self.rect.height

                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()

                gluOrtho2D(0, self._engine.screen.get_width(), 0, self._engine.screen.get_height())
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()

                glPushMatrix()

                glDisable(GL_LIGHTING)
                glDisable(GL_TEXTURE_2D)

                glColor4f(*self._color.normalized())

                glBegin(GL_QUADS)
                if self._flipped:
                    glVertex2f(self.rect.left, posHeight)
                    glVertex2f(posWidth, posHeight)
                    glVertex2f(posWidth, posY)
                    glVertex2f(self.rect.left, posY)
                else:
                    glVertex2f(self.rect.left, posY)
                    glVertex2f(posWidth, posY)
                    glVertex2f(posWidth, posHeight)
                    glVertex2f(self.rect.left, posHeight)
                glEnd()

                glPopMatrix()
        
        if self._border_color and self._border_width >= 1:
            # Lines are straight, no point in antialiasing them

            if self._engine._pipeline == wame.Pipeline.PYGAME:
                for index in range(self._border_width):
                    pygame.draw.lines(self._engine.screen, self._border_color.to_tuple(), True, [
                        (self.rect.left + index, self.rect.top + index), (self.rect.left + self.rect.width - index, self.rect.top + index),
                        (self.rect.left + self.rect.width - index, self.rect.top + self.rect.height - index), (self.rect.left + index, self.rect.top + self.rect.height - index)
                    ])
            elif self._engine._pipeline == wame.Pipeline.OPENGL:
                ...

        for child in self._children:
            child.ask_render()
    
    def set_border(self, color: ColorRGBA, width: int) -> None:
        '''
        Set the border of this object.
        
        Parameters
        ----------
        color : ColorRGBA
            The color to set the border to.
        width : int
            The width of the border.
        '''

        self._border_color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)
        self._border_width = width

    def set_color(self, color: ColorRGBA) -> None:
        '''
        Set the color of this object.
        
        Parameters
        ----------
        color : ColorRGBA
            The color of this object.
        '''

        self._color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)

    def set_pixel_transform(self, position: IntVector2, size: IntVector2) -> None:
        '''
        Set the exact pixel transform (position, size) of this object.
        
        Parameters
        ----------
        position : IntVector2
            The exact position of this object from the top-left point.
        size : IntVector2
            The exact size of this object.
        '''

        position = position if isinstance(position, IntVector2) else IntVector2.from_iterable(position)

        if self._parent:
            position.x += self._parent.rect.left
            position.y += self._parent.rect.top

        size = size if isinstance(size, IntVector2) else IntVector2.from_iterable(size)

        self.rect = pygame.Rect(*position, *size)

    def set_scaled_transform(self, position: FloatVector2, size: FloatVector2) -> None:
        '''
        Set the scaled transform (position, size) of this object.
        
        Parameters
        ----------
        position : FloatVector2
            The scaled position of this object from the top-left point.
        size : FloatVector2
            The scaled size of this object.
        '''

        position = position if isinstance(position, FloatVector2) else FloatVector2.from_iterable(position)
        size = size if isinstance(size, FloatVector2) else FloatVector2.from_iterable(size)

        if position.x < 0 or position.x > 1 or position.y < 0 or position.y > 1:
            error: str = "Scaled position X, Y values must be between 0 and 1."
            raise ValueError(error)
        
        if size.x < 0 or size.x > 1 or size.y < 0 or size.y > 1:
            error: str = "Scaled size X, Y values must be between 0 and 1."
            raise ValueError(error)
        
        new_position: IntVector2 = IntVector2(0, 0)
        new_size: IntVector2 = IntVector2(0, 0)

        if self._parent:
            new_position.x = int(self._parent.rect.left + (self._parent.rect.width * position.x))
            new_position.y = int(self._parent.rect.top + (self._parent.rect.height * position.y))

            new_size.x = int(self._parent.rect.width * size.x)
            new_size.y = int(self._parent.rect.height * size.y)
        else:
            new_position.x = int(self._engine.screen.get_width() * position.x)
            new_position.y = int(self._engine.screen.get_height() * position.y)

            new_size.x = int(self._engine.screen.get_width() * size.x)
            new_size.y = int(self._engine.screen.get_height() * size.y)

        self.rect = pygame.Rect(*new_position, *new_size)