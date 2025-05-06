from __future__ import annotations

from wame.color.rgb import ColorRGBA
from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.vector.xy import IntVector2, FloatVector2

from wame.pipeline import Pipeline

from OpenGL.GL import *

import pygame

class Text(Renderable):
    '''UI Text Object'''

    def __init__(self, parent:Frame, text:str, color:ColorRGBA, font:pygame.font.Font, y_flipped:bool=False) -> None:
        """

        Info
        ----
        The `y_flipped` variable is only needed if you are using the `OPENGL` `Pipeline` and this object is upside down based on your `OpenGL` context.
        """
        super().__init__(parent._engine)

        color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)

        parent.add_child(self)
        self._parent:Frame = parent

        self._color:ColorRGBA = color
        self._colors:dict[str, ColorRGBA] = {
            "default": color
        }

        self._font:pygame.font.Font = font
        self._fonts:dict[str, pygame.font.Font] = {
            "default": font
        }

        self.raw_text:str = text
        self.text:pygame.Surface = font.render(text, self._engine.settings.antialiasing, color.to_tuple())
        self._gl_texture_id = None
        self._flipped:bool = y_flipped

        self._render_text()

    def _render_text(self) -> None:
        self.text = self._font.render(self.raw_text, self._engine.settings.antialiasing, self._color.to_tuple())

        if self._engine._pipeline == Pipeline.OPENGL:
            if self._gl_texture_id:
                glDeleteTextures([self._gl_texture_id])

            textData = pygame.image.tostring(self.text, "RGBA", True)
            width, height = self.text.get_size()

            self._gl_texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self._gl_texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
            glBindTexture(GL_TEXTURE_2D, 0)

    def add_color(self, name:str, color:ColorRGBA, overwrite:bool=False) -> None:
        if name in self._colors and not overwrite:
            error:str = f"Color with name {name} is already registered as a color"
            raise ValueError(error)

        self._colors[name] = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)

    def add_font(self, name:str, font:pygame.font.Font) -> None:
        if name in self._fonts:
            error:str = f"Font with name {name} is already registered as a font"
            raise ValueError(error)
        
        self._fonts[name] = font

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.to_tuple(), self.text.get_size())

    def render(self) -> None:
        if self._engine._pipeline == Pipeline.PYGAME:
            self._engine.screen.blit(self.text, self.position.to_tuple())
        elif self._engine._pipeline == Pipeline.OPENGL:
            if not self._gl_texture_id:
                return
            
            width:int = self.text.get_width()
            height:int = self.text.get_height()

            posX:int = self.position.x
            posY:int = self.position.y

            if not self._flipped:
                posY = self._engine.screen.get_height() - (self.position.y + self.text.get_height())

            glPushMatrix()

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self._gl_texture_id)

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            if self._engine.settings.antialiasing:
                glEnable(GL_MULTISAMPLE)

            glColor4f(1.0, 1.0, 1.0, 1.0)

            glBegin(GL_QUADS)
            if self._flipped:
                glTexCoord2f(0, 1)
                glVertex2f(posX, posY)
                glTexCoord2f(1, 1)
                glVertex2f(posX + width, posY)
                glTexCoord2f(1, 0)
                glVertex2f(posX + width, posY + height)
                glTexCoord2f(0, 0)
                glVertex2f(posX, posY + height)
            else:
                glTexCoord2f(0, 0)
                glVertex2f(posX, posY)
                glTexCoord2f(1, 0)
                glVertex2f(posX + width, posY)
                glTexCoord2f(1, 1)
                glVertex2f(posX + width, posY + height)
                glTexCoord2f(0, 1)
                glVertex2f(posX, posY + height)
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_BLEND)
            glDisable(GL_TEXTURE_2D)

            if self._engine.settings.antialiasing:
                glDisable(GL_MULTISAMPLE)

            glPopMatrix()

        for child in self._children:
            child.ask_render()

    def set_color(self, name:str) -> None:
        if name not in self._colors:
            error:str = f"Color with name {name} is not registered as a color"
            raise ValueError(error)
        
        self._color = self._colors[name]
        self._render_text()
    
    def set_font(self, name:str) -> None:
        if name not in self._fonts:
            error:str = f"Font with name {name} is not registered as a font"
            raise ValueError(error)
        
        self._font = self._fonts[name]
        self._render_text()
    
    def set_pixel_position(self, position:IntVector2) -> None:
        position = position if isinstance(position, IntVector2) else IntVector2.from_tuple(position)
        position.x += self._parent.position.x
        position.y += self._parent.position.y

        self.position = position
    
    def set_scaled_position(self, position:FloatVector2) -> None:
        position = position if isinstance(position, FloatVector2) else FloatVector2.from_tuple(position)

        if position.x > 1 or position.x < 0 or position.y > 1 or position.y < 0:
            error:str = "Scaled position X, Y values must be between 0 and 1"
            raise ValueError(error)
        
        newPosition:IntVector2 = IntVector2(0, 0)
        newPosition.x = int(self._parent.position.x + (self._parent.size.x * position.x))
        newPosition.y = int(self._parent.position.y + (self._parent.size.y * position.y))

        self.position = newPosition
    
    def set_text(self, text:str) -> None:
        self.raw_text = text
        self._render_text()