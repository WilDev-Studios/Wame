from __future__ import annotations

from typing import Callable

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
    '''UI Checkbox Input'''

    def __init__(self, parent:'Frame', checkedColor:ColorRGBA, uncheckedColor:ColorRGBA, *, default:bool=False, y_flipped:bool=False) -> None:
        '''
        Create a UI checkbox input
        
        Parameters
        ----------
        parent : wame.ui.frame.Frame
            The parent of this input
        checkedColor : wame.color.rgb.ColorRGBA
            The color of the box when checked (`True`/active)
        uncheckedColor : wame.color.rgb.ColorRGBA
            The color of the box when unchecked (`False`/inactive)
        default : bool
            The original state of the input before any interaction
        y_flipped : bool
            If it should be rendered with the Y-axis flipped - May be necessary depending on your OpenGL setup

        Info
        ----
        The `y_flipped` variable is only needed if you are using the `OPENGL` `Pipeline` and this object is upside down based on your `OpenGL` context.
        '''

        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent = parent

        self._children:list[Renderable] = []

        self._checked_color:ColorRGBA = checkedColor if isinstance(checkedColor, ColorRGBA) else ColorRGBA.from_tuple(checkedColor)
        self._unchecked_color:ColorRGBA = uncheckedColor if isinstance(uncheckedColor, ColorRGBA) else ColorRGBA.from_tuple(uncheckedColor)
        self.state:bool = default
        '''The current state of the checkbox (`True`/`False`)'''

        self._border_color:ColorRGBA = None
        self._border_width:int = None

        self._flipped:bool = y_flipped

        self._callback:Callable[[bool], None] = None

    def check_click(self, position:IntVector2) -> None:
        '''
        Check if the location in which a mouse click is able to interact with this input
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The X, Y vector/position of the mouse
        '''

        if not self.rect.collidepoint(position.to_tuple()):
            return
        
        self.state = not self.state

        if self._callback:
            self._callback()

    def render(self) -> None:
        '''
        Render this input and it's children to the screen
        '''
        
        if not self.position or not self.size:
            error:str = "The frame must have its size and position set before rendering"
            raise ValueError(error)
    
        if self._engine._pipeline == wame.Pipeline.PYGAME:
            pygame.draw.rect(
                self._engine.screen, self._checked_color.to_tuple() if self.state else self._unchecked_color.to_tuple(), self.rect
            )
        elif self._engine._pipeline == wame.Pipeline.OPENGL:
            posY:int = self.position.y
            posWidth:int = self.position.x + self.size.x
            posHeight:int = self.position.y + self.size.y

            if not self._flipped:
                posY = self._engine.screen.get_height() - (self.position.y + self.size.y)

            glPushMatrix()

            glBegin(GL_QUADS)
            if self.state:
                glColor4f(*self._checked_color.to_tuple())
            else:
                glColor4f(*self._unchecked_color.to_tuple())
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
                posX:int = self.position.x
                posY:int = self.position.y
                posWidth:int = self.position.x + self.size.x
                posHeight:int = self.position.y + self.size.y

                if not self._flipped:
                    posY = self._engine.screen.get_height() - (self.position.y + self.size.y)

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
    
    def set_border(self, color:ColorRGBA, width:int) -> None:
        '''
        Set the border of this object
        
        Parameters
        ----------
        color : wame.color.rgb.ColorRGBA
            The color to set the border to
        width : int
            The width of the border
        '''
        
        self._border_color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)
        self._border_width = width

    def set_callback(self, func:Callable[[bool], None]) -> None:
        '''
        Set the callback method for when this input is edited/activated/deactivated
        
        Parameters
        ----------
        func : typing.Callable[[bool], None]
            The callback method to call - Takes the state of the input (`True`/`False`) as the only parameter
        '''

        self._callback = func

    def set_pixel_position(self, position:IntVector2) -> None:
        '''
        Set the exact pixel position of this object
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The exact position of this object from the top-left point
        '''
        
        position = position if isinstance(position, IntVector2) else IntVector2.from_iterable(position)

        if self._parent:
            position.x += self._parent.position.x
            position.y += self._parent.position.y
        
        self.position = position

    def set_pixel_size(self, size:IntVector2) -> None:
        '''
        Set the exact pixel size of this object
        
        Parameters
        ----------
        size : wame.vector.xy.IntVector2
            The exact size of this object
        '''
        
        self.size = size if isinstance(size, IntVector2) else IntVector2.from_iterable(size)

    def set_scaled_position(self, position:FloatVector2) -> None:
        '''
        Set the scaled position of this object
        
        Parameters
        ----------
        position : wame.vector.xy.FloatVector2
            The scaled position of this object from the top-left point
        
        Raises
        ------
        ValueError
            If the provided positional values exceed `0`-`1`
        '''
        
        position = position if isinstance(position, FloatVector2) else FloatVector2.from_iterable(position)

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
        '''
        Set the scaled size of this object
        
        Parameters
        ----------
        size : wame.vector.xy.IntVector2
            The scaled size of this object
        
        Raises
        ------
        ValueError
            If the provided size values exceed `0`-`1`
        '''
        
        size = size if isinstance(size, FloatVector2) else FloatVector2.from_iterable(size)

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

class TextInput(Renderable):
    '''UI Text Input'''

    def __init__(self, parent:'Frame', textColor:ColorRGBA, font:pygame.font.Font, *, default:str=None, yFlipped:bool=False) -> None:
        '''
        Create a UI text input
        
        Parameters
        ----------
        parent : wame.ui.frame.Frame
            The parent of this input
        textColor : wame.color.rgb.ColorRGBA
            The color of the text inside of the input
        font : pygame.font.Font
            The font of the text inside of the input
        default : str
            The original text to show in the input before any interaction
        yFlipped : bool
            If it should be rendered with the Y-axis flipped - May be necessary depending on your OpenGL setup
        '''

        super().__init__(parent._engine)

        parent.add_child(self)
        self._parent = parent

        self._children:list[Renderable] = []

        self._color:ColorRGBA = None

        self._border_color:ColorRGBA = None
        self._border_width:int = None

        self._flipped:bool = yFlipped
        
        self.text:Text = Text(self, default if default else "", textColor, font, yFlipped)
        '''The internal text object of this input'''

        self._active:bool = False
        self._callback:Callable[[None], None] = None

    def check_click(self, position:IntVector2) -> None:
        '''
        Check if the location in which a mouse click is able to interact with this input
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The X, Y vector/position of the mouse
        '''

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
    
    def check_key(self, key:int, mods:int, predicate:Callable[[int, int], bool]=None) -> None:
        '''
        Check if a key/mod combination is able to interact with this input (if active)
        
        Parameters
        ----------
        key : int
            The raw `pygame` keycode input
        mods : int
            The raw `pygame` key modifications
        predicate : typing.Callable[[int, int], bool]
            A function object that should be used to filter out whether the input should or should not be accepted
        '''

        if not self._active:
            return
        
        if predicate:
            if not predicate(key, mods):
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
        Render this input and it's children to the screen
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
                posY:int = self.position.y
                posWidth:int = self.position.x + self.size.x
                posHeight:int = self.position.y + self.size.y

                if not self._flipped:
                    posY = self._engine.screen.get_height() - (self.position.y + self.size.y)

                glPushMatrix()

                glBegin(GL_QUADS)
                glColor4f(*self._color.to_tuple())
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
                posX:int = self.position.x
                posY:int = self.position.y
                posWidth:int = self.position.x + self.size.x
                posHeight:int = self.position.y + self.size.y

                if not self._flipped:
                    posY = self._engine.screen.get_height() - (self.position.y + self.size.y)

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
    
    def set_border(self, color:ColorRGBA, width:int) -> None:
        '''
        Set the border of this object
        
        Parameters
        ----------
        color : wame.color.rgb.ColorRGBA
            The color to set the border to
        width : int
            The width of the border
        '''
        
        self._border_color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)
        self._border_width = width

    def set_callback(self, func:Callable[[None], None]) -> None:
        '''
        Set the callback method for when this input is edited/activated/deactivated
        
        Parameters
        ----------
        func : typing.Callable[[None], None]
            The callback method to call
        '''

        self._callback = func

    def set_color(self, color:ColorRGBA) -> None:
        '''
        Set the color of this object
        
        Parameters
        ----------
        color : wame.color.rgb.ColorRGBA
            The color of this object
        '''
        
        self._color = color if isinstance(color, ColorRGBA) else ColorRGBA.from_tuple(color)

    def set_pixel_position(self, position:IntVector2) -> None:
        '''
        Set the exact pixel position of this object
        
        Parameters
        ----------
        position : wame.vector.xy.IntVector2
            The exact position of this object from the top-left point
        '''

        position = position if isinstance(position, IntVector2) else IntVector2.from_iterable(position)

        if self._parent:
            position.x += self._parent.position.x
            position.y += self._parent.position.y
        
        self.position = position

        if self.size:
            self.text.set_pixel_position((
                10, (self.size.y // 2) - (self.text.rect.height // 2)
            ))

    def set_pixel_size(self, size:IntVector2) -> None:
        '''
        Set the exact pixel size of this object
        
        Parameters
        ----------
        size : wame.vector.xy.IntVector2
            The exact size of this object
        '''
        
        self.size = size if isinstance(size, IntVector2) else IntVector2.from_iterable(size)

        if self.position:
            self.text.set_pixel_position((
                10, (self.size.y // 2) - (self.text.text.get_height() // 2)
            ))

    def set_scaled_position(self, position:FloatVector2) -> None:
        '''
        Set the scaled position of this object
        
        Parameters
        ----------
        position : wame.vector.xy.FloatVector2
            The scaled position of this object from the top-left point
        
        Raises
        ------
        ValueError
            If the provided positional values exceed `0`-`1`
        '''

        position = position if isinstance(position, FloatVector2) else FloatVector2.from_iterable(position)

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

        if self.size:
            self.text.set_pixel_position((
                10, (self.size.y // 2) - (self.text.rect.height // 2)
            ))
    
    def set_scaled_size(self, size:IntVector2) -> None:
        '''
        Set the scaled size of this object
        
        Parameters
        ----------
        size : wame.vector.xy.IntVector2
            The scaled size of this object
        
        Raises
        ------
        ValueError
            If the provided size values exceed `0`-`1`
        '''

        size = size if isinstance(size, FloatVector2) else FloatVector2.from_iterable(size)

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

        self.text.set_pixel_position((
                10, (self.size.y // 2) - (self.text.rect.height // 2)
            ))