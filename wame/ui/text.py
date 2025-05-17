from __future__ import annotations

from wame.color.rgb import ColorRGBA
from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.vector.xy import IntVector2, FloatVector2

from wame.pipeline import Pipeline

from OpenGL.GL import *

import pygame

class Text(Renderable):
    '''UI Text Object.'''

    __slots__ = (
        "_parent", "_color", "_colors", "_font", "_fonts", "raw_text", "text",
        "_gl_texture_id", "_flipped",
    )

    def __init__(self, parent: Frame, text: str, color: ColorRGBA, font: pygame.font.Font, y_flipped: bool=False) -> None:
        """
        Instantiate a Text object.

        Parameters
        ----------
        parent : Frame
            The frame that will act as this child's parent.
        text : str
            The raw text that will be originally displayed.
        color : ColorRGBA
            The color of the text.
        font : pygame.font.Font
            The font of the text.
        y_flipped : bool
            Flips the position and orientation based on `OpenGL` context.
        
        Info
        ----
        The `y_flipped` variable is only needed if you are using the `OPENGL` `Pipeline` and this object is upside down based on your `OpenGL` context.
        """

        super().__init__(parent._engine)

        color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)

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

        if self._engine._pipeline != Pipeline.OPENGL:
            return
        
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

    def add_color(self, name: str, color: ColorRGBA, overwrite: bool=False) -> None:
        """
        Register a color with this object.
        
        Parameters
        ----------
        name : str
            The unique name for this color.
        color : ColorRGBA
            The color to register.
        overwrite : bool
            If this already exists, if it's ok to overwrite.
        
        Raises
        ------
        ValueError
            If the unique name already exists.
        """

        if name in self._colors and not overwrite:
            error:str = f"Color with name {name} is already registered as a color."
            raise ValueError(error)

        self._colors[name] = color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)

    def add_font(self, name: str, font: pygame.font.Font) -> None:
        """
        Register a font with this object.
        
        Parameters
        ----------
        name : str
            The unique name for this font.
        font : pygame.font.Font
            The font to register.

        Raises
        ------
        ValueError
            If the unique name already exists.
        """
        
        if name in self._fonts:
            error:str = f"Font with name {name} is already registered as a font."
            raise ValueError(error)
        
        self._fonts[name] = font

    def render(self) -> None:
        if self._engine._pipeline == Pipeline.PYGAME:
            self._engine.screen.blit(self.text, self.rect.topleft)
        elif self._engine._pipeline == Pipeline.OPENGL:
            if not self._gl_texture_id:
                return
            
            width:int = self.text.get_width()
            height:int = self.text.get_height()

            posX:int = self.rect.left
            posY:int = self.rect.top

            if not self._flipped:
                posY = self._engine.screen.get_height() - (self.rect.top + self.text.get_height())

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

    def set_color(self, name: str) -> None:
        '''
        Set the color of this text from a registered name.

        Parameters
        ----------
        name : str
            The unique name previously registered to a color.
        
        Raises
        ------
        ValueError
            If a color with the desired name doesn't exist.
        '''

        if name not in self._colors:
            error:str = f"Color with name {name} is not registered as a color."
            raise ValueError(error)
        
        self._color = self._colors[name]
        self._render_text()
    
    def set_font(self, name: str) -> None:
        '''
        Set the font of this text from a registered name.
        
        Parameters
        ----------
        name : str
            The unique name previously registered to a font.
        
        Raises
        ------
        ValueError
            If the unique name does not exist.
        '''
        
        if name not in self._fonts:
            error:str = f"Font with name {name} is not registered as a font."
            raise ValueError(error)
        
        self._font = self._fonts[name]
        self._render_text()
    
    def set_pixel_position(self, position: IntVector2) -> None:
        '''
        Set the exact pixel position of this object.
        
        Parameters
        ----------
        position : IntVector2
            The exact position to place the top-left of this object.
        '''

        position = position if isinstance(position, IntVector2) else IntVector2.from_iterable(position)
        position.x += self._parent.rect.left
        position.y += self._parent.rect.top

        self.rect = pygame.Rect(position.to_tuple(), self.text.get_rect().size)

    def set_scaled_position(self, position: FloatVector2) -> None:
        '''
        Set the scaled pixel position of this object.
        
        Parameters
        ----------
        position : FloatVector2
            The scaled position to place the top-left of this object.
        
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

        self.rect = pygame.Rect(new_position.to_tuple(), self.text.get_rect().size)
    
    def set_text(self, text: str) -> None:
        '''
        Set the text of this object.
        
        Parameters
        ----------
        text : str
            The raw text to set.
        '''
        
        self.raw_text = text
        self._render_text()

        self.rect = pygame.Rect(self.rect.topleft, self.text.get_rect().size)