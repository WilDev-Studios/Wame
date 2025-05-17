from __future__ import annotations

from wame.pipeline import Pipeline
from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.vector.xy import IntVector2, FloatVector2

from OpenGL.GL import *

import pygame

class Image(Renderable):
    '''UI Image Object.'''

    __slots__ = ("_parent", "image", "_gl_texture_id", "_flipped",)

    def __init__(self, parent: Frame, image: pygame.Surface, y_flipped: bool=False) -> None:
        """
        Instantiate a new image.

        Parameters
        ----------
        parent : Frame
            The frame to set this child image's parent to.
        image : pygame.Surface
            The image/surface to render.
        y_flipped : bool
            Flips the position and orientation based on `OpenGL` context.

        Info
        ----
        The `y_flipped` variable is only needed if you are using the `OPENGL` `Pipeline` and this object is upside down based on your `OpenGL` context.
        """

        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent:Frame = parent

        self.image:pygame.Surface = image
        self._gl_texture_id = None
        self._flipped:bool = y_flipped

        self._render_image()

    def _render_image(self) -> None:
        if self._engine._pipeline != Pipeline.OPENGL:
            return
        
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

    def render(self) -> None:
        if self._engine._pipeline == Pipeline.PYGAME:
            self._engine.screen.blit(self.image, self.rect.topleft)
        elif self._engine._pipeline == Pipeline.OPENGL:
            if not self._gl_texture_id:
                return
            
            width:int = self.image.get_width()
            height:int = self.image.get_height()

            posX:int = self.rect.left
            posY:int = self.rect.top

            if not self._flipped:
                posY = self._engine.screen.get_height() - (posY + self.image.get_height())

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

    def set_pixel_position(self, position: IntVector2) -> None:
        '''
        Set the exact pixel position of this object.
        
        Parameters
        ----------
        position : IntVector2
            The exact position of this object from the top-left point.
        '''

        position = position if isinstance(position, IntVector2) else IntVector2.from_iterable(position)
        position.x += self._parent.rect.left
        position.y += self._parent.rect.top

        self.rect = pygame.Rect(position.to_tuple(), self.image.get_rect().size)
    
    def set_scaled_position(self, position: FloatVector2) -> None:
        '''
        Set the scaled position of this object.
        
        Parameters
        ----------
        position : FloatVector2
            The scaled position of this object from the top-left point.
        
        Raises
        ------
        ValueError
            If the provided positional values exceed `0`-`1`.
        '''

        position = position if isinstance(position, FloatVector2) else FloatVector2.from_iterable(position)

        if position.x > 1 or position.x < 0 or position.y > 1 or position.y < 0:
            error:str = "Scaled position X, Y values must be between 0 and 1"
            raise ValueError(error)
        
        new_position:IntVector2 = IntVector2(
            int(self._parent.rect.left + (self._parent.rect.width * position.x)),
            int(self._parent.rect.top + (self._parent.rect.height * position.y))
        )

        self.rect = pygame.Rect(new_position.to_tuple(), self.image.get_rect().size)
    
    def set_image(self, image: pygame.Surface) -> None:
        '''
        Set the image of this object.
        
        Parameters
        ----------
        image : pygame.Surface
            The image/surface to set.
        '''
        
        self.image = image
        self.rect = pygame.Rect(self.rect.topleft, image.get_rect().size)

        self._render_image()