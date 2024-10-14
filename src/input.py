from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

import pygame
import wame

class TextInput:
    def __init__(self, scene:'Scene', position:wame.IntVector2, size:wame.IntVector2,
        font:wame.Font, textColor:wame.IntVector3, backgroundColor:wame.IntVector3,
        *, borderColor:wame.IntVector3=None, borderWidth:int=0
    ) -> None:
        '''
        Instantiate a new text input instance
        
        Parameters
        ----------
        scene : `wame.Scene`
            The parent scene to manage this instance
        position : `wame.IntVector2`
            The top-left X and Y coordinates to place the input
        size : `wame.IntVector2`
            The width and height of the input
        font : `wame.Font`
            The font of the inside text
        textColor : `wame.IntVector3`
            The RGB values of the inside text
        backgroundColor : `wame.IntVector3`
            The RGB values of the background clor
        borderColor : `wame.IntVector3`
            The RGB values of the border color when selected - Optional, default `None`
        borderWidth : `wame.IntVector3`
            The width of the border if present - Optional, default `0`
        '''
        
        self._scene:'Scene' = scene

        self._position:wame.IntVector2 = position if isinstance(position, wame.IntVector2) else wame.IntVector2.from_tuple(position)
        self._size:wame.IntVector2 = size if isinstance(size, wame.IntVector2) else wame.IntVector2.from_tuple(size)
    
        self.rect:pygame.Rect = pygame.Rect(self._position.x, self._position.y, self._size.x, self._size.y)
        '''Dimensions and transform of this instance'''

        self._background_color:wame.IntVector3 = backgroundColor if isinstance(backgroundColor, wame.IntVector3) else wame.IntVector3.from_tuple(backgroundColor)
        self._border_color:wame.IntVector3 = None

        if borderColor is None:
            self._border_color = self._background_color
        else:
            self._border_color = borderColor if isinstance(borderColor, wame.IntVector3) else wame.IntVector3.from_tuple(borderColor)

        self._border_width:int = borderWidth

        self.active:bool = False
        '''If the input (should be/is) currently selected'''

        self.text:wame.Text = wame.Text(self._scene, "", font, textColor)
        '''Inside text of the input'''

        self.text.set_position((self._position.x + self._border_width, (self._position.y + (self._size.y // 2)) - (self.text._textRender.get_height() // 2)))

    def check_key(self, key:int, mods:int) -> bool:
        '''
        Check if the input should handle anything text related based on the keys submitted
        
        Parameters
        ----------
        key : `int`
            The integer keycode to check
        mods : `int`
            The bitwise-combined keymods to apply (like CTRL, SHIFT, etc.)
        
        Returns
        -------
        changed : `bool`
            If the state of the input was changed based on the provided key
        '''

        changed:bool = False

        if key >= pygame.K_a and key <= pygame.K_z:
            name:str = pygame.key.name(key)
            self.text.set_text(self.text._text + (name.upper() if mods & pygame.KMOD_SHIFT else name.lower()))

            changed = True
        elif key >= pygame.K_0 and key <= pygame.K_9:
            symbols:dict[int, str] = {
                pygame.K_0: ')', pygame.K_1: '!', pygame.K_2: '@',
                pygame.K_3: '#', pygame.K_4: '$', pygame.K_5: '%',
                pygame.K_6: '^', pygame.K_7: '&', pygame.K_8: '*',
                pygame.K_9: '('
            }

            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + symbols[key])
            else:
                self.text.set_text(self.text._text + pygame.key.name(key))
            
            changed = True
        elif key == pygame.K_BACKQUOTE:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '~')
            else:
                self.text.set_text(self.text._text + '`')

            changed = True
        elif key == pygame.K_MINUS:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '_')
            else:
                self.text.set_text(self.text._text + '-')

            changed = True
        elif key == pygame.K_EQUALS:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '+')
            else:
                self.text.set_text(self.text._text + '=')

            changed = True
        elif key == pygame.K_LEFTBRACKET:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '{')
            else:
                self.text.set_text(self.text._text + '[')

            changed = True
        elif key == pygame.K_RIGHTBRACKET:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '}')
            else:
                self.text.set_text(self.text._text + ']')

            changed = True
        elif key == pygame.K_BACKSLASH:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '|')
            else:
                self.text.set_text(self.text._text + '\\')

            changed = True
        elif key == pygame.K_SEMICOLON:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + ':')
            else:
                self.text.set_text(self.text._text + ';')

            changed = True
        elif key == pygame.K_QUOTE:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '"')
            else:
                self.text.set_text(self.text._text + "'")

            changed = True
        elif key == pygame.K_COMMA:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '<')
            else:
                self.text.set_text(self.text._text + ',')

            changed = True
        elif key == pygame.K_PERIOD:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '>')
            else:
                self.text.set_text(self.text._text + '.')

            changed = True
        elif key == pygame.K_SLASH:
            if mods & pygame.KMOD_SHIFT:
                self.text.set_text(self.text._text + '?')
            else:
                self.text.set_text(self.text._text + '/')

            changed = True
        elif key == pygame.K_BACKSPACE:
            if len(self.text._text) == 0:
                return
            
            self.text.set_text(self.text._text[:-1])

            changed = True
        elif key == pygame.K_SPACE:
            self.text.set_text(self.text._text + ' ')

            changed = True
        
        return changed

    def render(self) -> None:
        '''
        Render the text input to the parent scene of this instance
        '''
        
        if self.active:
            pygame.draw.rect(self._scene.screen, self._border_color.to_tuple(), self.rect, self._border_width)
        else:
            pygame.draw.rect(self._scene.screen, self._background_color.to_tuple(), self.rect)
        
        self.text.render()
    
    def set_position(self, position:wame.IntVector2) -> 'TextInput':
        '''
        Sets the position of the input
        
        Parameters
        ----------
        position : `wame.IntVector2`
            The new position of the input
        
        Returns
        -------
        input : `wame.TextInput`
            This instance to allow call-chaining
        '''

        self._position = position if isinstance(position, wame.IntVector2) else wame.IntVector2.from_tuple(position)
        self.rect = pygame.Rect(self._position.x, self._position.y, self.rect.width, self.rect.height)
        self.text.set_position((self._position.x + self._border_width, (self._position.y + (self._size.y // 2)) - (self.text._textRender.get_height() // 2)))

        return self