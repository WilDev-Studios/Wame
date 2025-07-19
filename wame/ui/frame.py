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

__all__ = ("Frame", "FrameBorderMetadata", "FrameTween",)

@dataclass(frozen=True, slots=True)
class FrameTween:
    started_at: int
    duration: Union[int, float]
    easing: Callable[[float], float]
    start_position: tuple[Union[int, float], Union[int, float]]
    start_size: tuple[Union[int, float], Union[int, float]]
    end_position: tuple[Union[int, float], Union[int, float]]
    end_size: tuple[Union[int, float], Union[int, float]]

@dataclass(slots=True)
class FrameBorderMetadata:
    width: int
    color: ColorRGBA
    bottom_left_radius: int
    bottom_right_radius: int
    top_left_radius: int
    top_right_radius: int

class Frame(Element):
    '''User-Interface Frame.'''

    __slots__ = (
        "_local_position", "_local_size", "_anchor", "_calculated_position",
        "_calculated_size", "_color", "_border", "_tween",
    )
    _local_position: tuple[Union[int, float], Union[int, float]]
    _local_size: tuple[Union[int, float], Union[int, float]]
    _anchor: Anchor
    _calculated_position: IntVector2
    _calculated_size: IntVector2
    _color: ColorRGBA
    _border: FrameBorderMetadata
    _tween: FrameTween

    def __init__(
        self, scene: 'Scene', parent: Element, *,
        position: tuple[Union[int, float], Union[int, float]],
        size: tuple[Union[int, float], Union[int, float]],
        anchor: Anchor=Anchor.TOP_LEFT,
        color: ColorRGBA=None
    ) -> None:
        '''
        Create a new user interface frame.
        
        Parameters
        ----------
        scene : Scene
            The scene to interface this instance with.
        parent : Element
            Any `~Element`-like object to make the parent of this instance.
        position : tuple[int | float, int | float]
            - The X and Y values for the pixels in which this element will be placed.
            - If `int` they represent absolute pixel values, otherwise (`float`) will represent scaled pixel values.
        size : tuple[int | float, int | float]
            - The X and Y values for the pixels in which this element will be sized.
            - If `int` they represent absolute pixel values, otherwise (`float`) will represent scaled pixel values.
        anchor : Anchor
            The chosen area of this element to place at the position provided.
        color : ColorRGBA
            If provided, the color of this element when rendered.
        
        Raises
        ------
        TypeError
            - Provided anchor isn't an `Anchor` object.
            - Provided position X and Y values aren't `int` or `float`.
            - Provided size X and Y values aren't `int` or `float.
        ValueError
            - If any value of position or size are `float` and are not between `0` and `1`.
            - If values of position and size are not two values in length.
        '''
        
        for value in [position[0], position[1], size[0], size[1]]:
            if isinstance(value, int):
                continue

            if isinstance(value, float):
                if 0.0 > value or value > 1.0:
                    error: str = "Position and size values must be between 0 and 1 if they are `float`"
                    raise ValueError(error)
                
                continue

            error: str = "Position and size values can only contain `int` or `float` values"
            raise TypeError(error)
        
        if len(position) != 2 or len(size) != 2:
            error: str = "Position and size values can only contain 2 values each"
            raise ValueError(error)
        
        if not isinstance(anchor, Anchor):
            error: str = "Provided anchor must be an `Anchor` object"
            raise TypeError(error)
        
        super().__init__(scene, parent)

        if parent:
            self._parent.add_child(self)

        self._local_position: tuple[Union[int, float], Union[int, float]] = position
        self._local_size: tuple[Union[int, float], Union[int, float]] = size
        self._anchor: Anchor = anchor

        self._calculated_position: IntVector2 = None
        self._calculated_size: IntVector2 = None
        self._apply_transform()

        self._border: FrameBorderMetadata = None
        self._color: ColorRGBA = (color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)) if color else None

        self._tween: FrameTween = None
    
    def __repr__(self) -> str:
        return f"Frame(pos={self._calculated_position}, size={self._calculated_size}, anchor={self._anchor}, color={self._color})"

    def _apply_transform(self) -> None:
        self._calculated_position, self._calculated_size = self._calculate_transform(self._local_position, self._local_size)

        for child in self._children:
            child._apply_transform()

    def _calculate_transform(self, position: tuple[Union[int, float], Union[int, float]], size: tuple[Union[int, float], Union[int, float]]) -> tuple[IntVector2, IntVector2]:
        new_size: IntVector2 = IntVector2(0, 0)
        new_position: IntVector2 = IntVector2(0, 0)

        parent_bounds: pygame.Rect = self._parent.bounds if self._parent else self._scene.screen.get_rect()

        if isinstance(size[0], int):
            new_size.x = size[0]
        else:
            new_size.x = round(size[0] * parent_bounds.width)
        
        if isinstance(size[1], int):
            new_size.y = size[1]
        else:
            new_size.y = round(size[1] * parent_bounds.height)
        
        if isinstance(position[0], int):
            new_position.x = position[0] + parent_bounds.x
        else:
            new_position.x = round(position[0] * parent_bounds.width) + parent_bounds.x

        if isinstance(position[1], int):
            new_position.y = position[1] + parent_bounds.y
        else:
            new_position.y = round(position[1] * parent_bounds.height) + parent_bounds.y
        
        return Anchor.calculate_position(new_position, new_size, self._anchor), new_size

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
        self._local_size = (
            self._interpolate(self._tween.start_size[0], self._tween.end_size[0], progress),
            self._interpolate(self._tween.start_size[1], self._tween.end_size[1], progress)
        )

        self._apply_transform()

        if progress < 1.0:
            return
        
        self._tween = None
        
        if not self._tween_callback:
            return
        
        self._tween_callback()

    @property
    def bounds(self) -> pygame.Rect:
        return pygame.Rect(self._calculated_position, self._calculated_size)

    @property
    def color(self) -> Union[ColorRGBA, None]:
        '''The color of this frame - Can be `None`.'''
        return self._color
    
    @color.setter
    def color(self, color: ColorRGBA) -> None:
        self._color = (color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)) if color else None

    def render(self) -> None:
        if self._color:
            if self._border:
                pygame.draw.rect(self._scene.screen, self._color, self.bounds,
                    border_top_left_radius=self._border.top_left_radius,
                    border_top_right_radius=self._border.top_right_radius,
                    border_bottom_left_radius=self._border.bottom_left_radius,
                    border_bottom_right_radius=self._border.bottom_right_radius
                )
            else:
                pygame.draw.rect(self._scene.screen, self._color, self.bounds)
        
        if self._border:
            pygame.draw.rect(self._scene.screen, self._border.color, self.bounds, self._border.width,
                border_top_left_radius=self._border.top_left_radius,
                border_top_right_radius=self._border.top_right_radius,
                border_bottom_left_radius=self._border.bottom_left_radius,
                border_bottom_right_radius=self._border.bottom_right_radius
            )
    
    def set_border(
        self, color: ColorRGBA=None, *, width: int=1, radius: int=0,
        radius_bottom_left: int=None, radius_bottom_right: int=None,
        radius_top_left: int=None, radius_top_right: int=None
    ) -> None:
        '''
        Set the border attributes of this element.
        
        Parameters
        ----------
        color : ColorRGBA
            The color to set the border as - `None` will disable the border.
        width : int
            The width of the border - `None`/`0` will disable the border.
        radius : int
            The radius of the border - Initial value of all corners unless overriden by following parameters.
        radius_bottom_left : int
            The radius of the bottom left corner.
        radius_bottom_right: int
            The radius of the bottom right corner.
        radius_top_left : int
            The radius of the top left corner.
        radius_top_right : int
            The radius of the top right corner.
        
        Raises
        ------
        TypeError
            - If `width` is not an `int`.
            - If any `radius` value isn't an `int`.
        ValueError
            If any `radius` value is less than `0`.
        '''

        if not color or not width or width == 0:
            self._border = None
            return

        color: ColorRGBA = color if isinstance(color, ColorRGBA) else ColorRGBA.from_iterable(color)

        if not isinstance(width, int):
            error: str = "Provided width must be an `int`"
            raise TypeError(error)
        
        values: list[int] = [radius]

        if radius_bottom_left: values.append(radius_bottom_left)
        if radius_bottom_right: values.append(radius_bottom_right)
        if radius_top_left: values.append(radius_top_left)
        if radius_top_right: values.append(radius_top_right)

        for value in values:
            if isinstance(value, int):
                if value >= 0:
                    continue

                error: str = "Radius values must be `0` or greater"
                raise ValueError(error)

            error: str = "Radius values must be `int`"
            raise TypeError(error)
        
        self._border = FrameBorderMetadata(
            width, color,
            bottom_left_radius=radius_bottom_left if radius_bottom_left else radius,
            bottom_right_radius=radius_bottom_right if radius_bottom_right else radius,
            top_left_radius=radius_top_left if radius_top_left else radius,
            top_right_radius=radius_top_right if radius_top_right else radius,
        )

    def set_transform(
        self, *, anchor: Anchor=None,
        position: tuple[Union[int, float], Union[int, float]]=None,
        size: tuple[Union[int, float], Union[int, float]]=None,
    ) -> None:
        '''
        Set the transform (position, size, anchor) attributes of this element.
        
        Parameters
        ----------
        anchor : Anchor
            If provided, change the anchor point of this element.
        position : tuple[int | float, int | float]
            If provided, change the position of this element - `int` for absolute, `float` for scaled.
        size : tuple[int | float, int | float]
            If provided, change the size of this element - `int` for absolute, `float` for scaled.
        
        Info
        ----
        `anchor`, `position`, or `size` are optional, but one has to be specified.

        Raises
        ------
        TypeError
            - Provided anchor isn't an `Anchor` object.
            - Provided position X and Y values aren't `int` or `float`.
            - Provided size X and Y values aren't `int` or `float.
        ValueError
            - If none of the parameters above are provided.
            - If any value of position or size are `float` and are not between `0` and `1`.
        '''
        
        if not anchor and not position and not size:
            error: str = "Method requires at least one of `anchor`, `position`, or `size` to be specified"
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
        
        if size:
            if not isinstance(size[0], (int, float)) or not isinstance(size[1], (int, float)):
                error: str = "Provided size X and Y values must be either `int` or `float`"
                raise TypeError(error)
            
            if isinstance(size[0], float) and (0.0 > size[0] or 1.0 < size[0]):
                error: str = "Provided size X value must be between 0 and 1 as it's a `float`"
                raise ValueError(error)
            
            if isinstance(size[1], float) and (0.0 > size[1] or 1.0 < size[1]):
                error: str = "Provided size Y value must be between 0 and 1 as it's a `float`"
                raise ValueError(error)
            
            self._local_size = size
        
        self._apply_transform()
    
    def tween(
        self, *, position: Iterable[Union[int, float]]=None,
        size: Iterable[Union[int, float]]=None, duration: float,
        easing: Callable[[float], float]=Easing.LINEAR
    ) -> None:
        '''
        Tween/animate this element to an end state over a period of time.
        
        Parameters
        ----------
        position : typing.Iterable[int | float]
            The end position to reach, if provided.
        size : typing.Iterable[int | float]
            The end size to reach, if provided.
        duration : float
            The time in which it'll take to animate this element in seconds.
        easing : typing.Callable[[float], float]
            The easing function to use when animating.
        
        Info
        ----
        - Parameters `position` and `size` are mutually exclusive.
        - Either one, or both, has to be passed.
        
        Raises
        ------
        TypeError
            - If `position` or `size` are not iterable objects.
            - If `duration` is not `int` or `float`.
        ValueError
            - If `position` and `size` are not defined.
            - If `position` or `size` don't contain only two values.
            - If `position`, `size`, or `duration` don't contain `int` or `float` values.
        '''
        
        if not position and not size:
            error: str = "At least one of `end_position` or `end_size` must be defined"
            raise ValueError(error)

        if position and not isinstance(position, (tuple, list, ndarray)):
            error: str = "Provided `position` must be an iterable (tuple, list, NumPy array, etc.)"
            raise TypeError(error)
        
        if size and not isinstance(size, (tuple, list, ndarray)):
            error: str = "Provided `size` must be an iterable (tuple, list, NumPy array, etc.)"
            raise TypeError(error)
        
        if not isinstance(duration, (int, float)):
            error: str = "Provided `duration` must be an `int` or `float`"
            raise TypeError(error)
        
        if position and len(position) != 2:
            error: str = "Provided `position` can only contain two values"
            raise ValueError(error)
        
        if size and len(size) != 2:
            error: str = "Provided `size` can only contain two values"
            raise ValueError(error)

        values: list[Union[int, float]] = [duration]

        if position:
            values.extend([position[0], position[1]])
        
        if size:
            values.extend([size[0], size[1]])

        for value in values:
            if isinstance(value, (int, float)):
                continue

            error: str = "Provided `position`, `size`, and `duration` values can only contain `int` or `float` values"
            raise ValueError(error)
        
        self._tween = FrameTween(
            pygame.time.get_ticks(), duration, easing,
            self._local_position, self._local_size,
            position if position else self._local_position,
            size if size else self._local_size
        )