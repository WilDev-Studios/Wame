from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.vector import IntVector2, IntVector3
from wame.render import Renderer
from wame.error import *

from OpenGL.GL import *

import pygame
import wame

class Text:
    '''UI Text'''

    def __init__(self, scene:'Scene', text:str, font:wame.Font, color:IntVector3 | tuple[int, int, int]) -> None:
        '''
        Initialize a new text instance
        
        Parameters
        ----------
        scene : `wame.Scene`
            The scene to hook this instance to
        text : `str`
            The characters to be rendered
        font : `wame.Font`
            The font that is rendered - Will be stored with font version name "default" if you wish to use different fonts in `set_font`
        color : `wame.IntVector3 | tuple[int, int, int]`
            The color of the text - Will be stored with color version name "default" if you wish to use different colors in `set_color`
        '''
        
        self._scene:'Scene' = scene

        self._font:wame.Font = font
        self._text:str = text
        self._color:IntVector3 = color if isinstance(color, IntVector3) else IntVector3.from_tuple(color)
    
        self._fonts:dict[str, wame.Font] = {
            "default": self._font
        }
        self._colors:dict[str, wame.IntVector3] = {
            "default": self._color
        }
        
        self._textRender:pygame.Surface = self._font.render(self._text, self._scene.engine.settings.antialiasing, self._color.to_tuple())

        if self._scene.engine._renderer == Renderer.OPENGL:
            self._textRenderBytes = pygame.image.tostring(self._textRender, "RGBA", True)

        self._position:IntVector2 = None
    
    def add_color_option(self, name:str, color:IntVector3) -> None:
        '''
        Add a new color option that the text can switch to when needed
        
        Parameters
        ----------
        name : `str`
            The unique name of this color version
        color : `wame.IntVector3`
            The RGB values of this color version to add to this instance
        
        Raises
        ------
        `wame.UniqueNameAlreadyExists`
            If any unique name already exists
        '''

        if name in self._colors:
            error:str = f"Color with unique name \"{name}\" is already used by this Text instance"
            raise UniqueNameAlreadyExists(error)
        
        self._colors[name] = color if isinstance(color, IntVector3) else IntVector3.from_tuple(color)

    def add_font_option(self, name:str, font:wame.Font) -> None:
        '''
        Add a new font that the text can switch to when needed
        
        Parameters
        ----------
        name : `str`
            The unique name of this font version
        font : `wame.Font`
            The font to add to this instance

        Raises
        ------
        `wame.UniqueNameAlreadyExists`
            If any unique name already exists
        '''

        if name in self._fonts:
            error:str = f"Font with unique name \"{name}\" is already used by this Text instance"
            raise UniqueNameAlreadyExists(error)

        self._fonts[name] = font

    def render(self) -> None:
        '''
        Render the text to the screen
        
        Raises
        ------
        `ValueError`
            If the position was not set before rendering
        '''
        
        if self._position is None:
            error:str = "Position must be defined before the text can be rendered. Please use the Text.set_position() method"
            raise ValueError(error)

        if self._scene.engine._renderer == Renderer.PYGAME:
            self._scene.engine.screen.blit(self._textRender, self._position.to_tuple())
        elif self._scene.engine._renderer == Renderer.OPENGL:
            screenHeight:int = self._scene.engine.screen.get_height()
            textWidth, textHeight = self._textRender.get_size()

            glPushAttrib(GL_ALL_ATTRIB_BITS)

            textureID = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, textureID)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textWidth, textHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, self._textRenderBytes)

            glColor4f(1.0, 1.0, 1.0, 1.0)

            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            glDisable(GL_DEPTH_TEST)

            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self._scene.engine.screen.get_width(), 0, screenHeight, -1, 1)

            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glBindTexture(GL_TEXTURE_2D, textureID)
            glBegin(GL_QUADS)
            x, y = self._position.to_tuple()
            y = screenHeight - y - textHeight

            glTexCoord2f(0, 0); glVertex2f(x, y)
            glTexCoord2f(1, 0); glVertex2f(x + textWidth, y)
            glTexCoord2f(1, 1); glVertex2f(x + textWidth, y + textHeight)
            glTexCoord2f(0, 1); glVertex2f(x, y + textHeight)
            glEnd()

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

            glEnable(GL_DEPTH_TEST)
            glDisable(GL_BLEND)
            glDisable(GL_TEXTURE_2D)

            glDeleteTextures([textureID])

            glPopAttrib()

    def set_color(self, name:str) -> 'Text':
        '''
        Set the color of the text from a previously registered color
        
        Parameters
        ----------
        name : `str`
            The unique name of the color version registered in `Text.add_color_option()`

        Returns
        -------
        text : `wame.Text`
            This instance of `wame.Text` to allow call-chaining
        
        Raises
        ------
        `wame.UniqueNameNotFound`
            If the unique name for the color could not be found
        '''

        if name not in self._colors:
            error:str = f"Color version with unique name \"{name}\" does not exist"
            raise UniqueNameNotFound(error)

        if self._color == self._colors[name]:
            return

        self._color = self._colors[name]
        self._textRender = self._font.render(self._text, self._scene.engine.settings.antialiasing, self._color.to_tuple())

        if self._scene.engine._renderer == Renderer.OPENGL:
            self._textRenderBytes = pygame.image.tostring(self._textRender, "RGBA", True)

        return self

    def set_font(self, name:str) -> 'Text':
        '''
        Set the currently used font of the text using a previously registered font
        
        Parameters
        ----------
        name : `str`
            The unique name of the font version registered in `Text.add_font_option()`
        
        Returns
        -------
        text : `wame.Text`
            This instance of `wame.Text` to allow call-chaining

        Raises
        ------
        `wame.UniqueNameNotFound`
            If the unique name for the font could not be found
        '''

        if name not in self._fonts:
            error:str = f"Font version with unique name \"{name}\" does not exist"
            raise UniqueNameNotFound(error)
        
        if self._font == self._fonts[name]:
            return
        
        self._font = self._fonts[name]
        self._textRender = self._font.render(self._text, self._scene.engine.settings.antialiasing, self._color.to_tuple())

        if self._scene.engine._renderer == Renderer.OPENGL:
            self._textRenderBytes = pygame.image.tostring(self._textRender, "RGBA", True)

        return self

    def set_position(self, position:IntVector2 | tuple[int, int]) -> 'Text':
        '''
        Set the position of the text from the top left corner
        
        Parameters
        ----------
        position : `wame.IntVector2 | tuple[int, int]`
            The X, Y position values of the text

        Returns
        -------
        text : `wame.Text`
            This instance of `wame.Text` to allow call-chaining
        '''
        
        self._position = position if isinstance(position, IntVector2) else IntVector2.from_tuple(position)

        return self
    
    def set_text(self, text:str) -> 'Text':
        '''
        Set the text of the instance
        
        Parameters
        ----------
        text : `str`
            The characters to render

        Returns
        -------
        text : `wame.Text`
            This instance of `wame.Text` to allow call-chaining
        '''
        
        self._text = text
        self._textRender = self._font.render(text, self._scene.engine.settings.antialiasing, self._color.to_tuple())

        if self._scene.engine._renderer == Renderer.OPENGL:
            self._textRenderBytes = pygame.image.tostring(self._textRender, "RGBA", True)

        return self