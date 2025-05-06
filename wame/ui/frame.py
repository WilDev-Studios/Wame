from __future__ import annotations

from wame.color.rgb import ColorRGBA
from wame.vector.xy import FloatVector2, IntVector2
from wame.ui.renderable import Renderable

from OpenGL.GLU import *
from OpenGL.GL import *

import pygame
import wame

# TODO: Border Radius

class Frame(Renderable):
    '''UI Container'''

    def __init__(self, parent:'Frame', *, color:ColorRGBA=None, y_flipped:bool=False) -> None:
        '''
        Create a UI frame
        
        Parameters
        ----------
        parent : `wame.ui.frame.Frame`
            The parent of this frame
        color : `wame.color.rgb.ColorRGBA`
            The background color of the frame
        y_flipped : `bool`
            If it should be rendered with the Y-axis flipped - May be necessary depending on your OpenGL setup
        
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

        self._color:ColorRGBA = (color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)) if color else None

        self._border_color:ColorRGBA = None
        self._border_width:int = None

        self._flipped:bool = y_flipped

    def render(self) -> None:
        '''
        Render this frame and it's children to the screen
        '''
        
        if not self.position or not self.size:
            error:str = "The frame must have its size and position set before rendering"
            raise ValueError(error)
    
        if self._color:
            if self._engine._pipeline == wame.Pipeline.PYGAME:
                pygame.draw.rect(
                    self._engine.screen, self._color.to_tuple(), self.rect
                )
            elif self._engine._pipeline == wame.Pipeline.OPENGL:
                posY:int = self._engine.screen.get_height() - (self.position.y + self.size.y)
                posWidth:int = self.position.x + self.size.x
                posHeight:int = self.position.y + self.size.y

                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()

                gluOrtho2D(0, self._engine.screen.get_width(), 0, self._engine.screen.get_height())
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()

                glPushMatrix()

                glDisable(GL_LIGHTING)
                glDisable(GL_TEXTURE_2D)

                glColor4f(self._color.r / 255, self._color.g / 255, self._color.b / 255, self._color.a)

                glBegin(GL_QUADS)
                if self._flipped:
                    glVertex2f(self.position.x, posHeight)
                    glVertex2f(posWidth, posHeight)
                    glVertex2f(posWidth, posY)
                    glVertex2f(self.position.x, posY)
                else:
                    glVertex2f(self.position.x, posY)
                    glVertex2f(posWidth, posY)
                    glVertex2f(posWidth, posHeight)
                    glVertex2f(self.position.x, posHeight)
                glEnd()

                glPopMatrix()
        
        if self._border_color and self._border_width >= 1:
            # Lines are straight, no point in antialiasing them

            if self._engine._pipeline == wame.Pipeline.PYGAME:
                for index in range(self._border_width):
                    pygame.draw.lines(self._engine.screen, self._border_color.to_tuple(), True, [
                        (self.position.x + index, self.position.y + index), (self.position.x + self.size.x - index, self.position.y + index),
                        (self.position.x + self.size.x - index, self.position.y + self.size.y - index), (self.position.x + index, self.position.y + self.size.y - index)
                    ])
            elif self._engine._pipeline == wame.Pipeline.OPENGL:
                ...

        for child in self._children:
            child.ask_render()
    
    def set_border(self, color:ColorRGBA, width:int) -> None:
        self._border_color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)
        self._border_width = width

    def set_color(self, color:ColorRGBA) -> None:
        self._color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)

    def set_pixel_position(self, position:IntVector2) -> None:
        position = position if isinstance(position, IntVector2) else IntVector2.from_tuple(position)

        if self._parent:
            position.x += self._parent.position.x
            position.y += self._parent.position.y
        
        self.position = position

    def set_pixel_size(self, size:IntVector2) -> None:
        self.size = size if isinstance(size, IntVector2) else IntVector2.from_tuple(size)

    def set_scaled_position(self, position:FloatVector2) -> None:
        position = position if isinstance(position, FloatVector2) else FloatVector2.from_tuple(position)

        if position.x > 1 or position.x < 0 or position.y > 1 or position.y < 0:
            error:str = "Scaled position X, Y values must be between 0 and 1"
            raise ValueError(error)
        
        newPosition:IntVector2 = IntVector2(0, 0)

        if not self._parent:
            newPosition.x = int(self._engine.screen.get_width() * position.x)
            newPosition.y = int(self._engine.screen.get_height() * position.y)
        else:
            newPosition.x = int(self._parent.position.x + (self._parent.size.x * position.x))
            newPosition.y = int(self._parent.position.y + (self._parent.size.y * position.y))

        self.position = newPosition
    
    def set_scaled_size(self, size:IntVector2) -> None:
        size = size if isinstance(size, FloatVector2) else FloatVector2.from_tuple(size)

        if size.x > 1 or size.x < 0 or size.y > 1 or size.y < 0:
            error:str = "Scaled size X, Y values must be between 0 and 1"
            raise ValueError(error)
    
        newSize:IntVector2 = IntVector2(0, 0)

        if not self._parent:
            newSize.x = int(self._engine.screen.get_width() * size.x)
            newSize.y = int(self._engine.screen.get_height() * size.y)
        else:
            newSize.x = int(self._parent.size.x * size.x)
            newSize.y = int(self._parent.size.y * size.y)

        self.size = newSize