from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from dataclasses import dataclass
from numpy import ndarray
from typing import Callable, Iterable, Union
from wame.color.rgb import ColorRGBA
from wame.ui.anchor import Anchor
from wame.ui.element import Element
from wame.utils.tween import Easing, Tween
from wame.vector.xy import IntVector2

import pygame

__all__ = ("TextTween", "Text",)

@dataclass(frozen=True, slots=True)
class TextTween:
    started_at: int
    duration: Union[int, float]
    easing: Callable[[float], float]
    start_position: tuple[Union[int, float], Union[int, float]]
    end_position: tuple[Union[int, float], Union[int, float]]

class Text(Element):
    '''User-Interface Text.'''

    def __init__(
        self,
        scene: 'Scene',
        parent: Element,
        *,
        text: str,
        color: ColorRGBA,
        font: pygame.font.Font,
        position: tuple[Union[int, float], Union[int, float]],
        anchor: Anchor = Anchor.TOP_LEFT
    ) -> None:
        '''
        Create a new user interface text.
        
        Parameters
        ----------
        scene : Scene
            The scene to interface this instance with.
        parent : Element
            Any `~Element`-like object to make the parent of this instance.
        text : str
            The text that will be shown.
        color : ColorRGBA
            The color of the foreground (text).
        font : pygame.font.Font
            The font to render the text as.
        position : tuple[int | float, int | float]`
            - The X and Y values for the pixels in which this element will be placed.
            - If `int` they represent absolute pixel values, otherwise (`float`) will represent scaled pixel values.
        anchor : Anchor
            The chosen area of this element to place at the position provided.
        
        Raises
        ------
        TypeError
            - Provided text isn't a `str`.
            - Provided font isn't a `pygame.font.Font`.
            - Provided position X and Y values aren't `int` or `float`.
            - Provided anchor isn't an `Anchor` object.
        ValueError
            - If any value of position is `float` and is not between `0` and `1`.
            - If values of position are not two values in length.
        '''

        if not isinstance(text, str):
            error: str = "Provided text must be a `str` object"
            raise TypeError(error)
        
        if not isinstance(font, pygame.font.Font):
            error: str = "Provided font must be a `pygame.font.Font` object"
            raise TypeError(error)
        
        for value in [position[0], position[1]]:
            if isinstance(value, int):
                continue

            if isinstance(value, float):
                if 0.0 > value or value > 1.0:
                    error: str = "Position values must be between 0 and 1 if they are `float`"
                    raise ValueError(error)
                
                continue

            error: str = "Position can only contain `int` or `float` values"
            raise TypeError(error)
        
        if len(position) != 2:
            error: str = "Position values can only contain 2 values"
            raise ValueError(error)
        
        if not isinstance(anchor, Anchor):
            error: str = "Provided anchor must be an `Anchor` object"
            raise TypeError(error)
        
        super().__init__(scene, parent)
        self._parent.add_child(self)
        self._scene.engine._antialiasing_hooks.add(self._update_text)

        self._local_position: tuple[Union[int, float], Union[int, float]] = position
        self._anchor: Anchor = anchor

        self._calculated_position: IntVector2 = None

        self._color: ColorRGBA = color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)

        self._text: str = text
        self._font: pygame.font.Font = font

        self.text_render: pygame.Surface = None
        '''Rendered internal text object that is updated every change - Usable with `OpenGL` as well.'''

        self._tween: TextTween = None

        self._update_text()
        self._apply_transform()

    def __repr__(self) -> str:
        return "Text(" + ', '.join([
            f"pos={self._calculated_position}",
            f"size={self.text_render.get_rect().size}",
            f"anchor={self._anchor}",
            f"color={self._color}",
            f"text={self._text}",
            f"font={self._font}"
        ]) + ')'
    
    def _apply_transform(self) -> None:
        self._calculated_position = self._calculate_transform(self._local_position)

        for child in self._children:
            child._apply_transform()

    def _calculate_transform(
        self,
        position: tuple[Union[int, float], Union[int, float]]
    ) -> IntVector2:
        new_position: IntVector2 = IntVector2(0, 0)

        parent_bounds: pygame.Rect = self._parent.bounds
        
        if isinstance(position[0], int):
            new_position.x = position[0] + parent_bounds.x
        else:
            new_position.x = round(position[0] * parent_bounds.width) + parent_bounds.x
        
        if isinstance(position[1], int):
            new_position.y = position[1] + parent_bounds.y
        else:
            new_position.y = round(position[1] * parent_bounds.height) + parent_bounds.y
        
        return Anchor.calculate_position(new_position, IntVector2.from_iterable(self.text_render.get_rect().size), self._anchor)
    
    @staticmethod
    def _interpolate(start: Union[int, float], end: Union[int, float], progress: float) -> Union[int, float]:
        return start + (end - start) * progress
    
    def _update(self) -> None:
        if not self._tween:
            return
        
        progress: float = Tween.calculate_progress(self._tween.started_at, self._tween.duration, self._tween.easing)
        self._local_position = (
            self._interpolate(self._tween.start_position[0], self._tween.end_position[0], progress),
            self._interpolate(self._tween.start_position[1], self._tween.end_position[1], progress)
        )

        self._apply_transform()

        if progress < 1.0:
            return
        
        self._tween = None

        if not self._tween_callback:
            return
        
        self._tween_callback()
    
    def _update_text(self) -> None:
        self.text_render = self._font.render(self._text, self._scene.engine.settings.antialiasing, self._color)
    
    @property
    def bounds(self) -> pygame.Rect:
        return pygame.Rect(self._calculated_position, self.text_render.get_rect().size)
    
    @property
    def color_text(self) -> ColorRGBA:
        '''The color of the text.'''
        return self._color
    
    @color_text.setter
    def color_text(self, value: ColorRGBA) -> None:
        if not value:
            error: str = "A color must be provided"
            raise ValueError(error)
        
        self._color = value if isinstance(value, ColorRGBA) else ColorRGBA.from_iterable(value)
        self._update_text()

    @property
    def text(self) -> str:
        '''The text being shown in this element.'''
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        if not value:
            error: str = "A text string must be provided"
            raise ValueError(error)
        
        if not isinstance(value, str):
            error: str = "Text string value must be `str`"
            raise TypeError(error)
        
        self._text = value
        self._update_text()

    def render(self) -> None:
        self._scene.screen.blit(self.text_render, self._calculated_position)

    def set_font(self, font: pygame.font.Font) -> None:
        '''
        Set the font of the rendered text.
        
        Parameters
        ----------
        font : pygame.font.Font
            The font to set the text to render as.
        
        Raises
        ------
        TypeError
            If the provided font is not `pygame.font.Font`
        '''

        if not isinstance(font, pygame.font.Font):
            error: str = "Font must be of type `pygame.font.Font`"
            raise TypeError(error)
        
        self._font = font
        self._update_text()

    def set_transform(
        self,
        *,
        anchor: Anchor = None,
        position: tuple[Union[int, float], Union[int, float]] = None,
    ) -> None:
        '''
        Set the transform (position, size, anchor) attributes of this element.
        
        Parameters
        ----------
        anchor : Anchor
            If provided, change the anchor point of this element.
        position : tuple[int | float, int | float]
            If provided, change the position of this element - `int` for absolute, `float` for scaled.
        
        Info
        ----
        `anchor`, `position`, or `size` are optional, but one has to be specified.

        Raises
        ------
        TypeError
            - Provided anchor isn't an `Anchor` object.
            - Provided position X and Y values aren't `int` or `float`.
        ValueError
            - If none of the parameters above are provided.
            - If any value of position is `float` and is not between `0` and `1`.
        '''
        
        if not anchor and not position:
            error: str = "Method requires at least one of `anchor` or `position` to be specified"
            raise ValueError(error)

        if anchor:
            if not isinstance(anchor, Anchor):
                error: str = "Provided anchor must be an `Anchor` object"
                raise TypeError(error)
            
            self._anchor = anchor
        
        if position:
            if not isinstance(position[0], (int, float)) or not isinstance(position[1], (int, float)):
                error: str = "Provided position X and Y values must be either `int` or `float`"
                raise TypeError(error)
            
            if isinstance(position[0], float) and (0.0 > position[0] or 1.0 < position[0]):
                error: str = "Provided position X value must be between 0 and 1 as it's a `float`"
                raise ValueError(error)
            
            if isinstance(position[1], float) and (0.0 > position[1] or 1.0 < position[1]):
                error: str = "Provided position Y value must be between 0 and 1 as it's a `float`"
                raise ValueError(error)
            
            self._local_position = position
        
        self._apply_transform()
    
    def tween(
        self,
        position: Iterable[Union[int, float]],
        duration: float,
        easing: Callable[[float], float] = Easing.LINEAR
    ) -> None:
        '''
        Tween/animate this element to an end state over a period of time.
        
        Parameters
        ----------
        position : typing.Iterable[int | float]
            The end position to reach.
        duration : float
            The time in which it'll take to animate this element in seconds.
        easing : typing.Callable[[float], float]
            The easing function to use when animating.
        
        Raises
        ------
        TypeError
            - If `position` is not an iterable object.
            - If `duration` is not `int` or `float`.
        ValueError
            - If `position` doesn't contain only two values.
            - If `position` or `duration` don't contain `int` or `float` values.
        '''

        if not isinstance(position, (tuple, list, ndarray)):
            error: str = "Provided `position` must be an iterable (tuple, list, NumPy array, etc.)"
            raise TypeError(error)
    
        if not isinstance(duration, (int, float)):
            error: str = "Provided `duration` must be an `int` or `float`"
            raise TypeError(error)
        
        if len(position) != 2:
            error: str = "Provided `position` must only contain two values"
            raise ValueError(error)

        for value in position:
            if isinstance(value, (int, float)):
                continue

            error: str = "Provided `position` values can only be `int` or `float`"
            raise ValueError(error)

        self._tween = TextTween(
            pygame.time.get_ticks(), duration, easing,
            self._local_position, position
        )