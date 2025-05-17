from __future__ import annotations

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.color.rgb import ColorRGBA
from wame.utils.keys import KEYS
from wame.vector.xy import FloatVector2, IntVector2
from wame.ui.frame import Frame
from wame.ui.renderable import Renderable
from wame.ui.text import Text

from OpenGL.GLU import *
from OpenGL.GL import *

import pygame
import wame

class CheckboxInput(Renderable):
    '''UI Checkbox Input.'''

    __slots__ = (
        "_parent", "_children", "_checked_color", "unchecked_color", "state",
        "_border_color", "_border_width", "_flipped", "_callback",
    )

    def __init__(self, scene: 'Scene', parent: Frame, checked_color: ColorRGBA, unchecked_color: ColorRGBA, *, default: bool=False, y_flipped: bool=False) -> None:
        '''
        Create a UI checkbox input.
        
        Parameters
        ----------
        scene : Scene
            The scene handling this input to dispatch events.
        parent : Frame
            The parent of this input.
        checked_color : ColorRGBA
            The color of the box when checked (`True`/active).
        unchecked_color : ColorRGBA
            The color of the box when unchecked (`False`/inactive).
        default : bool
            The original state of the input before any interaction.
        y_flipped : bool
            If it should be rendered with the Y-axis flipped - May be necessary depending on your OpenGL setup.

        Info
        ----
        The `y_flipped` variable is only needed if you are using the `OPENGL` `Pipeline` and this object is upside down based on your `OpenGL` context.
        '''

        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent = parent
        scene._subscribers_mouse_click.add(self._check_click)

        self._children:list[Renderable] = []

        self._checked_color:ColorRGBA = checked_color if isinstance(checked_color, ColorRGBA) else ColorRGBA.from_iterable(checked_color)
        self._unchecked_color:ColorRGBA = unchecked_color if isinstance(unchecked_color, ColorRGBA) else ColorRGBA.from_iterable(unchecked_color)

        self.state:bool = default
        '''The current state of the checkbox (`True`/`False`)'''

        self._border_color:ColorRGBA = None
        self._border_width:int = None

        self._flipped:bool = y_flipped

        self._callback:Callable[[bool], None] = None

    def _check_click(self, position: IntVector2, _: int) -> None:
        if not self.rect.collidepoint(position.to_tuple()):
            return
        
        self.state = not self.state

        if self._callback:
            self._callback()

    def render(self) -> None:
        '''
        Render this input and it's children to the screen.
        '''
        
        if not self.rect:
            error:str = "The frame must have its size and position set before rendering"
            raise ValueError(error)
    
        if self._engine._pipeline == wame.Pipeline.PYGAME:
            pygame.draw.rect(
                self._engine.screen, self._checked_color.to_tuple() if self.state else self._unchecked_color.to_tuple(), self.rect
            )
        elif self._engine._pipeline == wame.Pipeline.OPENGL:
            posY:int = self.rect.top
            posWidth:int = self.rect.left + self.rect.width
            posHeight:int = self.rect.top + self.rect.height

            if not self._flipped:
                posY = self._engine.screen.get_height() - (posY + self.rect.height)

            glPushMatrix()

            glBegin(GL_QUADS)
            if self.state:
                glColor4f(*self._checked_color.to_tuple())
            else:
                glColor4f(*self._unchecked_color.to_tuple())
                
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
                posX:int = self.rect.left
                posY:int = self.rect.top
                posWidth:int = self.rect.left + self.rect.width
                posHeight:int = self.rect.top + self.rect.height

                if not self._flipped:
                    posY = self._engine.screen.get_height() - (self.rect.top + self.rect.height)

                for index in range(self._border_width):
                    glPushMatrix()

                    glBegin(GL_LINES)
                    glColor4f(*self._border_color.to_tuple())
                    glVertex2f(posX + index, posY + index)
                    glVertex2f(posWidth - index, posY + index)

                    glVertex2f(posWidth - index, posY + index)
                    glVertex2f(posWidth - index, posHeight - index)

                    glVertex2f(posWidth - index, posHeight - index)
                    glVertex2f(posX + index, posHeight - index)

                    glVertex2f(posX + index, posHeight - index)
                    glVertex2f(posX + index, posY + index)
                    glEnd()

                    glPopMatrix()

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

    def set_callback(self, func: Callable[[bool], None]) -> None:
        '''
        Set the callback method for when this input is edited/activated/deactivated.
        
        Parameters
        ----------
        func : typing.Callable[[bool], None]
            The callback method to call - Takes the state of the input (`True`/`False`) as the only parameter.
        '''

        self._callback = func

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
        
        position = IntVector2(
            int(self._parent.rect.left + (self._parent.rect.width * position.x)),
            int(self._parent.rect.top + (self._parent.rect.height * position.y))
        )
        size = IntVector2(
            int(self._parent.rect.width * size.x),
            int(self._parent.rect.height * size.y)
        )

        self.rect = pygame.Rect(*position, *size)

class TextInput(Renderable):
    '''UI Text Input.'''

    __slots__ = (
        "_parent", "_children", "_color", "_border_color", "border_width",
        "_flipped", "text", "_active", "_callback", "_predicate",
    )

    def __init__(self, scene: 'Scene', parent: Frame, text_color: ColorRGBA, font: pygame.font.Font, *, default: str=None, y_flipped: bool=False) -> None:
        '''
        Create a UI text input.
        
        Parameters
        ----------
        scene : Scene
            The scene handling this input for automatic event dispatching.
        parent : Frame
            The parent of this input.
        text_color : ColorRGBA
            The color of the text inside of the input.
        font : pygame.font.Font
            The font of the text inside of the input.
        default : str
            The original text to show in the input before any interaction.
        y_flipped : bool
            If it should be rendered with the Y-axis flipped - May be necessary depending on your OpenGL setup.
        '''

        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent = parent
        scene._subscribers_mouse_click.add(self._check_click)
        scene._subscribers_key_pressed.add(self._check_key)

        self._children:list[Renderable] = []

        self._color:ColorRGBA = None

        self._border_color:ColorRGBA = None
        self._border_width:int = None

        self._flipped:bool = y_flipped
        
        self.text:Text = Text(self, default if default else "", text_color, font, y_flipped)
        '''The internal text object of this input.'''

        self._active:bool = False
        self._callback:Callable[[None], None] = None
        self._predicate: Callable[[int, int], bool] = None

    def _check_click(self, position: IntVector2, _: int) -> None:
        if self.rect.collidepoint(position.to_tuple()):
            active:bool = self._active
            self._active = True

            if not active and self._callback:
                self._callback()
        else:
            active:bool = self._active
            self._active = False
            
            if active and self._callback:
                self._callback()
    
    def _check_key(self, key: int, mods: int) -> None:
        if not self._active:
            return
        
        if self._predicate:
            if not self._predicate(key, mods):
                return
            
        strKey:str = KEYS.get((key, mods), None)

        if not strKey:
            if key == pygame.K_BACKSPACE and len(self.text.raw_text) >= 1:
                text:str = self.text.raw_text[:-1]

                self.text.set_text(text)

                if self._callback:
                    self._callback()

            return
        
        self.text.set_text(self.text.raw_text + strKey)

        if self._callback:
            self._callback()

    def render(self) -> None:
        '''
        Render this input and it's children to the screen.
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
                posY:int = self.rect.top
                posWidth:int = self.rect.left + self.rect.width
                posHeight:int = self.rect.top + self.rect.height

                if not self._flipped:
                    posY = self._engine.screen.get_height() - (self.rect.top + self.rect.height)

                glPushMatrix()

                glBegin(GL_QUADS)
                glColor4f(*self._color.to_tuple())
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
                posX:int = self.rect.left
                posY:int = self.rect.top
                posWidth:int = self.rect.left + self.rect.width
                posHeight:int = self.rect.top + self.rect.height

                if not self._flipped:
                    posY = self._engine.screen.get_height() - (self.rect.top + self.rect.height)

                for index in range(self._border_width):
                    glPushMatrix()

                    glBegin(GL_LINES)
                    glColor4f(*self._border_color.to_tuple())
                    glVertex2f(posX + index, posY + index)
                    glVertex2f(posWidth - index, posY + index)

                    glVertex2f(posWidth - index, posY + index)
                    glVertex2f(posWidth - index, posHeight - index)

                    glVertex2f(posWidth - index, posHeight - index)
                    glVertex2f(posX + index, posHeight - index)

                    glVertex2f(posX + index, posHeight - index)
                    glVertex2f(posX + index, posY + index)
                    glEnd()

                    glPopMatrix()

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

    def set_callback(self, func: Callable[[None], None]) -> None:
        '''
        Set the callback method for when this input is edited/activated/deactivated.
        
        Parameters
        ----------
        func : typing.Callable[[None], None]
            The callback method to call.
        '''

        self._callback = func

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
        position.x += self._parent.rect.left
        position.y += self._parent.rect.top

        size = size if isinstance(size, IntVector2) else IntVector2.from_iterable(size)

        self.rect = pygame.Rect(*position, *size)
        self.text.set_pixel_position((
            10, (self.rect.height // 2) - (self.text.rect.height // 2)
        ))
    
    def set_predicate(self, func: Callable[[int, int], bool]) -> None:
        '''
        Set the predicate for all keys typed in this input. This should return `True` if the keys typed should be entered, `False` otherwise.
        
        Parameters
        ----------
        func : typing.Callable[[int, int], bool]
            The predicate function - Takes the `key` and `mods` parameters provided by `pygame`.
        '''

        self._predicate = func

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
        
        position = IntVector2(
            int(self._parent.rect.left + (self._parent.rect.width * position.x)),
            int(self._parent.rect.top + (self._parent.rect.height * position.y))
        )
        size = IntVector2(
            int(self._parent.rect.width * size.x),
            int(self._parent.rect.height * size.y)
        )

        self.rect = pygame.Rect(*position, *size)
        self.text.set_pixel_position((
            10, (self.rect.height // 2) - (self.text.rect.height // 2)
        ))