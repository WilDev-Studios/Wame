from __future__ import annotations

from wame.pipeline import Pipeline
from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.vector.xy import IntVector2, FloatVector2

from OpenGL.GL import *

import pygame

class Image(Renderable):
    '''UI Image Object'''

    def __init__(self, parent:Frame, image:pygame.Surface, y_flipped:bool=False) -> None:
        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent:Frame = parent

        self.image:pygame.Surface = image
        self._gl_texture_id = None
        self._flipped:bool = y_flipped

        self._render_image()

    def _render_image(self) -> None:
        if self._engine._pipeline == Pipeline.OPENGL:
            if self._gl_texture_id:
                glDeleteTextures([self._gl_texture_id])

            textData = pygame.image.tostring(self.image, "RGBA", True)
            width, height = self.image.get_size()

            self._gl_texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self._gl_texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
            glBindTexture(GL_TEXTURE_2D, 0)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position.to_tuple(), self.image.get_size())

    def render(self) -> None:
        if self._engine._pipeline == Pipeline.PYGAME:
            self._engine.screen.blit(self.image, self.position.to_tuple())
        elif self._engine._pipeline == Pipeline.OPENGL:
            if not self._gl_texture_id:
                return
            
            width:int = self.image.get_width()
            height:int = self.image.get_height()

            posX:int = self.position.x
            posY:int = self.position.y

            if not self._flipped:
                posY = self._engine.screen.get_height() - (self.position.y + self.image.get_height())

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
    
    def set_image(self, image:pygame.Surface) -> None:
        self.image = image
        self._render_image()