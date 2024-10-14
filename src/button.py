from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.vector import IntVector3, IntVector2
from wame.area import Area
from wame.text import Text

import pygame

class Button:
    '''2D User Interface Button'''

    def __init__(
        self, scene:'Scene', color:IntVector3 | tuple[int, int, int],
        hoverColor:IntVector3 | tuple[int, int, int], text:Text=None
    ) -> None:
        '''
        Instantiate a new button
        
        Parameters
        ----------
        scene : `wame.Scene`
            The scene to assign this button to
        color : `wame.IntVector3 | tuple[int, int, int]`
            The background color of the button (RGB values)
        hoverColor : `wame.IntVector3 | tuple[int, int, int]`
            The background color of the button when hovered on by the cursor (RGB values)
        text : `wame.Text`
            The text to render on the button - Optional, default `None`
        '''
        
        self._scene:'Scene' = scene
        self._scene._buttons.append(self)

        self.rect:pygame.Rect = None
        '''The button's rectangular position and size'''

        self._baseColor:IntVector3 = color if isinstance(color, IntVector3) else IntVector3.from_tuple(color)
        self._hoverColor:IntVector3 = hoverColor if isinstance(hoverColor, IntVector3) else IntVector3.from_tuple(hoverColor)
        self._currentColor:IntVector3 = self._baseColor

        self._text:Text = text

        self._clickExecutor:Callable = None
        self._hoverExecutor:Callable = None

    def _check_click(self, mousePosition:IntVector2) -> None:
        if self.rect is None:
            error:str = "Button must have a position and size defined. Please use the Button.set_transform() method."
            raise ValueError(error)
        
        if not self.rect.collidepoint(mousePosition.x, mousePosition.y):
            return
        
        if self._clickExecutor is None:
            return
        
        self._clickExecutor()

    def _check_hover(self, mousePosition:IntVector2) -> None:
        if self.rect is None:
            error:str = "Button must have a position and size defined. Please use the Button.set_transform() method."
            raise ValueError(error)
        
        if not self.rect.collidepoint(mousePosition.x, mousePosition.y):
            self._currentColor = self._baseColor
            
            return
        
        self._currentColor = self._hoverColor

        if self._hoverExecutor is None:
            return
        
        self._hoverExecutor()

    def render(self) -> None:
        '''
        Render this button to the screen
        
        Note
        ----
        This method should only need to be used in a `Scene.on_update()` method
        
        Raises
        ------
        `ValueError`
            If the button has not had its transform defined.

        Example
        -------
        ```python
        class MyScene(wame.Scene):
            def __init__(self, engine) -> None:
                super().__init__(engine)
            
                self.button:wame.Button = wame.Button(...)
                self.button.set_transform(...)

            def on_update(self) -> None:
                self.button.render()
        ```
        '''
        
        if self.rect is None:
            error:str = "Button must have a position and size defined. Please use the Button.set_transform() method."
            raise ValueError(error)
        
        pygame.draw.rect(self._scene.engine.screen, self._currentColor.to_tuple(), self.rect)

        if self._text is not None:
            self._text.render()

    def set_click_callback(self, callback:Callable) -> None:
        '''
        Sets the function to call when the button is clicked
        
        Parameters
        ----------
        callback : `Callable`
            The function to call when the button is clicked
        '''

        self._clickExecutor = callback
    
    def set_hover_callback(self, callback:Callable) -> None:
        '''
        Sets the function to call when the button is hovered over
        
        Parameters
        ----------
        callback : `Callable`
            The function to call when the button is hovered over
        '''

        self._hoverExecutor = callback

    def set_position(self, position:IntVector2 | tuple[int, int], area:Area=Area.TOP_LEFT) -> None:
        '''
        Sets the position of the button
        
        Parameters
        ----------
        position : `wame.IntVector2 | tuple[int, int]`
            The X, Y position values
        area : `wame.Area`
            The location of the button in relation to the position - Default `TOP_LEFT`
        
        Raises
        ------
        `ValueError`
            If the button has not had it's size defined yet.
        '''

        if self.rect is None:
            error:str = "Button must have a size defined. Please use the Button.set_transform() method."
            raise ValueError(error)
        
        if isinstance(position, tuple):
            position:IntVector2 = IntVector2.from_tuple(position)
        
        properPosition:IntVector2 = Area.calculate_position(position, area, IntVector2.from_tuple(self.rect.size))
        self.rect = pygame.Rect(properPosition.x, properPosition.y, self.rect.width, self.rect.height)

        buttonCenterX:int = self.rect.x + (self.rect.width // 2)
        buttonCenterY:int = self.rect.y + (self.rect.height // 2)

        textX:int = buttonCenterX - (self._text._textRender.get_width() // 2)
        textY:int = buttonCenterY - (self._text._textRender.get_height() // 2)

        if self._text is not None:
            self._text.set_position(IntVector2(textX, textY))

        self._check_hover(IntVector2.from_tuple(pygame.mouse.get_pos()))

    def set_size(self, size:IntVector2 | tuple[int, int]) -> None:
        '''
        Set the size of the button
        
        Note
        ----
        This does not affect the position of the button in any way.
        Ensure the position stays the same if edited.

        Parameters
        ----------
        size : `wame.IntVector2 | tuple[int, int]`
            The X, Y size values
        
        Raises
        ------
        `ValueError`
            If the button has not had it's position defined yet.
        '''
        
        if self.rect is None:
            error:str = "Button must have a position defined. Please use the Button.set_transform() method."
            raise ValueError(error)
        
        if isinstance(size, tuple):
            size:IntVector2 = IntVector2.from_tuple(size)
        
        self.rect = pygame.Rect(self.rect.left, self.rect.top, size.x, size.y)

        self._check_hover(IntVector2.from_tuple(pygame.mouse.get_pos()))

    def set_transform(self, position:IntVector2 | tuple[int, int], size:IntVector2 | tuple[int, int], area:Area=Area.TOP_LEFT) -> None:
        '''
        Sets the position and size (transform) of the button in relation to the provided area
        
        Parameters
        ----------
        position : `wame.IntVector2 | tuple[int, int]`
            The X, Y position of the button
        size : `wame.IntVector2 | tuple[int, int]`
            The X, Y size of the button
        area : `wame.Area`
            The location of the button in relation to the position - Default `TOP_LEFT`
        '''

        if isinstance(position, tuple):
            position:IntVector2 = IntVector2.from_tuple(position)
        
        if isinstance(size, tuple):
            size:IntVector2 = IntVector2.from_tuple(size)
        
        properPosition:IntVector2 = Area.calculate_position(position, area, size)
        self.rect = pygame.Rect(properPosition.x, properPosition.y, size.x, size.y)

        buttonCenterX:int = self.rect.x + (self.rect.width // 2)
        buttonCenterY:int = self.rect.y + (self.rect.height // 2)

        if self._text is not None:
            textX:int = buttonCenterX - (self._text._textRender.get_width() // 2)
            textY:int = buttonCenterY - (self._text._textRender.get_height() // 2)

            self._text.set_position(IntVector2(textX, textY))

        self._check_hover(IntVector2.from_tuple(pygame.mouse.get_pos()))